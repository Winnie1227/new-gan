import axios from 'axios'

const request = axios.create({
  baseURL: '/api', // 与 vite.config.js 的代理前缀一致
  timeout: 120000 // 增加到2分钟，图像修复耗时较长
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    console.log(`发送请求: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    console.log(`收到响应: ${response.status} ${response.config.url}`)
    return response.data
  },
  (error) => {
    console.error('请求失败:', error)
    if (error.response) {
      console.error('响应数据:', error.response.data)
      console.error('响应状态:', error.response.status)
    }
    return Promise.reject(error)
  }
)

export default request
