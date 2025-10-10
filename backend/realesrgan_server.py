# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import io
import asyncio
import numpy as np
from PIL import Image

# 导入RealESRGAN模型
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

app = FastAPI(title="文化遗产图像修复系统")

# CORS配置 - 允许Vue开发服务器
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 添加Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------- 模型初始化 --------------------------
USE_GPU = False
DEVICE = "cuda" if USE_GPU else "cpu"
HALF_PRECISION = True if USE_GPU else False
MODEL_PATH = r"D:\比赛\ican终稿\RealESRGAN_x4plus.pth"

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

print("===== RealESRGAN 模型初始化完成 =====")

# -------------------------- API路由 --------------------------
@app.get("/")
async def root():
    return {"message": "文化遗产图像修复系统 API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "model_loaded": upsampler.model is not None,
        "device": DEVICE
    }

@app.post("/api/repair-image")
async def repair_image(file: UploadFile = File(...)):
    """图像修复接口"""
    try:
        # 检查文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="请上传图像文件")
        
        # 1. 读取上传图片
        img_pil = Image.open(io.BytesIO(await file.read())).convert('RGB')
        print(f"处理图片: {file.filename}, 尺寸: {img_pil.size}")

        # 2. 格式转换：PIL → BGR数组
        img_np_rgb = np.array(img_pil)
        img_np = img_np_rgb[:, :, ::-1]  # RGB转BGR
        img_np = np.ascontiguousarray(img_np)

        # 3. 调用Real-ESRGAN修复
        output_np, _ = await asyncio.to_thread(upsampler.enhance, img_np, outscale=4)

        # 4. 输出格式转换：BGR → RGB → PIL
        output_np_rgb = output_np[:, :, ::-1]  # BGR转RGB
        output_np_rgb = np.clip(output_np_rgb, 0, 255).astype(np.uint8)
        output_pil = Image.fromarray(output_np_rgb)

        # 5. 返回给前端
        buf = io.BytesIO()
        output_pil.save(buf, format='PNG')
        buf.seek(0)
        
        print(f"修复完成: {file.filename} → 输出尺寸: {output_pil.size}")
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        print(f"修复错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修复失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("启动 FastAPI 服务器...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")