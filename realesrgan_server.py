from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import asyncio
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# 初始化FastAPI应用
app = FastAPI()

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------- 模型配置与初始化 --------------------------
USE_GPU = False  # 强制使用CPU调试（避免硬件问题干扰）
DEVICE = "cuda" if USE_GPU else "cpu"
HALF_PRECISION = True if USE_GPU else False  # CPU必须设为False
MODEL_PATH = r"D:\比赛\ican终稿\RealESRGAN_x4plus.pth"  # 模型路径

# 初始化模型
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path=MODEL_PATH,
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=HALF_PRECISION,
    device=DEVICE
)

# 初始化检查
print("===== 模型初始化信息 =====")
print(f"使用设备: {DEVICE}")
print(f"半精度计算: {HALF_PRECISION}")
print(f"模型路径: {MODEL_PATH}")
print(f"模型是否加载: {upsampler.model is not None}")  # 检查模型是否存在
print("==========================\n")

# -------------------------- 添加缺失的路由 --------------------------
@app.get("/")
async def root():
    """根路由"""
    return JSONResponse(content={
        "message": "RealESRGAN Image Enhancement Server is running",
        "status": "success",
        "endpoints": {
            "test": "/test (GET)",
            "repair_image": "/repair-image (POST)",
            "health": "/health (GET)"
        }
    })

@app.get("/test")
async def test_endpoint():
    """测试接口"""
    return JSONResponse(content={
        "status": "success", 
        "message": "服务器连接正常",
        "model_loaded": upsampler.model is not None
    })

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return JSONResponse(content={
        "status": "healthy",
        "model_loaded": upsampler.model is not None,
        "device": DEVICE
    })

# -------------------------- 图片修复接口 --------------------------
@app.post("/repair-image")
async def repair_image(file: UploadFile = File(...)):
    try:
        # 检查文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="请上传图像文件")
        
        # 1. 读取上传图片
        img_pil = Image.open(io.BytesIO(await file.read())).convert('RGB')
        print("\n===== 步骤1：读取上传图片 =====")
        print(f"图片尺寸 (宽x高): {img_pil.size}")
        print(f"图片模式: {img_pil.mode} (应为RGB)")

        # 2. 格式转换：PIL → BGR数组（模型输入格式）
        img_np_rgb = np.array(img_pil)  # RGB格式数组
        img_np = img_np_rgb[:, :, ::-1]  # 转为BGR
        img_np = np.ascontiguousarray(img_np)  # 确保内存连续
        print("\n===== 步骤2：输入格式转换检查 =====")
        print(f"原始RGB数组形状: {img_np_rgb.shape} (应为[H, W, 3])")
        print(f"转换后BGR数组形状: {img_np.shape} (应与原始一致)")
        print(f"数组是否连续: {img_np.flags['C_CONTIGUOUS']} (必须为True)")
        print(f"数组数据类型: {img_np.dtype} (应为uint8)")

        # 3. 调用Real-ESRGAN修复
        output_np, _ = await asyncio.to_thread(upsampler.enhance, img_np, outscale=4)
        print("\n===== 步骤3：模型增强结果检查 =====")
        print(f"输入数组大小: {img_np.nbytes / 1024:.1f} KB")
        print(f"输出数组形状: {output_np.shape} (应为[H*4, W*4, 3]左右)")
        print(f"输出数组大小: {output_np.nbytes / 1024:.1f} KB (应>10KB)")
        print(f"输出数据类型: {output_np.dtype}")

        # 4. 输出格式转换：BGR → RGB → PIL
        output_np_rgb = output_np[:, :, ::-1]  # BGR转RGB
        output_np_rgb = np.clip(output_np_rgb, 0, 255).astype(np.uint8)  # 确保数值范围正确
        output_pil = Image.fromarray(output_np_rgb)
        print("\n===== 步骤4：输出格式转换检查 =====")
        print(f"BGR转RGB后形状: {output_np_rgb.shape} (应与输出数组一致)")
        print(f"数值范围: [{output_np_rgb.min()}, {output_np_rgb.max()}] (应在0-255)")
        print(f"PIL图片是否有效: {output_pil is not None} (必须为True)")
        print(f"PIL图片尺寸: {output_pil.size if output_pil else '无效'}")

        # 5. 本地保存调试
        output_pil.save("backend_test.png")
        print("\n===== 调试信息 =====")
        print("修复结果已保存至: backend_test.png")

        # 6. 返回给前端
        buf = io.BytesIO()
        output_pil.save(buf, format='PNG')
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        error_msg = f"\n===== 错误信息 =====" \
                    f"\n发生异常: {str(e)}" \
                    f"\n==================="
        print(error_msg)
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "接口不存在", "path": request.url.path}
    )