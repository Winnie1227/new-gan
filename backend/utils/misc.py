import cv2
import numpy as np
import torch
from torchvision import transforms


def output_to_img(tensor):
    """将模型输出的张量转换为图像格式"""
    img = tensor.squeeze(0).cpu().numpy().transpose(1, 2, 0)  # 移除batch维度并转置
    img = (img + 1.) / 2. * 255.  # 将[-1,1]范围转回[0,255]
    img = img.astype(np.uint8)
    return img


@torch.no_grad()
def infer_deepfill(generator, image, mask, return_vals=['inpainted', 'stage1']):
    """模型推理核心函数（确保所有逻辑在函数内部）"""
    # 1. 打印掩码信息（调试用）
    print(f"掩码有效像素数: {mask.sum().item()}")
    print(f"掩码 min: {mask.min().item()}, max: {mask.max().item()}")

    # 2. 解析图像维度（4维：batch, channel, height, width）
    batch_size, channels, h, w = image.shape
    grid = 8

    # 3. 调整图像尺寸以适应模型（确保能被8整除）
    image = image[:, :3, :h // grid * grid, :w // grid * grid]
    mask = mask[:, 0:1, :h // grid * grid, :w // grid * grid]

    # 4. 图像预处理（归一化到[-1,1]）
    image = (image * 2 - 1.)  # 映射到[-1,1]范围
    mask = (mask > 0.).to(dtype=torch.float32)  # 二值化掩码（1表示需要修复）

    # 5. 准备模型输入（拼接图像、掩码等信息）
    image_masked = image * (1. - mask)  # 掩盖原始图像中的待修复区域
    ones_x = torch.ones_like(image_masked)[:, 0:1, :, :]  # 生成全1的草图通道
    x = torch.cat([image_masked, ones_x, ones_x * mask], dim=1)  # 拼接输入通道

    # 6. 模型推理（双阶段生成）
    x_stage1, x_stage2 = generator(x, mask)
    image_compl = image * (1. - mask) + x_stage2 * mask  # 合并修复结果

    # 7. 调试：保存输入/输出图像到本地（仅在函数内部执行）
    input_img = output_to_img(image)
    output_img = output_to_img(image_compl)
    cv2.imwrite("app/files/input_debug.png", input_img[:, :, ::-1])  # 转BGR保存
    cv2.imwrite("app/files/output_debug.png", output_img[:, :, ::-1])
    cv2.imwrite("app/files/mask_debug.png", mask.squeeze(0).squeeze(0).cpu().numpy() * 255)

    # 8. 整理输出结果
    output = []
    for return_val in return_vals:
        if return_val.lower() == 'stage1':
            output.append(output_to_img(x_stage1))
        elif return_val.lower() == 'stage2':
            output.append(output_to_img(x_stage2))
        elif return_val.lower() == 'inpainted':
            output.append(output_to_img(image_compl))
        else:
            print(f'Invalid return value: {return_val}')

    return output
