import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/css/all.min.css'
import * as echarts from 'echarts'

// ① 引入两省 GeoJSON（必须放在 src/geo 且后缀 .json）
import gxGeo from '@/geo/guangxi.json'
import fjGeo from '@/geo/fujian.json'

// ② 立即注册（同步，保证先于任何图表）
echarts.registerMap('guangxi', gxGeo)
echarts.registerMap('fujian', fjGeo)
console.log('广西 & 福建 地图注册完成')

const app = createApp(App)
window.echarts = echarts
app.provide('echarts', echarts)

app.use(createPinia())
app.use(router)
app.mount('#app')