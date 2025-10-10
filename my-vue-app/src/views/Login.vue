<template>
  <div class="login-page">
    <div class="center-wrapper">
      <div class="platform-title">文化遗产图像智能修复系统</div>
      <form class="login-container" @submit.prevent="handleLogin">
        <h2>用户登录</h2>
        <input 
          type="text" 
          v-model="username" 
          placeholder="请输入登录ID" 
          class="input" 
          required
        >
        <input 
          type="password" 
          v-model="password" 
          placeholder="请输入密码" 
          class="input" 
          required
        >
        <div class="options">
          <label><input type="checkbox" v-model="rememberPassword"> 记住密码</label>
          <a href="#" class="forgot">忘记密码？</a>
        </div>
        <button type="submit" class="login-btn" @click="handleRipple">登 录</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const rememberPassword = ref(false)

const handleLogin = async () => {
  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
    
    // 登录成功，跳转到主页面
    router.push('/dashboard')
  } catch (error) {
    alert('登录失败：' + error.message)
  }
}

const handleRipple = (e) => {
  const btn = e.currentTarget;
  const rect = btn.getBoundingClientRect();
  btn.style.setProperty('--x', `${e.clientX - rect.left}px`);
  btn.style.setProperty('--y', `${e.clientY - rect.top}px`);
}
</script>

<style scoped>
/* 登录页面容器 */
.login-page {
  margin: 0;
  padding: 0;
  height: 100vh;
  background: url('/images/login.jpg') no-repeat center center;
  background-size: cover;
  font-family: "Microsoft YaHei", sans-serif;
  position: relative;
}

.center-wrapper {
  position: absolute;
  top: 50%;
  right: 12%;
  transform: translateY(-50%);
}

.platform-title {
  text-align: center;
  font-size: 24px;
  color: #00ffff;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #00ffff;
}

.login-container {
  width: 300px;
  padding: 30px 30px 40px;
  background-color: rgba(0, 85, 170, 0.2);
  border: 2px solid #00bfff;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0,255,255,0.4);
  color: #ffffff;
}

.login-container h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #00ffff;
  font-size: 22px;
}

.input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: none;
  border-radius: 5px;
  background-color: rgba(255,255,255,0.1);
  color: white;
  font-size: 14px;
}

.input::placeholder {
  color: #a0dfff;
}

.options {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-bottom: 15px;
}

.options label {
  color: #a0dfff;
}

.forgot {
  color: #a0dfff;
  text-decoration: none;
}

.login-btn {
  width: 100%;
  padding: 10px;
  background-color: #00bfff;
  border: none;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: background 0.3s;
}

.login-btn:hover {
  background-color: #0099cc;
}

.login-btn::after {
  content: '';
  position: absolute;
  top: var(--y);
  left: var(--x);
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: ripple 0.6s ease-out;
}

@keyframes ripple {
  to {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}
</style>