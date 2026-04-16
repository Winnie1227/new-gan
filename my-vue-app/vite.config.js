import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // 开发服务器配置
  server: {
    port: 8080, // 自定义开发服务器端口（默认5173）
    open: true, // 启动时自动打开浏览器
    host: '0.0.0.0', // 允许外部访问（如同一局域网内其他设备）
    // API代理配置（解决跨域问题）
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 后端API地址
        changeOrigin: true, // 跨域时修改Origin
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  // 构建配置
  build: {
    outDir: 'dist', // 输出目录（默认dist）
    sourcemap: false, // 生产环境是否生成sourcemap（默认false）
    rollupOptions: {
      // 可以配置rollup的额外选项，比如分割代码
      output: {
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: '[ext]/[name]-[hash].[ext]'
      }
    }
  },
  // 环境变量配置
  envDir: './env', // 自定义环境变量文件目录（默认项目根目录）
})
