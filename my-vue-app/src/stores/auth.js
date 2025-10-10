import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)

  const login = async (credentials) => {
    // 这里替换为实际的登录API调用
    // 模拟登录过程
    if (credentials.username && credentials.password) {
      user.value = {
        username: credentials.username,
        // 其他用户信息...
      }
      return Promise.resolve()
    } else {
      return Promise.reject(new Error('用户名或密码错误'))
    }
  }

  const logout = () => {
    user.value = null
  }

  return {
    user,
    isAuthenticated,
    login,
    logout
  }
})