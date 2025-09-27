from flask import Flask, render_template, request, redirect, url_for, send_file
import io
from PIL import Image, ImageFilter
import os
import requests 
import logging
import socket
logging.basicConfig(level=logging.DEBUG)

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

@app.route('/repair-image', methods=['POST'])
def repair_image():
    try:
        print("=== 开始处理图像修复请求 ===")
        
        if 'file' not in request.files:
            return '没有文件', 400
        
        file = request.files['file']
        if file.filename == '':
            return '没有选择文件', 400
        
        print(f"接收文件: {file.filename}, 大小: {request.content_length} bytes")
        
        # 检查文件大小，如果太大则拒绝
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if request.content_length and request.content_length > MAX_SIZE:
            return '文件太大，请选择小于10MB的图片', 400
        
        # 读取文件内容
        file_data = file.read()
        print(f"实际文件大小: {len(file_data)} 字节")
        
        if len(file_data) == 0:
            return '文件为空', 400
        
        # 重新创建文件流
        file_stream = io.BytesIO(file_data)
        files = {'file': (file.filename, file_stream, file.content_type)}
        
        print("正在转发到 RealESRGAN 服务...")
        
        # 大幅增加超时时间，并分阶段超时
        try:
            response = requests.post(
                'http://127.0.0.1:8001/repair-image',
                files=files,
                timeout=(10.0, 300.0)  # 读取超时300秒（5分钟）
            )
            
            print(f"RealESRGAN 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"修复成功，返回数据大小: {len(response.content)} 字节")
                return send_file(
                    io.BytesIO(response.content), 
                    mimetype='image/png'
                )
            else:
                error_msg = f'RealESRGAN 服务错误: {response.status_code}'
                print(error_msg)
                return error_msg, response.status_code
                
        except requests.exceptions.Timeout as e:
            print(f"超时详情: {e}")
            return '图像处理时间过长，请尝试较小的图片或稍后重试', 500
            
    except Exception as e:
        error_msg = f'处理失败: {str(e)}'
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg, 500
    
@app.route('/debug-test')
def debug_test():
    """调试测试页面"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>调试测试</title>
    </head>
    <body>
        <h1>图像修复调试测试</h1>
        
        <h2>1. 测试服务连通性</h2>
        <button onclick="testConnection()">测试连通性</button>
        <div id="connection-result"></div>
        
        <h2>2. 测试文件上传</h2>
        <input type="file" id="testFile">
        <button onclick="testUpload()">测试上传</button>
        <div id="upload-result"></div>
        
        <h2>3. 测试图像修复</h2>
        <input type="file" id="repairFile" accept="image/*">
        <button onclick="testRepair()">测试修复</button>
        <div id="repair-result"></div>
        <img id="resultImage" style="max-width: 300px; display: none;">
        
        <script>
            async function testConnection() {
                try {
                    const response = await fetch('/test-connection');
                    const data = await response.json();
                    document.getElementById('connection-result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('connection-result').innerHTML = 
                        '错误: ' + error.message;
                }
            }
            
            async function testUpload() {
                const fileInput = document.getElementById('testFile');
                if (!fileInput.files[0]) {
                    alert('请选择文件');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                try {
                    const response = await fetch('/test-upload', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    document.getElementById('upload-result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('upload-result').innerHTML = 
                        '错误: ' + error.message;
                }
            }
            
            async function testRepair() {
                const fileInput = document.getElementById('repairFile');
                if (!fileInput.files[0]) {
                    alert('请选择图像文件');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                try {
                    const response = await fetch('/repair-image', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
                        document.getElementById('resultImage').src = url;
                        document.getElementById('resultImage').style.display = 'block';
                        document.getElementById('repair-result').innerHTML = 
                            '修复成功！图像大小: ' + blob.size + ' 字节';
                    } else {
                        const errorText = await response.text();
                        document.getElementById('repair-result').innerHTML = 
                            '错误: ' + response.status + ' - ' + errorText;
                    }
                } catch (error) {
                    document.getElementById('repair-result').innerHTML = 
                        '请求错误: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    '''

# 添加CORS支持（如果前端在不同端口）
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def test_connection():
    """测试到127.0.0.1:8001的连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 8001))
        sock.close()
        return result == 0  # 0表示连接成功
    except:
        return False

# 在应用启动时测试
print("=== 网络连接测试 ===")
print(f"能否连接到 127.0.0.1:8001: {test_connection()}")

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # 修改端口为8000以匹配前端调用