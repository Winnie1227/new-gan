<template>
  <div class="tab-panel" id="panel-1">
    <div class="tech-title">
      <div class="tech-title-inner">
        <span class="tech-title-text">图像修复中心</span>
        <div class="tech-title-decoration"></div>
      </div>
    </div>
    
    <div class="upload-container">
      <!-- 单图上传区域 -->
      <div class="upload-section">
        <div class="sci-fi-corner top-left"></div>
        <div class="sci-fi-corner top-right"></div>
        <div class="sci-fi-corner bottom-left"></div>
        <div class="sci-fi-corner bottom-right"></div>
        <h3><i class="fas fa-image"></i> 单图修复</h3>
        <div 
          class="upload-area" 
          @dragover.prevent="handleDragOver"
          @dragleave="handleDragLeave"
          @drop="handleSingleDrop"
        >
          <div class="upload-icon">
            <i class="fas fa-cloud-upload-alt"></i>
          </div>
          <div class="upload-text">
            <p>拖放图像文件到此处或</p>
            <div class="upload-button-wrap">
              <button type="button" class="upload-button" @click="triggerSingleFileInput">
                选择文件
              </button>
              <input 
                type="file" 
                ref="singleFileInput"
                accept="image/*" 
                class="file-overlay-input"
                @change="handleSingleFileSelect"
                style="display: none;"
              >
            </div>
          </div>
          <div class="upload-preview" v-if="singlePreviewUrl">
            <img :src="singlePreviewUrl" alt="预览图像" style="max-width: 100%; border-radius: 8px;">
          </div>
        </div>
        <div class="upload-status" :class="`status-${singleStatus.type}`">
          {{ singleStatus.message }}
        </div>
      </div>
      
      <!-- 批量上传区域 -->
      <div class="upload-section">
        <h3><i class="fas fa-images"></i> 批量修复</h3>
        <div 
          class="upload-area"
          @dragover.prevent="handleDragOver"
          @dragleave="handleDragLeave" 
          @drop="handleBatchDrop"
        >
          <div class="upload-icon">
            <i class="fas fa-folder-open"></i>
          </div>
          <div class="upload-text">
            <p>拖放ZIP文件或多张图像或</p>
            <div class="upload-button-wrap">
              <button type="button" class="upload-button" @click="triggerBatchFileInput">
                选择文件
              </button>
              <input 
                type="file" 
                ref="batchFileInput"
                accept=".zip,image/*" 
                class="file-overlay-input"
                @change="handleBatchFileSelect"
                multiple
                style="display: none;"
              >
            </div>
          </div>
          <div class="file-list" v-if="batchFiles.length > 0">
            <div v-for="(file, index) in batchFiles" :key="index" class="file-item">
              <span>{{ file.name }}</span>
              <span class="file-status">
                <i v-if="file.status === 'processing'" class="fas fa-spinner fa-spin"></i>
                <i v-else-if="file.status === 'success'" class="fas fa-check" style="color: #10b981;"></i>
                <i v-else-if="file.status === 'error'" class="fas fa-times" style="color: #ef4444;"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="upload-status" :class="`status-${batchStatus.type}`">
          {{ batchStatus.message }}
        </div>
        <div class="progress-container" v-show="batchProgress.show">
          <div class="progress-bar" :style="{ width: batchProgress.percentage + '%' }"></div>
          <div class="progress-text">{{ batchProgress.percentage }}%</div>
        </div>
      </div>
    </div>

    <!-- 修复结果展示区 -->
    <div class="result-container" v-show="results.length > 0">
      <h3><i class="fas fa-tasks"></i> 修复结果</h3>
      <div class="result-actions">
        <button class="action-button" @click="downloadAllResults">
          <i class="fas fa-download"></i> 全部下载
        </button>
        <button class="action-button" @click="clearAllResults">
          <i class="fas fa-trash-alt"></i> 清空结果
        </button>
      </div>
      <div class="result-grid">
        <div v-for="(result, index) in results" :key="index" class="result-item">
          <div class="result-image">
            <img :src="result.imageUrl" :alt="'修复结果: ' + result.fileName">
          </div>
          <div class="result-info">
            <span class="result-name">{{ result.fileName }}</span>
-           <span class="result-size">{{ formatFileSize(result.fileSize) }}</span>
          </div>
          <div class="result-actions">
            <button class="view-btn" @click="viewImage(result.imageUrl)">
              <i class="fas fa-search"></i>
            </button>
            <button class="download-btn" @click="downloadSingleImage(result.imageUrl, result.fileName)">
              <i class="fas fa-download"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片查看模态框 -->
    <div v-if="showImageModal" class="image-modal" @click="closeImageModal">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeImageModal">&times;</span>
        <img :src="currentImageUrl" alt="查看图像">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// 响应式数据
const singleFileInput = ref(null)
const batchFileInput = ref(null)
const singlePreviewUrl = ref('')
const showImageModal = ref(false)
const currentImageUrl = ref('')

// 单图上传状态
const singleStatus = reactive({
  message: '',
  type: 'info' // info, success, error, warning
})

// 批量上传状态
const batchStatus = reactive({
  message: '',
  type: 'info'
})

// 批量文件列表
const batchFiles = ref([])

// 批量进度
const batchProgress = reactive({
  show: false,
  percentage: 0
})

// 修复结果
const results = ref([])

// 方法定义
const triggerSingleFileInput = () => {
  singleFileInput.value?.click()
}

const triggerBatchFileInput = () => {
  batchFileInput.value?.click()
}

const handleDragOver = (event) => {
  event.currentTarget.style.borderColor = '#4fc3f7'
  event.currentTarget.style.backgroundColor = 'rgba(79, 195, 247, 0.1)'
}

const handleDragLeave = (event) => {
  event.currentTarget.style.borderColor = '#475569'
  event.currentTarget.style.backgroundColor = 'transparent'
}

const handleSingleDrop = (event) => {
  event.preventDefault()
  handleDragLeave(event)
  
  const files = event.dataTransfer.files
  if (files.length > 0) {
    handleSingleUpload(files[0])
  }
}

const handleBatchDrop = (event) => {
  event.preventDefault()
  handleDragLeave(event)
  
  const files = Array.from(event.dataTransfer.files)
  if (files.length > 0) {
    handleBatchUpload(files)
  }
}

const handleSingleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    handleSingleUpload(file)
  }
}

const handleBatchFileSelect = (event) => {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    handleBatchUpload(files)
  }
}

const handleSingleUpload = async (file) => {
  if (!file.type.match('image.*')) {
    updateStatus(singleStatus, '请上传有效的图像文件', 'error')
    return
  }

  // 显示预览
  const reader = new FileReader()
  reader.onload = (e) => {
    singlePreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)

  updateStatus(singleStatus, '正在上传并修复图像...', 'info')

  try {
    const formData = new FormData()
    formData.append('file', file)

    // 直接调用 realesrgan_server.py
    const response = await fetch('http://127.0.0.1:8000/api/repair-image', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error(`修复失败: ${response.status}`)
    }

    const blob = await response.blob()
    
    if (blob.size === 0) {
      throw new Error('返回的图片为空')
    }

    const enhancedImageUrl = URL.createObjectURL(blob)
    
    // 添加到结果列表
    addToResults(enhancedImageUrl, file.name, blob.size)
    updateStatus(singleStatus, '✅ 图像修复完成！', 'success')

  } catch (error) {
    console.error('修复错误:', error)
    updateStatus(singleStatus, '❌ 修复失败: ' + error.message, 'error')
  }
}

const handleBatchUpload = async (files) => {
  // 过滤图像文件
  const imageFiles = files.filter(file => file.type.match('image.*'))
  
  if (imageFiles.length === 0) {
    updateStatus(batchStatus, '请选择有效的图像文件', 'error')
    return
  }

  // 初始化文件列表
  batchFiles.value = imageFiles.map(file => ({
    file,
    name: file.name,
    status: 'pending' // pending, processing, success, error
  }))

  batchProgress.show = true
  batchProgress.percentage = 0
  updateStatus(batchStatus, '正在处理文件...', 'info')

  let processedCount = 0

  for (let i = 0; i < batchFiles.value.length; i++) {
    batchFiles.value[i].status = 'processing'
    
    try {
      const formData = new FormData()
      formData.append('file', batchFiles.value[i].file)

      // 调用后端
      const response = await fetch('http://127.0.0.1:8000/api/repair-image', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('修复失败')
      }

      const blob = await response.blob()
      const imageUrl = URL.createObjectURL(blob)
      
      batchFiles.value[i].status = 'success'
      addToResults(imageUrl, batchFiles.value[i].name, blob.size)
      
    } catch (error) {
      batchFiles.value[i].status = 'error'
      console.error(`文件 ${batchFiles.value[i].name} 处理失败:`, error)
    }

    processedCount++
    batchProgress.percentage = Math.round((processedCount / batchFiles.value.length) * 100)
  }

  updateStatus(batchStatus, '所有文件处理完成', 'success')
  
  // 3秒后隐藏进度条
  setTimeout(() => {
    batchProgress.show = false
  }, 3000)
}

const addToResults = (imageUrl, fileName, fileSize) => {
  console.log('Adding result:', imageUrl, fileName, fileSize);
  results.value.push({
    imageUrl,
    fileName,
    fileSize
  })
}

const downloadSingleImage = (imageUrl, fileName) => {
  const link = document.createElement('a')
  const baseName = fileName.replace(/\.[^/.]+$/, "")
  link.download = `${baseName}_修复结果.png`
  link.href = imageUrl
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const downloadAllResults = async () => {
  if (results.value.length === 0) {
    updateStatus(singleStatus, '没有可下载的修复结果', 'warning')
    return
  }

  try {
    // 这里可以添加ZIP打包下载逻辑
    results.value.forEach((result, index) => {
      setTimeout(() => {
        downloadSingleImage(result.imageUrl, result.fileName)
      }, index * 300)
    })
  } catch (error) {
    console.error('下载失败:', error)
    updateStatus(singleStatus, '下载失败: ' + error.message, 'error')
  }
}

const clearAllResults = () => {
  if (confirm('确定要清空所有修复结果吗？')) {
    results.value = []
    singlePreviewUrl.value = ''
    batchFiles.value = []
    batchProgress.percentage = 0
    batchProgress.show = false
    updateStatus(singleStatus, '已清空所有修复结果', 'info')
    updateStatus(batchStatus, '', 'info')
  }
}

const viewImage = (imageUrl) => {
  currentImageUrl.value = imageUrl
  showImageModal.value = true
}

const closeImageModal = () => {
  showImageModal.value = false
  currentImageUrl.value = ''
}

const updateStatus = (statusObj, message, type) => {
  statusObj.message = message
  statusObj.type = type
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// 组件挂载后的初始化
onMounted(() => {
  console.log('图像修复组件已加载')
})
</script>

<style scoped>
/* 主面板容器样式 */
.tab-panel {
  padding: 20px;                    /* 内边距 */
  max-width: 1200px;                /* 最大宽度限制 */
  margin: 0 auto;                   /* 水平居中 */
  color: black !important;         /* 黑色文字，强制覆盖 */
  min-height: 500px;                /* 最小高度 */
  display: block;                   /* 块级显示 */
  opacity: 1;                       /* 完全不透明 */
  visibility: visible;              /* 可见 */
}

/* 科技感标题容器 */
.tech-title {
  text-align: center;               /* 文字居中 */
  margin-bottom: 60px;              /* 底部外边距 */
  position: relative;               /* 相对定位 */
  perspective: 1000px;              /* 3D透视效果 */
  padding-top: 15rem; /* 向下移动 */
}

/* 标题内部容器 */
.tech-title-inner {
  display: inline-block;            /* 行内块显示 */
  position: relative;               /* 相对定位 */
  padding: 0 0.5rem;                /* 左右内边距 */
}

/* 主标题文字样式 */
.tech-title-text {
  font-size: 8rem;               /* 字体大小 */
  color: #00d8ff;                   /* 科技蓝颜色 */
  text-transform: uppercase;        /* 大写字母 */
  letter-spacing: 1rem;          /* 字母间距 */
  text-shadow: 0 0 0.5rem rgba(0, 216, 255, 0.7);  /* 文字发光效果 */
  position: relative;               /* 相对定位 */
  z-index: 2;                       /* 层级 */
  background: linear-gradient(to right, #00d8ff, #00f5d4);  /* 渐变背景 */
  background-clip: text;            /* 背景裁剪到文字 */
  -webkit-background-clip: text;    /* Safari兼容 */
  -webkit-text-fill-color: transparent;  /* 文字透明，显示渐变背景 */
  font-weight: bold;                /* 粗体 */
  animation: textGlow 3s infinite alternate;  /* 文字发光动画 */
}

/* 标题装饰线 */
.tech-title-decoration {
  position: absolute;               /* 绝对定位 */
  bottom: -3rem;                  /* 定位在标题下方 */
  left: 0;                          /* 左对齐 */
  right: 0;                         /* 右对齐 */
  height: 0.5rem;                  /* 线条高度 */
  background: linear-gradient(90deg, transparent, #00d8ff, transparent);  /* 渐变线条 */
  z-index: 1;                       /* 层级 */
}

/* 装饰线两端的菱形装饰 */
.tech-title-decoration::before,
.tech-title-decoration::after {
  content: "";                      /* 伪元素内容 */
  position: absolute;               /* 绝对定位 */
  top: 50%;                         /* 垂直居中 */
  width: 1.5rem;                   /* 宽度 */
  height: 1.5rem;                  /* 高度 */
  border: 2px solid #00d8ff;        /* 边框 */
  transform: translateY(-50%) rotate(45deg);  /* 居中并旋转45度成菱形 */
  animation: borderPulse 2s infinite;  /* 边框脉动动画 */
}

/* 左侧菱形 */
.tech-title-decoration::before {
  left: -1rem;                    /* 定位在左侧 */
}

/* 右侧菱形 */
.tech-title-decoration::after {
  right: -1rem;                   /* 定位在右侧 */
}

/* 文字发光动画 */
@keyframes textGlow {
  0% { text-shadow: 0 0 0.5rem rgba(0, 216, 255, 0.7); }  /* 初始发光 */
  100% { text-shadow: 0 0 1rem rgba(0, 216, 255, 0.9), 
                    0 0 1.5rem rgba(0, 216, 255, 0.5); }  /* 增强发光 */
}

/* 边框脉动动画 */
@keyframes borderPulse {
  0% { opacity: 0.3; transform: translateY(-50%) rotate(45deg) scale(0.8); }  /* 缩小淡出 */
  50% { opacity: 1; transform: translateY(-50%) rotate(45deg) scale(1.1); }   /* 放大显示 */
  100% { opacity: 0.3; transform: translateY(-50%) rotate(45deg) scale(0.8); }  /* 恢复原状 */
}

/* 上传区域网格容器 */
.upload-container {
  display: grid;                    /* 网格布局 */
  grid-template-columns: 1fr 1fr;   /* 两列等宽 */
  gap: 30px;                        /* 列间距 */
  margin-bottom: 40px;              /* 底部外边距 */
}

/* 单个上传区块 */
.upload-section {
  background: rgba(2, 22, 45, 0.6);  /* 半透明深蓝背景 */
  border: 1px solid #217093;        /* 边框 */
  border-radius: 12px;              /* 圆角 */
  padding: 25px;                    /* 内边距 */
  position: relative;               /* 相对定位 */
  overflow: hidden;                 /* 溢出隐藏 */
  transition: all 0.3s ease;        /* 过渡动画 */
  box-shadow: 0 0 15px rgba(0, 216, 255, 0.3);  /* 发光阴影 */
}

/* 上传区块悬停效果 */
.upload-section:hover {
  border-color: #4fc3f7;            /* 边框颜色变化 */
  box-shadow: 0 0 20px rgba(79, 195, 247, 0.2);  /* 阴影增强 */
  transform: translateY(-5px);      /* 上移效果 */
}

/* 科幻风格边角装饰 */
.sci-fi-corner {
  position: absolute;               /* 绝对定位 */
  width: 20px;                      /* 宽度 */
  height: 20px;                     /* 高度 */
  border: 2px solid #4fc3f7;        /* 边框 */
  opacity: 0.6;                     /* 半透明 */
}

/* 左上角装饰 */
.top-left {
  top: 10px;                        /* 顶部定位 */
  left: 10px;                       /* 左侧定位 */
  border-right: none;               /* 去掉右边框 */
  border-bottom: none;              /* 去掉下边框 */
}

/* 右上角装饰 */
.top-right {
  top: 10px;                        /* 顶部定位 */
  right: 10px;                      /* 右侧定位 */
  border-left: none;                /* 去掉左边框 */
  border-bottom: none;              /* 去掉下边框 */
}

/* 左下角装饰 */
.bottom-left {
  bottom: 10px;                     /* 底部定位 */
  left: 10px;                       /* 左侧定位 */
  border-right: none;               /* 去掉右边框 */
  border-top: none;                 /* 去掉上边框 */
}

/* 右下角装饰 */
.bottom-right {
  bottom: 10px;                     /* 底部定位 */
  right: 10px;                      /* 右侧定位 */
  border-left: none;                /* 去掉左边框 */
  border-top: none;                 /* 去掉上边框 */
}

/* 上传区块标题 */
.upload-section h3 {
  color: #00d8ff;                   /* 科技蓝颜色 */
  font-size: 5rem;               /* 字体大小 */
  margin-bottom: 20px;              /* 底部外边距 */
  text-shadow: 0 0 0.1rem rgba(0, 216, 255, 0.3);  /* 文字阴影 */
  display: flex;                    /* 弹性布局 */
  align-items: center;              /* 垂直居中 */
  gap: 10px;                        /* 元素间距 */
}

/* 标题图标颜色 */
.upload-section h3 i {
  color: #00f5d4;                   /* 青绿色 */
}

/* 上传区域主体 */
.upload-area {
  border: 2px dashed #0b3d66;       /* 虚线边框 */
  border-radius: 8px;               /* 圆角 */
  padding: 30px;                    /* 内边距 */
  text-align: center;               /* 文字居中 */
  transition: all 0.3s;             /* 过渡动画 */
  min-height: 200px;                /* 最小高度 */
  display: flex;                    /* 弹性布局 */
  flex-direction: column;           /* 垂直方向 */
  justify-content: center;          /* 垂直居中 */
  align-items: center;              /* 水平居中 */
  background: rgba(11, 61, 102, 0.3);  /* 半透明背景 */
  position: relative;               /* 相对定位 */
}

/* 上传区域悬停效果 */
.upload-area:hover {
  border-color: #00d8ff;            /* 边框颜色变化 */
  background: rgba(11, 61, 102, 0.5);  /* 背景加深 */
}

/* 上传图标 */
.upload-icon {
  font-size: 48px;                  /* 图标大小 */
  color: #00d8ff;                   /* 图标颜色 */
  margin-bottom: 15px;              /* 底部外边距 */
  opacity: 0.7;                     /* 半透明 */
}

/* 上传文字区域 */
.upload-text {
  color: #a0d7ff;                   /* 浅蓝色文字 */
  font-size: 16px;                  /* 字体大小 */
  margin-bottom: 15px;              /* 底部外边距 */
}

/* 上传文字段落 */
.upload-text p {
  margin-bottom: 10px;              /* 底部外边距 */
  color: #d0e8ff;                   /* 更亮的蓝色 */
  font-size: 16px;                  /* 字体大小 */
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.3);  /* 文字阴影 */
}

/* 上传按钮容器 */
.upload-button-wrap {
  margin-top: 10px;                 /* 顶部外边距 */
}

/* 上传按钮样式 */
.upload-button {
  position: relative;               /* 相对定位 */
  overflow: hidden;                 /* 溢出隐藏 */
  padding: 12px 30px;               /* 内边距 */
  background: linear-gradient(45deg, #01cfff, #0066ff);  /* 渐变背景 */
  border: none;                     /* 无边框 */
  border-radius: 25px;              /* 圆角 */
  color: white;                     /* 白色文字 */
  font-size: 16px;                  /* 字体大小 */
  cursor: pointer;                  /* 手型光标 */
  transition: all 0.3s;             /* 过渡动画 */
  box-shadow: 0 0 10px rgba(0, 168, 255, 0.5);  /* 发光阴影 */
  z-index: 1;                       /* 层级 */
}

/* 按钮流光效果 */
.upload-button::before {
  content: "";                      /* 伪元素内容 */
  position: absolute;               /* 绝对定位 */
  top: 0;                           /* 顶部对齐 */
  left: -100%;                      /* 初始位置在左侧外 */
  width: 100%;                      /* 全宽 */
  height: 100%;                     /* 全高 */
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);  /* 渐变流光 */
  transition: 0.5s;                 /* 过渡时间 */
  z-index: -1;                      /* 在按钮背景下方 */
}

/* 按钮悬停时流光效果 */
.upload-button:hover::before {
  left: 100%;                       /* 流光移动到右侧 */
}

/* 按钮悬停效果 */
.upload-button:hover {
  box-shadow: 0 0 20px rgba(0, 216, 255, 0.8);  /* 阴影增强 */
  transform: translateY(-2px);      /* 上移效果 */
}

/* 隐藏的文件输入框 */
.file-overlay-input {
  position: absolute;               /* 绝对定位 */
  opacity: 0;                       /* 完全透明 */
  cursor: pointer;                  /* 手型光标 */
}

/* 图片预览区域 */
.upload-preview {
  margin-top: 20px;                 /* 顶部外边距 */
  max-width: 100%;                  /* 最大宽度 */
}

/* 预览图片样式 */
.upload-preview img {
  max-width: 100%;                  /* 最大宽度 */
  max-height: 200px;                /* 最大高度 */
  border: 1px solid #0b3d66;        /* 边框 */
  border-radius: 8px;               /* 圆角 */
  box-shadow: 0 0 15px rgba(0, 216, 255, 0.3);  /* 发光阴影 */
  transition: all 0.3s;             /* 过渡动画 */
}

/* 预览图片悬停效果 */
.upload-preview img:hover {
  transform: scale(1.02);           /* 轻微放大 */
  box-shadow: 0 0 25px rgba(0, 216, 255, 0.5);  /* 阴影增强 */
}

/* 文件列表容器 */
.file-list {
  margin-top: 15px;                 /* 顶部外边距 */
  max-height: 150px;                /* 最大高度 */
  overflow-y: auto;                 /* 垂直滚动 */
  width: 100%;                      /* 全宽 */
}

/* 单个文件项 */
.file-item {
  display: flex;                    /* 弹性布局 */
  align-items: center;              /* 垂直居中 */
  justify-content: space-between;   /* 两端对齐 */
  padding: 10px;                    /* 内边距 */
  background: rgba(11, 61, 102, 0.3);  /* 半透明背景 */
  border-radius: 5px;               /* 圆角 */
  margin-bottom: 5px;               /* 底部外边距 */
  font-size: 14px;                  /* 字体大小 */
  color: #a0d7ff;                   /* 文字颜色 */
  border-left: 3px solid #00d8ff;   /* 左侧边框 */
  transition: all 0.3s;             /* 过渡动画 */
}

/* 文件项悬停效果 */
.file-item:hover {
  background: rgba(11, 61, 102, 0.5);  /* 背景加深 */
  transform: translateX(5px);       /* 右移效果 */
}

/* 文件状态图标 */
.file-status {
  font-size: 14px;                  /* 字体大小 */
}

/* 上传状态提示 */
.upload-status {
  margin-top: 15px;                 /* 顶部外边距 */
  font-size: 14px;                  /* 字体大小 */
  min-height: 20px;                 /* 最小高度 */
  padding: 5px 10px;                /* 内边距 */
  border-radius: 4px;               /* 圆角 */
  text-align: center;               /* 文字居中 */
}

/* 信息状态样式 */
.status-info {
  color: #00d8ff;                   /* 科技蓝 */
  text-shadow: 0 0 5px rgba(0, 216, 255, 0.5);  /* 发光效果 */
}

/* 成功状态样式 */
.status-success {
  color: #00ff88;                   /* 绿色 */
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.5);  /* 发光效果 */
}

/* 错误状态样式 */
.status-error {
  color: #ff4d4d;                   /* 红色 */
  text-shadow: 0 0 5px rgba(255, 77, 77, 0.5);  /* 发光效果 */
}

/* 警告状态样式 */
.status-warning {
  color: #ffcc00;                   /* 黄色 */
  text-shadow: 0 0 5px rgba(255, 204, 0, 0.5);  /* 发光效果 */
}

/* 进度条容器 */
.progress-container {
  margin-top: 15px;                 /* 顶部外边距 */
  height: 25px;                     /* 高度 */
  background: rgba(11, 61, 102, 0.5);  /* 背景色 */
  border-radius: 10px;              /* 圆角 */
  position: relative;               /* 相对定位 */
  overflow: hidden;                 /* 溢出隐藏 */
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.3);  /* 内阴影 */
}

/* 进度条 */
.progress-bar {
  height: 100%;                     /* 全高 */
  background: linear-gradient(90deg, #01cfff, #0066ff);  /* 渐变背景 */
  border-radius: 10px;              /* 圆角 */
  transition: width 0.3s;           /* 宽度过渡动画 */
  position: relative;               /* 相对定位 */
  overflow: hidden;                 /* 溢出隐藏 */
}

/* 进度条流光效果 */
.progress-bar::after {
  content: "";                      /* 伪元素内容 */
  position: absolute;               /* 绝对定位 */
  top: 0;                           /* 顶部对齐 */
  left: 0;                          /* 左侧对齐 */
  right: 0;                         /* 右侧对齐 */
  bottom: 0;                        /* 底部对齐 */
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);  /* 渐变流光 */
  animation: progressShine 2s infinite;  /* 流光动画 */
}

/* 进度文字 */
.progress-text {
  position: absolute;               /* 绝对定位 */
  top: 0;                           /* 顶部对齐 */
  left: 0;                          /* 左侧对齐 */
  width: 100%;                      /* 全宽 */
  text-align: center;               /* 文字居中 */
  color: white;                     /* 白色文字 */
  font-size: 12px;                  /* 字体大小 */
  line-height: 25px;                /* 行高 */
  font-weight: bold;                /* 粗体 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);  /* 文字阴影 */
}

/* 结果展示容器 */
.result-container {
  margin-top: 30px;                 /* 顶部外边距 */
  background: rgba(2, 22, 45, 0.6);  /* 半透明背景 */
  border: 1px solid #217093;       /* 边框 */
  border-radius: 12px;              /* 圆角 */
  padding: 25px;                   /* 内边距 */
  box-shadow: 0 0 15px rgba(0, 216, 255, 0.2) inset;  /* 内发光阴影 */
  z-index: 10;
  display: block ;
}

/* 结果标题 */
.result-container h3 {
  color: #00d8ff;                   /* 科技蓝 */
  font-size: 5rem;               /* 字体大小 */
  margin-bottom: 20px;              /* 底部外边距 */
  text-shadow: 0 0 0.1rem rgba(0, 216, 255, 0.3);  /* 文字阴影 */
  display: flex;                    /* 弹性布局 */
  align-items: center;              /* 垂直居中 */
  gap: 10px;                        /* 元素间距 */
}

/* 结果操作按钮区域 */
.result-actions {
  display: flex;                    /* 弹性布局 */
  gap: 15px;                        /* 按钮间距 */
  margin-bottom: 20px;              /* 底部外边距 */
}

/* 操作按钮样式 */
.action-button {
  padding: 10px 20px;               /* 内边距 */
  background: rgba(0, 168, 255, 0.2);  /* 半透明背景 */
  border: 1px solid #00a8ff;        /* 边框 */
  border-radius: 20px;              /* 圆角 */
  color: #00d8ff;                   /* 文字颜色 */
  font-size: 14px;                  /* 字体大小 */
  cursor: pointer;                  /* 手型光标 */
  transition: all 0.3s;             /* 过渡动画 */
  display: flex;                    /* 弹性布局 */
  align-items: center;              /* 垂直居中 */
  gap: 8px;                         /* 图标文字间距 */
}

/* 操作按钮悬停效果 */
.action-button:hover {
  background: rgba(0, 168, 255, 0.3);  /* 背景加深 */
  box-shadow: 0 0 15px rgba(0, 216, 255, 0.3);  /* 发光阴影 */
  transform: translateY(-2px);      /* 上移效果 */
}

/* 结果网格布局 */
.result-grid {
  display: grid;                    /* 网格布局 */
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));  /* 自适应列 */
  gap: 20px;                        /* 网格间距 */
}

/* 单个结果项 */
.result-item {
  background: rgba(11, 61, 102, 0.3);  /* 半透明背景 */
  border: 1px solid #0b3d66;        /* 边框 */
  border-radius: 8px;               /* 圆角 */
  padding: 10px;                    /* 内边距 */
  position: relative;               /* 相对定位 */
  overflow: hidden;                 /* 溢出隐藏 */
  transition: all 0.3s ease;        /* 过渡动画 */
  transform-style: preserve-3d;     /* 3D变换保持 */
  perspective: 1000px;              /* 透视效果 */
  height: auto; 
}

/* 结果项悬停效果 */
.result-item:hover {
  transform: translateY(-5px) rotateX(5deg);  /* 上移并3D旋转 */
  box-shadow: 0 10px 25px rgba(0, 216, 255, 0.3);  /* 阴影增强 */
  border-color: #00d8ff;            /* 边框颜色变化 */
}

/* 结果项顶部装饰线 */
.result-item::after {
  content: "";                      /* 伪元素内容 */
  position: absolute;               /* 绝对定位 */
  top: 0;                           /* 顶部对齐 */
  left: 0;                          /* 左侧对齐 */
  right: 0;                         /* 右侧对齐 */
  height: 2px;                      /* 线条高度 */
  background: linear-gradient(90deg, transparent, #00d8ff, transparent);  /* 渐变线条 */
  opacity: 0;                       /* 初始透明 */
  transition: opacity 0.3s;         /* 透明度过渡 */
}

/* 悬停时显示装饰线 */
.result-item:hover::after {
  opacity: 1;                       /* 显示线条 */
}

/* 结果图片容器 */
.result-image {
  margin-bottom: 10px;              /* 底部外边距 */
}

/* 结果图片 */
.result-image img {
  width: 100%;                      /* 全宽 */
  height: auto;                     /* 高度自适应 */
  border-radius: 6px;               /* 圆角 */
  border: 1px solid #0b3d66;        /* 边框 */
  transition: all 0.3s;             /* 过渡动画 */
}

/* 结果图片悬停效果 */
.result-item:hover .result-image img {
  transform: scale(1.05);           /* 轻微放大 */
  box-shadow: 0 5px 15px rgba(0, 216, 255, 0.2);  /* 发光阴影 */
}

/* 结果信息区域 */
.result-info {
  display: flex;                    /* 弹性布局 */
  flex-direction: column;           /* 垂直方向 */
  gap: 5px;                         /* 元素间距 */
  margin-bottom: 10px;              /* 底部外边距 */
}

/* 结果文件名 */
.result-name {
  color: #ffffff;                   /* 白色文字 */
  font-size: 14px;                  /* 字体大小 */
  font-weight: bold;                /* 粗体 */
  white-space: nowrap;              /* 不换行 */
  overflow: hidden;                 /* 溢出隐藏 */
  text-overflow: ellipsis;          /* 省略号 */
}

/* 结果文件大小 */
.result-size {
  color: #80c0ff;                   /* 浅蓝色 */
  font-size: 12px;                  /* 较小字体 */
}

/* 结果项操作按钮区域 */
.result-actions {
  display: flex;                    /* 弹性布局 */
  gap: 8px;                         /* 按钮间距 */
  justify-content: center;          /* 水平居中 */
}

/* 查看和下载按钮 */
.view-btn, .download-btn {
  padding: 8px 12px;                /* 内边距 */
  background: rgba(0, 168, 255, 0.2);  /* 半透明背景 */
  border: 1px solid #00a8ff;        /* 边框 */
  border-radius: 6px;               /* 圆角 */
  color: #00d8ff;                   /* 文字颜色 */
  cursor: pointer;                  /* 手型光标 */
  transition: all 0.3s;             /* 过渡动画 */
  display: flex;                    /* 弹性布局 */
  align-items: center;              /* 垂直居中 */
  justify-content: center;          /* 水平居中 */
}

/* 查看和下载按钮悬停效果 */
.view-btn:hover, .download-btn:hover {
  background: rgba(0, 168, 255, 0.3);  /* 背景加深 */
  transform: translateY(-2px);      /* 上移效果 */
  box-shadow: 0 5px 10px rgba(0, 216, 255, 0.2);  /* 发光阴影 */
}

/* 图片查看模态框 */
.image-modal {
  position: fixed;                  /* 固定定位 */
  top: 0;                           /* 顶部对齐 */
  left: 0;                          /* 左侧对齐 */
  width: 100%;                      /* 全宽 */
  height: 100%;                     /* 全高 */
  background: rgba(0, 0, 0, 0.8);   /* 半透明黑色背景 */
  display: flex;                    /* 弹性布局 */
  justify-content: center;          /* 水平居中 */
  align-items: center;              /* 垂直居中 */
  z-index: 1000;                    /* 高层级 */
  animation: modalFadeIn 0.3s ease-out;  /* 淡入动画 */
}

/* 模态框内容 */
.modal-content {
  position: relative;               /* 相对定位 */
  max-width: 90%;                   /* 最大宽度 */
  max-height: 90%;                  /* 最大高度 */
  background: rgba(2, 22, 45, 0.95);  /* 半透明深蓝背景 */
  border: 2px solid #00d8ff;        /* 边框 */
  border-radius: 12px;              /* 圆角 */
  padding: 20px;                    /* 内边距 */
  box-shadow: 0 0 30px rgba(0, 216, 255, 0.5);  /* 发光阴影 */
}

/* 模态框图片 */
.modal-content img {
  max-width: 100%;                  /* 最大宽度 */
  max-height: 80vh;                 /* 最大高度 */
  border-radius: 8px;               /* 圆角 */
}

/* 关闭按钮 */
.close {
  position: absolute;               /* 绝对定位 */
  top: 10px;                        /* 顶部定位 */
  right: 15px;                      /* 右侧定位 */
  font-size: 30px;                  /* 字体大小 */
  color: #00d8ff;                   /* 科技蓝 */
  cursor: pointer;                  /* 手型光标 */
  transition: all 0.3s;             /* 过渡动画 */
  z-index: 1001;                    /* 最高层级 */
}

/* 关闭按钮悬停效果 */
.close:hover {
  color: #ff4d4d;                   /* 红色 */
  transform: scale(1.2);            /* 放大效果 */
}

/* 进度条流光动画 */
@keyframes progressShine {
  0% { transform: translateX(-100%); }  /* 从左侧开始 */
  100% { transform: translateX(100%); }  /* 移动到右侧 */
}

/* 模态框淡入动画 */
@keyframes modalFadeIn {
  from { opacity: 0; }              /* 初始透明 */
  to { opacity: 1; }                /* 最终不透明 */
}

/* 响应式设计 - 移动端适配 */
@media (max-width: 768px) {
  .upload-container {
    grid-template-columns: 1fr;     /* 单列布局 */
    gap: 20px;                      /* 间距调整 */
  }
  
  .result-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));  /* 更小的网格 */
    gap: 15px;                      /* 间距调整 */
  }
  
  .modal-content {
    max-width: 95%;                 /* 更大宽度 */
    padding: 15px;                  /* 内边距调整 */
  }
  
  .tech-title-text {
    font-size: 0.24rem;             /* 字体缩小 */
  }
}

/* 加载旋转动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }   /* 初始角度 */
  100% { transform: rotate(360deg); }  /* 旋转一圈 */
}

/* Font Awesome 旋转类 */
.fa-spin {
  animation: spin 1s linear infinite;  /* 无限旋转 */
}
</style>