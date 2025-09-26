from flask import Flask, render_template, request, redirect, url_for, send_file
import io
from PIL import Image, ImageFilter
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '123456':
        return redirect(url_for('index_page'))
    return "用户名或密码错误"

@app.route('/index')
def index_page():
    return render_template('index.html')

# 添加图像修复API接口
@app.route('/repair-image', methods=['POST'])
def repair_image():
    try:
        if 'file' not in request.files:
            return '没有文件', 400
        
        file = request.files['file']
        if file.filename == '':
            return '没有选择文件', 400
        
        # 读取图像
        image = Image.open(file.stream)
        
        # 简单的图像处理模拟修复（实际应替换为您的AI模型）
        # 这里使用高斯模糊模拟修复效果
        repaired_image = image.filter(ImageFilter.GaussianBlur(1))
        
        # 转换为RGB模式（避免PNG的RGBA问题）
        if repaired_image.mode != 'RGB':
            repaired_image = repaired_image.convert('RGB')
        
        # 保存到内存
        img_io = io.BytesIO()
        repaired_image.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
        
    except Exception as e:
        return f'处理失败: {str(e)}', 500

# 添加CORS支持（如果前端在不同端口）
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # 修改端口为8000以匹配前端调用