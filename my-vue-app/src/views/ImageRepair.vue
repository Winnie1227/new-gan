<template>
  <div class="system-container">
    <div class="system-header">
      <div class="connection-status" :class="backendStatusClass">
        后端状态: {{ backendStatusText }}
      </div>
    </div>
    <div class="main-content">
      <!-- 原始图像与绘制区域 -->
      <div class="original-image-section">
        <div class="section-border">
          <!-- 上传/图像/画布区域 -->
          <div class="image-upload-area" v-if="!originalImageUrl">
            <div class="upload-prompt" @click="triggerFileInput">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>点击或拖放上传文物图像</p>
              <input
                type="file"
                accept="image/*"
                class="file-input"
                ref="fileInput"
                @change="handleImageUpload"
              >
            </div>
          </div>
          <div class="image-editor" v-else>
            <img
              :src="originalImageUrl"
              alt="待修复文物图像"
              class="original-image"
              @load="initCanvas"
              ref="originalImage"
            >
            <canvas
              ref="drawingCanvas"
              class="drawing-layer"
            ></canvas>
          </div>
          <!-- 工具栏 -->
          <div class="toolbar" v-if="originalImageUrl">
            <button
              class="tool-btn"
              :class="{ active: currentTool === 'brush' }"
              @click="setTool('brush')"
            >
              <i class="fas fa-paint-brush"></i> 画笔
            </button>
            <button
              class="tool-btn"
              :class="{ active: currentTool === 'eraser' }"
              @click="setTool('eraser')"
            >
              <i class="fas fa-eraser"></i> 橡皮擦
            </button>
            <button
              class="tool-btn"
              @click="clearDrawing"
            >
              <i class="fas fa-trash"></i> 清除
            </button>
            <div class="brush-size">
              <span class="brush-label">笔刷大小: {{ brushSize }}px</span>
              <input
                type="range"
                min="1"
                max="50"
                v-model="brushSize"
                class="size-slider"
              >
            </div>
            <!-- 模型选择 -->
            <div class="model-selector">
              <label>修复模型:</label>
              <select v-model="selectedModel" class="model-dropdown">
                <option value="pt_places2">Places2 (通用场景)</option>
                <option value="pt_celebahq">CelebA-HQ (人脸)</option>
              </select>
            </div>
            <!-- 尺寸选择 -->
            <div class="size-selector">
              <label>修复尺寸:</label>
              <select v-model="selectedSize" class="size-dropdown">
                <option value="256">256x256</option>
                <option value="512">512x512</option>
                <option value="768">768x768</option>
              </select>
            </div>
            <button
              class="repair-btn"
              @click="startRepair"
              :disabled="!hasDrawing || isLoading"
            >
              <i class="fas fa-magic" v-if="!isLoading"></i>
              <i class="fas fa-spinner fa-spin" v-else></i>
              {{ isLoading ? '修复中...' : '开始修复' }}
            </button>
          </div>
        </div>
      </div>
      <!-- 修复结果区域 -->
      <div class="results-section">
        <div class="section-title">
          <i class="fas fa-images"></i> 修复结果
        </div>
        <div class="results-grid">
          <div class="result-item">
            <div class="result-content">
              <img
                :src="originalImageUrl"
                alt="原始图像"
                class="result-image"
                v-if="originalImageUrl"
              >
              <div v-else class="no-result">
                <i class="fas fa-image"></i>
                <p>请先上传图像</p>
              </div>
            </div>
            <div class="result-label">
              <i class="fas fa-file-image"></i> 原图
            </div>
          </div>
          <div class="result-item">
            <div class="result-content">
              <img
                :src="repairResultUrl"
                alt="修复结果"
                class="result-image"
                v-if="repairResultUrl"
              >
              <div v-else class="no-result">
                <i class="fas fa-hourglass-half" v-if="isLoading"></i>
                <i class="fas fa-paint-brush" v-else-if="!hasDrawing"></i>
                <i class="fas fa-play-circle" v-else></i>
                <p v-if="!hasDrawing">请绘制掩码区域</p>
                <p v-else-if="isLoading">修复进行中...</p>
                <p v-else>点击"开始修复"查看结果</p>
              </div>
              <!-- 下载按钮添加文字提示（title属性） -->
              <button
                class="download-btn"
                @click="downloadResult"
                v-if="repairResultUrl"
                :disabled="isLoading"
                title="下载修复后的图像"
              >
                <i class="fas fa-download"></i> 下载结果
              </button>
            </div>
            <div class="result-label">
              <i class="fas fa-magic"></i> 修复图
            </div>
          </div>
        </div>
      </div>
      <!-- 操作说明 -->
      <div class="instructions-section">
        <div class="section-title">
          <i class="fas fa-info-circle"></i> 使用说明
        </div>
        <div class="instructions-content">
          <div class="instruction-item">
            <i class="fas fa-upload"></i>
            <span>上传需要修复的文物图像</span>
          </div>
          <div class="instruction-item">
            <i class="fas fa-paint-brush"></i>
            <span>使用画笔在图像上标记需要修复的区域（白色区域）</span>
          </div>
          <div class="instruction-item">
            <i class="fas fa-cog"></i>
            <span>选择合适的修复模型和尺寸</span>
          </div>
          <div class="instruction-item">
            <i class="fas fa-magic"></i>
            <span>点击"开始修复"按钮进行智能修复</span>
          </div>
          <div class="instruction-item">
            <i class="fas fa-download"></i>
            <span>修复完成后可下载结果图像</span>
          </div>
        </div>
      </div>
    </div>
    <!-- 加载中提示 -->
    <div class="loading-modal" v-if="isLoading">
      <div class="loading-content">
        <div class="spinner"></div>
        <p class="loading-text">{{ loadingMessage }}</p>
        <p class="loading-subtext">这可能需要几分钟时间，请耐心等待...</p>
      </div>
    </div>
    <!-- 调试面板 -->
    <div class="debug-panel" v-if="showDebug">
      <h3>调试信息</h3>
      <div class="debug-info">
        <p><strong>后端状态:</strong> {{ backendStatus }}</p>
        <p><strong>绘制状态:</strong> {{ hasDrawing ? '已绘制' : '未绘制' }}</p>
        <p><strong>当前工具:</strong> {{ currentTool }}</p>
        <p><strong>笔刷大小:</strong> {{ brushSize }}px</p>
        <p><strong>选择模型:</strong> {{ selectedModel }}</p>
        <p><strong>选择尺寸:</strong> {{ selectedSize }}</p>
        <p><strong>图像尺寸:</strong> {{ canvasSize.width }} x {{ canvasSize.height }}</p>
      </div>
      <button class="debug-toggle" @click="showDebug = !showDebug">
        {{ showDebug ? '隐藏调试' : '显示调试' }}
      </button>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, nextTick, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
// 后端API配置
const API_CONFIG = {
  baseUrl: 'http://127.0.0.1:8000',
  repairEndpoint: '/api/inpaint',
  healthEndpoint: '/health',
  timeout: 180000 // 3分钟超时
};
// 状态变量
const originalImage = ref(null);
const drawingCanvas = ref(null);
const fileInput = ref(null);
const originalImageUrl = ref('');
const repairResultUrl = ref('');
const selectedFile = ref(null);
const currentTool = ref('brush');
const brushSize = ref(15);
const isDrawing = ref(false);
const lastPos = ref({ x: 0, y: 0 });
const hasDrawing = ref(false);
const isLoading = ref(false);
const loadingMessage = ref('');
const backendStatus = ref('checking');
const backendStatusText = ref('检查连接中...');
const backendStatusClass = ref('checking');
const showDebug = ref(false);
const canvasSize = reactive({ width: 0, height: 0 });
const selectedModel = ref('pt_places2');
const selectedSize = ref('512');
// 检查后端连接
const checkBackendConnection = async () => {
  try {
    backendStatus.value = 'checking';
    backendStatusText.value = '检查连接中...';
    backendStatusClass.value = 'checking';
    console.log('正在检查后端连接...');
    const response = await axios.get(API_CONFIG.baseUrl + API_CONFIG.healthEndpoint, {
      timeout: 5000
    });
    if (response.data && response.data.status === 'healthy') {
      backendStatus.value = 'connected';
      backendStatusText.value = '已连接';
      backendStatusClass.value = 'connected';
      console.log('✅ 后端服务连接正常');
      return true;
    } else {
      throw new Error('后端服务响应异常');
    }
  } catch (error) {
    backendStatus.value = 'disconnected';
    backendStatusText.value = '未连接';
    backendStatusClass.value = 'disconnected';
    console.error('❌ 后端服务连接失败:', error.message);
    if (error.code === 'ECONNABORTED') {
      backendStatusText.value = '连接超时';
    } else if (error.response) {
      backendStatusText.value = `服务器错误: ${error.response.status}`;
    } else if (error.request) {
      backendStatusText.value = '无法连接到服务器';
    }
    return false;
  }
};
// 触发文件选择
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};
// 处理图片上传
const handleImageUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请上传有效的图片文件（JPEG、PNG等）');
      return;
    }
    // 验证文件大小（最大10MB）
    if (file.size > 10 * 1024 * 1024) {
      alert('图片文件大小不能超过10MB');
      return;
    }
    const reader = new FileReader();
    reader.onload = (event) => {
      originalImageUrl.value = event.target.result;
      selectedFile.value = file;
      hasDrawing.value = false;
      repairResultUrl.value = '';
      nextTick(() => {
        initCanvas();
      });
    };
    reader.onerror = () => {
      alert('文件读取失败，请重试或选择其他文件');
    };
    reader.readAsDataURL(file);
  }
};
// 初始化画布
const initCanvas = () => {
  if (!drawingCanvas.value || !originalImage.value) return;
  const canvas = drawingCanvas.value;
  const img = originalImage.value;
  
  // 设置画布尺寸与图片显示尺寸一致
  canvas.width = img.offsetWidth;
  canvas.height = img.offsetHeight;
  canvasSize.width = canvas.width;
  canvasSize.height = canvas.height;
  
  const ctx = canvas.getContext('2d');
  // 修改：初始化透明背景，而不是黑色
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // 设置绘制样式
  ctx.globalCompositeOperation = 'source-over';
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  
  bindCanvasEvents(canvas);
  console.log('画布初始化完成，尺寸:', canvas.width, 'x', canvas.height);
};
// 绑定画布事件
const bindCanvasEvents = (canvas) => {
  // 移除旧的事件监听器
  canvas.removeEventListener('mousedown', startDrawing);
  canvas.removeEventListener('mousemove', draw);
  canvas.removeEventListener('mouseup', stopDrawing);
  canvas.removeEventListener('mouseleave', stopDrawing);
  canvas.removeEventListener('touchstart', startDrawingTouch);
  canvas.removeEventListener('touchmove', drawTouch);
  canvas.removeEventListener('touchend', stopDrawing);
  // 添加新的事件监听器
  canvas.addEventListener('mousedown', startDrawing);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', stopDrawing);
  canvas.addEventListener('mouseleave', stopDrawing);
  canvas.addEventListener('touchstart', startDrawingTouch, { passive: false });
  canvas.addEventListener('touchmove', drawTouch, { passive: false });
  canvas.addEventListener('touchend', stopDrawing);
};
// 绘制逻辑
const startDrawing = (e) => {
  isDrawing.value = true;
  const pos = getCanvasCoordinates(e);
  lastPos.value = pos;
  drawPoint(pos.x, pos.y);
};
const startDrawingTouch = (e) => {
  e.preventDefault();
  if (e.touches.length === 0) return;
  const touch = e.touches[0];
  isDrawing.value = true;
  const pos = getTouchCoordinates(touch);
  lastPos.value = pos;
  drawPoint(pos.x, pos.y);
};
const draw = (e) => {
  if (!isDrawing.value) return;
  e.preventDefault();
  const pos = getCanvasCoordinates(e);
  drawLine(lastPos.value.x, lastPos.value.y, pos.x, pos.y);
  lastPos.value = pos;
};
const drawTouch = (e) => {
  e.preventDefault();
  if (!isDrawing.value || e.touches.length === 0) return;
  const touch = e.touches[0];
  const pos = getTouchCoordinates(touch);
  drawLine(lastPos.value.x, lastPos.value.y, pos.x, pos.y);
  lastPos.value = pos;
};
const stopDrawing = () => {
  if (isDrawing.value) {
    isDrawing.value = false;
  }
};
// 获取坐标
const getCanvasCoordinates = (e) => {
  if (!drawingCanvas.value) return { x: 0, y: 0 };
  const canvas = drawingCanvas.value;
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  };
};
const getTouchCoordinates = (touch) => {
  if (!drawingCanvas.value) return { x: 0, y: 0 };
  const canvas = drawingCanvas.value;
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (touch.clientX - rect.left) * scaleX,
    y: (touch.clientY - rect.top) * scaleY
  };
};
// 绘制点和线
// 绘制点和线 - 修改为半透明白色
const drawPoint = (x, y) => {
  if (!drawingCanvas.value) return;
  const ctx = drawingCanvas.value.getContext('2d');
  ctx.beginPath();
  ctx.arc(x, y, brushSize.value / 2, 0, Math.PI * 2);
  if (currentTool.value === 'brush') {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'; // 半透明白色
    ctx.fill();
    hasDrawing.value = true;
  } else {
    // 橡皮擦逻辑 - 清除绘制区域
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';
  }
};

const drawLine = (x1, y1, x2, y2) => {
  if (!drawingCanvas.value) return;
  const ctx = drawingCanvas.value.getContext('2d');
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.lineWidth = brushSize.value;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  if (currentTool.value === 'brush') {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)'; // 半透明白色
    ctx.stroke();
    hasDrawing.value = true;
  } else {
    // 橡皮擦逻辑 - 清除绘制区域
    ctx.globalCompositeOperation = 'destination-out';
    ctx.stroke();
    ctx.globalCompositeOperation = 'source-over';
  }
};
// 工具切换
const setTool = (tool) => {
  currentTool.value = tool;
  console.log('切换工具:', tool);
};
// 清除绘制
// 清除绘制
const clearDrawing = () => {
  if (drawingCanvas.value) {
    const ctx = drawingCanvas.value.getContext('2d');
    // 修改：清除画布为透明，而不是黑色
    ctx.clearRect(0, 0, drawingCanvas.value.width, drawingCanvas.value.height);
    hasDrawing.value = false;
    console.log('清除画布');
  }
};
// 开始修复
const startRepair = async () => {
  if (!selectedFile.value || !hasDrawing.value || isLoading.value) return;
  // 检查后端连接
  const isBackendConnected = await checkBackendConnection();
  if (!isBackendConnected) {
    alert('❌ 后端服务未启动！\n\n请确保：\n1. 后端服务运行在 http://127.0.0.1:8000\n2. 已安装所有必需的Python依赖\n3. 端口8000未被占用');
    return;
  }
  try {
    isLoading.value = true;
    loadingMessage.value = '正在准备修复数据...';
    const canvas = drawingCanvas.value;
    const ctx = canvas.getContext('2d');
    // 优化掩码处理 - 使用渐变阈值让边缘更柔和
    loadingMessage.value = '正在优化掩码...';
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    

    // 创建新的掩码canvas
    const maskCanvas = document.createElement('canvas');
    maskCanvas.width = canvas.width;
    maskCanvas.height = canvas.height;
    const maskCtx = maskCanvas.getContext('2d');
    
    // 将绘制区域转换为黑白掩码
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      const a = data[i + 3]; // 透明度
      
      // 如果有绘制内容（alpha > 0），则设为白色（需要修复）
      // 否则设为黑色（保留原图）
      const value = a > 10 ? 255 : 0; // 阈值处理
      
      const pixelIndex = (i / 4) * 4;
      data[i] = value;     // R
      data[i + 1] = value; // G
      data[i + 2] = value; // B
      data[i + 3] = 255;   // A - 完全不透明
    }
    
    maskCtx.putImageData(imageData, 0, 0);
    
    // 生成掩码 blob
    loadingMessage.value = '正在生成掩码文件...';
    const maskBlob = await new Promise((resolve) => {
      maskCanvas.toBlob((blob) => {
        if (!blob) {
          console.error('无法生成掩码Blob');
          resolve(null);
        } else {
          resolve(blob);
        }
      }, 'image/png');
    });
    if (!maskBlob) {
      throw new Error('无法生成掩码图像');
    }
    const formData = new FormData();
    formData.append('image', selectedFile.value);
    formData.append('mask', maskBlob, 'mask.png');
    formData.append('models', selectedModel.value); // 使用选择的模型
    formData.append('size', selectedSize.value); // 使用选择的尺寸
    loadingMessage.value = '正在发送修复请求...';
    console.log('开始发送修复请求到后端...');
    console.log('使用模型:', selectedModel.value);
    console.log('使用尺寸:', selectedSize.value);
    const response = await axios.post(API_CONFIG.baseUrl + API_CONFIG.repairEndpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      timeout: API_CONFIG.timeout,
    });
    console.log("✅ 后端响应数据：", response.data);
    loadingMessage.value = '正在处理修复结果...';
    // 处理响应数据
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      const firstModel = response.data[0];
      if (firstModel.output && Array.isArray(firstModel.output) && firstModel.output.length > 0) {
        const firstOutput = firstModel.output[0];
        if (firstOutput.file) {
          let fileUrl = firstOutput.file;
          // 处理文件路径
          if (fileUrl.startsWith('/files/')) {
            fileUrl = API_CONFIG.baseUrl + fileUrl;
          } else if (!fileUrl.startsWith('http')) {
            fileUrl = API_CONFIG.baseUrl + '/files/' + fileUrl;
          }
          // 添加时间戳避免缓存
          repairResultUrl.value = fileUrl + '?t=' + Date.now();
          console.log('✅ 修复结果URL:', repairResultUrl.value);
        } else {
          throw new Error('修复结果文件路径不存在');
        }
      } else {
        throw new Error('修复结果输出为空');
      }
    } else {
      throw new Error('修复结果结构异常');
    }
    isLoading.value = false;
    loadingMessage.value = '';
    backendStatus.value = '修复完成';
    backendStatusText.value = '修复完成';
    backendStatusClass.value = 'connected';
    console.log('🎉 图像修复完成！');
  } catch (error) {
    isLoading.value = false;
    loadingMessage.value = '';
    console.error('❌ 修复失败详情:', error);
    let errorMessage = '修复失败：';
    if (error.code === 'ECONNABORTED') {
      errorMessage = '⏰ 请求超时，修复过程耗时较长，请稍后重试';
    } else if (error.response) {
      errorMessage = `❌ 服务器返回 ${error.response.status} 错误`;
      if (error.response.data?.detail) {
        errorMessage += ` - ${error.response.data.detail}`;
      } else if (error.response.data?.message) {
        errorMessage += ` - ${error.response.data.message}`;
      }
    } else if (error.request) {
      errorMessage = '🔌 无法连接到后端服务器！\n\n请检查：\n• 后端服务是否启动\n• 端口8000是否被占用\n• 防火墙设置\n• 网络连接';
    } else {
      errorMessage = `❌ ${error.message}`;
    }
    alert(errorMessage);
    backendStatus.value = '修复失败';
    backendStatusText.value = '修复失败';
    backendStatusClass.value = 'disconnected';
  }
};
// 下载修复结果
const downloadResult = async () => {
  if (!repairResultUrl.value || isLoading.value) return;
  
  try {
    loadingMessage.value = '正在准备下载...';
    isLoading.value = true;
    
    console.log('开始下载修复结果:', repairResultUrl.value);
    
    // 方法1: 使用 fetch 获取图片并创建下载链接
    const response = await fetch(repairResultUrl.value);
    if (!response.ok) {
      throw new Error(`下载失败: ${response.status} ${response.statusText}`);
    }
    
    const blob = await response.blob();
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    
    // 设置下载文件名
    const timestamp = new Date().getTime();
    link.download = `数字建筑遗产图像智能修复_${timestamp}.png`;
    
    // 添加到DOM并触发点击
    document.body.appendChild(link);
    link.click();
    
    // 清理
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    console.log('✅ 下载成功');
    
    // 显示下载成功提示
    setTimeout(() => {
      alert('下载成功！文件已保存到您的下载文件夹。');
    }, 500);
    
  } catch (error) {
    console.error('下载失败:', error);
    // 这里可以添加错误处理，比如显示错误提示
    alert('下载失败，请重试或联系管理员。');
  } finally {
    isLoading.value = false;
    loadingMessage.value = '';
  }
};
// 组件挂载时检查后端状态
onMounted(async () => {
  console.log('🖼️ 图像修复页面已加载');
  await checkBackendConnection();
  
  // 在组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(intervalId);
    if (drawingCanvas.value) {
      const canvas = drawingCanvas.value;
      canvas.removeEventListener('mousedown', startDrawing);
      canvas.removeEventListener('mousemove', draw);
      canvas.removeEventListener('mouseup', stopDrawing);
      canvas.removeEventListener('mouseleave', stopDrawing);
      canvas.removeEventListener('touchstart', startDrawingTouch);
      canvas.removeEventListener('touchmove', drawTouch);
      canvas.removeEventListener('touchend', stopDrawing);
    }
  });
});
</script>

<style scoped>
/* ========== 粒子背景层 ========== */
.particles-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

/* ========== 整体容器 - 透明背景 ========== */
.system-container {
  background: transparent;  /* 关键：透明背景 */
  color: #ffffff;
  min-height: 100vh;
  font-family: 'Microsoft YaHei', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 0;
  font-size: 14px;
  position: relative;
  /* 底部留出距离，避免与页脚重叠 */
  padding-bottom: 80px;
}

/* ========== 后端状态标识 - 固定在右上角 ========== */
.connection-status {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.connection-status.connected {
  background: rgba(0, 255, 136, 0.9);
  color: #000000;
  border: 1px solid #00cc66;
}

.connection-status.disconnected {
  background: rgba(255, 68, 68, 0.9);
  color: #ffffff;
  border: 1px solid #cc0000;
}

.connection-status.checking {
  background: rgba(255, 170, 0, 0.9);
  color: #000000;
  border: 1px solid #cc8800;
}

/* ========== 主内容区 - 顶部留出距离给状态标识 ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 20px 30px; /* 顶部60px给状态标识留空间 */
}

/* ========== 上传区域 - 半透明背景 ========== */
.original-image-section {
  margin-bottom: 25px;
}

.section-border {
  border: 1px solid rgba(0, 240, 255, 0.4);
  border-radius: 10px;
  background: rgba(16, 32, 64, 0.5);  /* 半透明，让背景图透过来 */
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);  /* 毛玻璃效果 */
}

.image-upload-area {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 280px;
  padding: 30px;
}

.upload-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #00ffff;
  padding: 50px 70px;
  border: 2px dashed rgba(0, 255, 255, 0.5);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 255, 255, 0.1);  /* 半透明 */
  backdrop-filter: blur(5px);
}

.upload-prompt:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 255, 255, 0.3);
}

.upload-prompt i {
  font-size: 40px;
  margin-bottom: 15px;
  color: #00ffff;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
}

.upload-prompt p {
  margin: 0;
  font-size: 16px;
  color: #ffffff;
  font-weight: 500;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);  /* 文字阴影增强可读性 */
}

.file-input {
  display: none;
}

/* ========== 图像编辑区 - 半透明 ========== */
.image-editor {
  position: relative;
  min-height: 380px;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);  /* 更透明 */
  margin: 15px;
  border-radius: 8px;
  backdrop-filter: blur(3px);
}

.original-image {
  max-width: 100%;
  max-height: 450px;
  border: 2px solid rgba(0, 240, 255, 0.5);
  border-radius: 6px;
  display: block;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.drawing-layer {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: crosshair;
  border: 2px dashed rgba(255, 255, 255, 0.5);
  background: transparent;
  border-radius: 6px;
  mix-blend-mode: normal;
}

/* ========== 工具栏 - 半透明 ========== */
.toolbar {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: rgba(10, 25, 47, 0.7);  /* 半透明 */
  border-top: 1px solid rgba(0, 240, 255, 0.3);
  gap: 12px;
  flex-wrap: wrap;
  backdrop-filter: blur(5px);
}

.tool-btn {
  background: rgba(0, 240, 255, 0.2);
  border: 1px solid rgba(0, 240, 255, 0.4);
  color: #00ffff;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tool-btn:hover {
  background: rgba(0, 240, 255, 0.35);
  border-color: #00ffff;
  color: #ffffff;
}

.tool-btn.active {
  background: #00ffff;
  color: #000000;
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
}

.brush-size {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #00ffff;
  font-size: 14px;
  font-weight: 500;
  background: rgba(0, 240, 255, 0.15);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid rgba(0, 240, 255, 0.25);
}

.brush-label {
  white-space: nowrap;
  color: #ffffff;
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
}

.size-slider {
  width: 100px;
  accent-color: #00ffff;
}

.model-selector, .size-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #00ffff;
  font-size: 14px;
  font-weight: 500;
  background: rgba(0, 240, 255, 0.15);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid rgba(0, 240, 255, 0.25);
}

.model-selector label, .size-selector label {
  color: #ffffff;
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
}

.model-dropdown, .size-dropdown {
  background: rgba(16, 32, 64, 0.8);
  border: 1px solid rgba(0, 240, 255, 0.4);
  color: #00ffff;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.repair-btn {
  margin-left: auto;
  background: linear-gradient(135deg, #00ff66, #00cc44);
  border: none;
  color: #000000;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 255, 102, 0.4);
}

.repair-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 102, 0.6);
}

.repair-btn:disabled {
  background: rgba(102, 102, 102, 0.7);
  color: #aaaaaa;
  cursor: not-allowed;
  box-shadow: none;
}

/* ========== 结果区域 - 半透明背景 ========== */
.results-section {
  margin-bottom: 25px;
}

.section-title {
  border-bottom: 2px solid rgba(0, 240, 255, 0.4);
  padding-bottom: 12px;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00ffff;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.result-item {
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 10px;
  background: rgba(16, 32, 64, 0.4);  /* 更透明 */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  backdrop-filter: blur(5px);
}

.result-item:hover {
  border-color: rgba(0, 240, 255, 0.6);
  background: rgba(16, 32, 64, 0.6);
  box-shadow: 0 8px 25px rgba(0, 240, 255, 0.3);
}

.result-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  background: rgba(0, 0, 0, 0.1);  /* 几乎透明 */
}

.result-image {
  max-width: 100%;
  max-height: 350px;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.result-label {
  background: rgba(0, 240, 255, 0.15);
  color: #00ffff;
  padding: 12px;
  text-align: center;
  border-top: 1px solid rgba(0, 240, 255, 0.3);
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

.no-result {
  color: #ffffff;
  text-align: center;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.no-result i {
  font-size: 40px;
  color: #00ffff;
  opacity: 0.9;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
}

.no-result p {
  margin: 0;
  font-size: 15px;
  color: #ffffff;
  font-weight: 500;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
}

.download-btn {
  background: linear-gradient(135deg, #00f0ff, #0099ff);
  border: none;
  color: #000000;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 15px;
  font-weight: 700;
  font-size: 14px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6);
}

/* ========== 使用说明 - 半透明 ========== */
.instructions-section {
  margin-bottom: 25px;
}

.instructions-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.instruction-item {
  background: rgba(16, 32, 64, 0.4);  /* 更透明 */
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #ffffff;
  transition: all 0.3s;
  backdrop-filter: blur(3px);
}

.instruction-item:hover {
  border-color: rgba(0, 240, 255, 0.6);
  background: rgba(16, 32, 64, 0.6);
  transform: translateX(5px);
}

.instruction-item i {
  color: #00ffff;
  font-size: 20px;
  width: 24px;
  text-align: center;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.6);
}

.instruction-item span {
  color: #ffffff;
  font-weight: 500;
  line-height: 1.4;
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
}

/* ========== 加载模态框 ========== */
.loading-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(5, 20, 39, 0.9);  /* 稍微透明，能看到背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.loading-content {
  text-align: center;
  color: #00ffff;
  background: rgba(10, 25, 47, 0.9);
  padding: 40px;
  border-radius: 10px;
  border: 2px solid rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.4);
  backdrop-filter: blur(10px);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 255, 255, 0.3);
  border-top: 4px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin: 0 0 10px 0;
  font-size: 20px;
  font-weight: 700;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.loading-subtext {
  margin: 0;
  font-size: 14px;
  color: #ffffff;
  opacity: 0.9;
}

/* ========== 调试面板 ========== */
.debug-panel {
  position: fixed;
  bottom: 15px;
  right: 15px;
  background: rgba(0, 0, 0, 0.85);
  border: 1px solid #00ffff;
  border-radius: 8px;
  padding: 12px;
  color: #00ffff;
  font-size: 12px;
  max-width: 280px;
  z-index: 100;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  margin-bottom: 60px;
  backdrop-filter: blur(5px);
}

.debug-panel h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #00ffff;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  padding-bottom: 5px;
}

.debug-info p {
  margin: 5px 0;
  color: #ffffff;
  font-family: 'Courier New', monospace;
  font-size: 11px;
}

.debug-info strong {
  color: #00ffff;
}

.debug-toggle {
  background: rgba(0, 255, 255, 0.2);
  border: 1px solid #00ffff;
  color: #00ffff;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  margin-top: 10px;
  transition: all 0.2s;
}

.debug-toggle:hover {
  background: rgba(0, 255, 255, 0.3);
  color: #ffffff;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .system-container {
    padding-bottom: 60px;
  }
  
  .connection-status {
    top: 10px;
    right: 10px;
    padding: 4px 8px;
    font-size: 11px;
  }
  
  .main-content {
    padding: 50px 15px 20px;
  }
  
  .image-upload-area {
    min-height: 220px;
    padding: 20px;
  }
  
  .upload-prompt {
    padding: 35px 45px;
  }
  
  .upload-prompt i {
    font-size: 32px;
  }
  
  .image-editor {
    min-height: 280px;
    padding: 15px;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .result-content {
    min-height: 220px;
    padding: 15px;
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
    padding: 12px 15px;
  }
  
  .repair-btn {
    margin-left: 0;
    justify-content: center;
    width: 100%;
  }
  
  .instructions-content {
    grid-template-columns: 1fr;
  }
  
  .debug-panel {
    margin-bottom: 50px;
    max-width: 200px;
  }
}
</style>