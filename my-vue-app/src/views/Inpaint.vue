<template>
  <div class="inpaint-page">
    <div class="upload-area">
      <input type="file" @change="handleImageUpload" accept="image/*" />
      <input type="file" @change="handleMaskUpload" accept="image/*" />
      <button @click="inpaintImage">开始图像修复</button>
    </div>
    <div class="result-area" v-if="resultUrl">
      <h3>修复结果</h3>
      <img :src="resultUrl" alt="修复后的图像" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../utils/request'

const imageFile = ref(null)
const maskFile = ref(null)
const resultUrl = ref('')

const handleImageUpload = (e) => {
  imageFile.value = e.target.files[0]
}

const handleMaskUpload = (e) => {
  maskFile.value = e.target.files[0]
}

const inpaintImage = async () => {
  if (!imageFile.value || !maskFile.value) {
    alert('请选择图像和掩码文件')
    return
  }

  const formData = new FormData()
  formData.append('image', imageFile.value)
  formData.append('mask', maskFile.value)

  try {
    // 调用后端 deepfillv2 的 /api/inpaint 接口（代理后实际地址是 http://127.0.0.1:8000/inpaint）
    const res = await request.post('/inpaint', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (res.status === 'success') {
      resultUrl.value = res.image // 后端返回的 Base64 图像地址
    }
  } catch (error) {
    alert('修复失败，请检查后端服务是否启动')
    console.error(error)
  }
}
</script>

<style scoped>
.inpaint-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.upload-area {
  margin-bottom: 20px;
}
input, button {
  margin: 8px 0;
}
.result-area img {
  max-width: 100%;
  height: auto;
}
</style>