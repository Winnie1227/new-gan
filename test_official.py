from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from PIL import Image
import numpy as np

# 初始化 RealESRGAN 模型
model = RRDBNet(
    num_in_ch=3,
    num_out_ch=3,
    num_feat=64,
    num_block=23,
    num_grow_ch=32,
    scale=4
)

upsampler = RealESRGANer(
    scale=4,
    model_path=r"D:\比赛\ican终稿\RealESRGAN_x4plus.pth",  # 替换为你的模型路径
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False,  # CPU 运行时必须设为 False
    device='cpu'  # 无 GPU 时用 'cpu'
)

# 1. 读取并转换为 NumPy 数组（RGB 格式）
img = Image.open("test_image.jpg").convert("RGB")
img_np = np.array(img)  # 形状：(H, W, 3)

# 2. RGB → BGR（RealESRGAN 通常期望 BGR 输入）
img_np = img_np[:, :, ::-1]

# 3. 确保数组内存连续（解决负步长问题）
img_np = np.ascontiguousarray(img_np)

# 4. 调用 enhance 修复（直接传入 NumPy 数组）
output, _ = upsampler.enhance(img_np, outscale=4)

# 5. 输出转换：BGR → RGB + 保存为 PIL Image
output_rgb = output[:, :, ::-1]  # BGR 转回 RGB
output_img = Image.fromarray(output_rgb)
output_img.save("official_test.png")

print("修复成功！结果已保存为 official_test.png")