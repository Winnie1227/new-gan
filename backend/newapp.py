from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import numpy as np
from PIL import Image
import io
import base64
# 假设你已有deepfillv2的模型加载和推理函数（需根据实际代码调整）
from model.inference import load_model, inpaint

app = FastAPI()

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定前端域名
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载模型（启动时加载一次即可）
model = load_model("pretrained/states_tf_places2.pth")  # 替换为你的模型权重路径


@app.post("/api/inpaint")
async def inpaint_image(image: UploadFile = File(...), mask: UploadFile = File(...)):
    try:
        # 读取并处理图像
        img_bytes = await image.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # 读取并处理掩码
        mask_bytes = await mask.read()
        mask = Image.open(io.BytesIO(mask_bytes)).convert("L")  # 灰度图，0表示背景，255表示待修复区域

        # 调用deepfillv2推理函数（需根据你的代码实现调整）
        result = inpaint(model, img, mask)

        # 将结果转换为Base64返回给前端
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"status": "success", "image": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))