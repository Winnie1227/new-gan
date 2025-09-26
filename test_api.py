import requests

# 后端接口地址（必须与启动的地址一致）
api_url = "http://localhost:8000/repair-image"
# 本地测试图片路径（选一张模糊/低清图，修复效果更明显）
test_img_path = "test_image.jpg"

# 发送请求给后端
with open(test_img_path, "rb") as f:
    files = {"file": (test_img_path, f, "image/jpeg")}  # 上传图片
    response = requests.post(api_url, files=files)

# 检查结果
if response.status_code == 200:
    # 保存后端返回的修复图
    with open("test_backend_output.png", "wb") as f:
        f.write(response.content)
    print(f"✅ 后端修复成功！结果已保存为 test_backend_output.png")
    print(f"📊 修复图大小：{len(response.content) / 1024:.1f} KB（正常应>10KB）")
else:
    # 打印后端返回的错误信息（关键调试依据）
    print(f"❌ 后端修复失败！状态码：{response.status_code}")
    print(f"错误详情：{response.json()}")