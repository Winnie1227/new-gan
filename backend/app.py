import uvicorn
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import asyncio

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from utils.app_utils import Inpainter

# 初始化修复器
inpainter = Inpainter()

app = FastAPI(title="文化遗产图像修复系统")

# CORS配置 - 放宽限制
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 暂时允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保静态文件目录存在
files_dir = os.path.join(current_dir, 'files')
os.makedirs(files_dir, exist_ok=True)
app.mount('/files', StaticFiles(directory=files_dir), name='files')


@app.on_event("startup")
async def startup_event():
    """异步加载模型，避免阻塞事件循环"""
    try:
        # 使用绝对路径
        config_path = os.path.join(current_dir, 'models.yaml')
        print(f"尝试加载模型配置: {config_path}")

        # 在线程池中执行模型加载，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, inpainter.load_models, config_path)
        print("✅ 模型加载成功")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")


@app.get('/')
async def get_root():
    return {"message": "文化遗产图像修复系统API服务运行中", "status": "healthy"}


@app.get('/health')
async def health_check():
    return {"status": "healthy", "message": "服务运行正常"}


@app.get('/api/health')
async def api_health_check():
    model_status = "loaded" if inpainter.loaded_models else "failed"
    return {
        "status": "healthy",
        "message": "API服务正常",
        "model_status": model_status,
        "available_models": list(inpainter.available_models.keys()) if inpainter.available_models else []
    }


@app.post('/api/inpaint')
async def inpaint(
        image: UploadFile,
        mask: UploadFile,
        models: str = Form("pt_places2"),
        size: int = Form(512)
):
    try:
        print(f"收到修复请求: 模型={models}, 尺寸={size}, 文件={image.filename}")

        if not inpainter.loaded_models:
            raise HTTPException(status_code=503, detail="模型未加载，请检查模型配置")

        # 设置主机地址用于生成文件URL
        inpainter.set_host('http://127.0.0.1:8000')

        # 调用修复逻辑
        response_data = inpainter.inpaint(image, mask, models, size)

        print(f"修复完成，返回 {len(response_data)} 个模型结果")
        return response_data

    except Exception as e:
        print(f"修复过程出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图像修复失败: {str(e)}")


if __name__ == "__main__":
    print("🚀 启动文化遗产图像修复系统后端服务...")
    print(f"📁 当前工作目录: {current_dir}")
    print(f"🌐 服务地址: http://127.0.0.1:8000")
    print(f"🔧 健康检查: http://127.0.0.1:8000/health")

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,  # 关闭热重载，避免文件监视器问题
        log_level="debug",  # 改为debug级别查看更多日志
        access_log=True  # 启用访问日志
    )