import os
import torch
import logging
from PIL import Image
import numpy as np
from torchvision.transforms import ToTensor

# 尝试导入修复相关模块，如果失败则提供模拟功能
try:
    from utils.misc import infer_deepfill
    
    def load_model(path, device):
        """正确加载模型，返回可调用的模型对象"""
        try:
            # 导入模型加载函数
            from model import load_model as load_model_from_checkpoint
            
            # 使用正确的模型加载函数
            model = load_model_from_checkpoint(path, device)
            if model:
                print(f"✅ 成功加载模型: {path}")
                return model
            else:
                print(f"❌ 加载模型失败: {path}")
                return None
                
        except Exception as e:
            print(f"❌ 加载模型时出错: {e}")
            # 备用方案：直接使用 torch.load
            try:
                checkpoint = torch.load(path, map_location=device)
                if 'G' in checkpoint:
                    # 根据模型类型创建对应的生成器
                    if 'stage1.conv1.conv.weight' in checkpoint['G'].keys():
                        from model.networks import Generator
                    else:
                        from model.networks_tf import Generator
                    
                    gen = Generator(cnum_in=5, cnum=48, return_flow=False)
                    gen.load_state_dict(checkpoint['G'], strict=False)
                    gen.to(device)
                    gen.eval()
                    print(f"✅ 备用方案成功加载模型: {path}")
                    return gen
                else:
                    print(f"❌ 检查点中未找到生成器权重")
                    return None
            except Exception as e2:
                print(f"❌ 备用方案也失败: {e2}")
                return None

    DEEPFILL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  DeepFill模块导入失败: {e}")
    DEEPFILL_AVAILABLE = False


    # 提供模拟函数
    def infer_deepfill(model, image_tensor, mask_tensor, return_vals):
        # 模拟修复过程 - 返回原图
        image_np = (image_tensor[0].cpu().numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
        return [image_np]


    def load_model(path, device):
        print(f"📦 模拟加载模型: {path}")
        return "mock_model"

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _load_models(config_path, device='cuda'):
    try:
        print(f"📖 读取模型配置: {config_path}")
        if not os.path.exists(config_path):
            logger.warning(f"配置文件不存在: {config_path}")
            return {}, {}

        with open(config_path, 'r', encoding='utf-8') as stream:
            yaml_data = yaml.safe_load(stream)
            models_config = yaml_data.get('models', {})

        valid_config = {}
        for name, cfg in models_config.items():
            model_path = cfg.get('path', '')
            full_path = os.path.join(os.path.dirname(config_path), model_path)
            if os.path.exists(full_path):
                valid_config[name] = {**cfg, 'full_path': full_path}
                print(f"✅ 找到模型: {name} -> {full_path}")
            else:
                logger.warning(f"❌ 模型 {name} 路径不存在: {full_path}")

        loaded_models = {}
        for name, cfg in valid_config.items():
            is_loaded = False
            if cfg.get('load_at_startup', False):
                try:
                    model = load_model(cfg['full_path'], device)
                    if model:
                        loaded_models[name] = model
                        is_loaded = True
                        print(f"✅ 成功加载模型: {name}")
                    else:
                        logger.error(f"加载模型 {name} 失败")
                except Exception as e:
                    logger.error(f"加载模型 {name} 时出错: {str(e)}")
            valid_config[name]['is_loaded'] = is_loaded

        return valid_config, loaded_models
    except Exception as e:
        logger.error(f"加载模型配置失败: {str(e)}")
        return {}, {}


class Inpainter:
    def __init__(self, device=None):
        self.available_models = {}
        self.loaded_models = {}
        self.host = ""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') \
            if device is None else device
        logger.info(f"使用设备: {self.device}")

        # 创建文件目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, '..', 'files')
        os.makedirs(files_dir, exist_ok=True)

    def set_host(self, host):
        self.host = host

    def load_models(self, config_path):
        try:
            self.available_models, self.loaded_models = _load_models(config_path, self.device)
            logger.info(f"成功加载 {len(self.loaded_models)} 个启动模型")
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}")
            self.available_models = {}
            self.loaded_models = {}

    def get_model_info(self):
        if not self.available_models:
            return []
        return [
            {**cfg.copy(), 'name': name, 'type': 'df'}
            for name, cfg in self.available_models.items()
        ]

    def check_requested_models(self, models):
        if not self.available_models:
            logger.warning("未加载模型配置")
            return

        for name in models:
            if name not in self.available_models:
                logger.warning(f"模型 {name} 不存在于配置中")
                continue
            if name not in self.loaded_models:
                try:
                    path = self.available_models[name]['full_path']
                    model = load_model(path, self.device)
                    if model:
                        self.loaded_models[name] = model
                        self.available_models[name]['is_loaded'] = True
                        logger.info(f"动态加载模型: {name}")
                    else:
                        logger.error(f"动态加载模型 {name} 失败")
                except Exception as e:
                    logger.error(f"加载模型 {name} 时出错: {str(e)}")

    def inpaint(self, image, mask, models, max_size=512):
        logger.info(f"开始处理修复请求，模型: {models}，尺寸: {max_size}")

        if not self.loaded_models:
            logger.error("模型配置未加载")
            raise ValueError("请先加载模型配置")

        req_models = [m.strip() for m in models.split(',') if m.strip()]
        if not req_models:
            logger.error("未指定请求的模型")
            raise ValueError("未指定请求的模型")

        self.check_requested_models(req_models)
        logger.info(f"已确认请求模型: {req_models}")

        try:
            # 读取图像和掩码
            image_pil = Image.open(image.file).convert('RGB')
            mask_pil = Image.open(mask.file).convert('L')
            logger.info(f"成功读取图像和掩码，原始尺寸: 图像{image_pil.size}, 掩码{mask_pil.size}")

            # 调整尺寸
            image_pil = image_pil.resize((max_size, max_size), Image.LANCZOS)
            mask_pil = mask_pil.resize((max_size, max_size), Image.LANCZOS)
            logger.info(f"调整后尺寸: {image_pil.size}")

            # 转换为张量
            image_tensor = ToTensor()(image_pil).unsqueeze(0).to(self.device)
            mask_tensor = ToTensor()(mask_pil).unsqueeze(0).to(self.device)

            # 二值化掩码：黑色区域(0)为修复区域，白色区域(1)为保留区域
            mask_tensor = (mask_tensor > 0.5).float()
            logger.info(f"图像张量形状: {image_tensor.shape}, 掩码张量形状: {mask_tensor.shape}")

            response_data = []
            for idx_model, model_name in enumerate(req_models):
                if model_name not in self.loaded_models:
                    logger.warning(f"模型 {model_name} 未加载，跳过处理")
                    continue

                logger.info(f"开始使用模型 {model_name} 进行推理")
                return_vals = self.available_models[model_name].get('return_vals', ['inpainted'])

                outputs = infer_deepfill(
                    self.loaded_models[model_name],
                    image_tensor,
                    mask_tensor,
                    return_vals=return_vals
                )
                logger.info(f"模型 {model_name} 推理完成，输出数量: {len(outputs)}")

                model_output_list = []
                for idx_out, output in enumerate(outputs):
                    # 确保输出是numpy数组且值在0-255范围内
                    if isinstance(output, torch.Tensor):
                        output = output.cpu().numpy()
                    if output.dtype != np.uint8:
                        output = (output * 255).astype(np.uint8)

                    # 如果是单通道，转换为RGB
                    if len(output.shape) == 2:
                        output = np.stack([output] * 3, axis=-1)
                    elif output.shape[0] == 3:  # CHW -> HWC
                        output = output.transpose(1, 2, 0)

                    filename = f"inpaint_{idx_model}_{idx_out}.png"
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    files_dir = os.path.join(current_dir, '..', 'files')
                    filepath = os.path.join(files_dir, filename)

                    # 保存图像
                    Image.fromarray(output).save(filepath)
                    logger.info(f"修复结果已保存至: {filepath}")

                    output_name = return_vals[idx_out] if idx_out < len(return_vals) else f'output_{idx_out}'
                    file_url = f'{self.host}/files/{filename}' if self.host else f'/files/{filename}'

                    model_output_list.append({
                        'name': output_name,
                        'file': file_url
                    })

                response_data.append({
                    'name': model_name,
                    'output': model_output_list
                })
                logger.info(f"模型 {model_name} 结果已添加到响应")

            logger.info(f"修复完成，生成 {len(response_data)} 个模型结果")
            return response_data

        except Exception as e:
            logger.error(f"图像修复过程出错: {str(e)}", exc_info=True)
            raise