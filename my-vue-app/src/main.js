// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/css/all.min.css'
import * as echarts from 'echarts';

// 引入地图组件
import 'echarts/components.js'; // 引入所有组件
// 或者按需引入
// import 'echarts/lib/chart/map';
// import 'echarts/lib/component/visualMap';

const app = createApp(App)

// 尝试注册中国地图
try {
  // 方式1：使用在线地图数据
  fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    .then(response => response.json())
    .then(chinaJson => {
      echarts.registerMap('china', chinaJson);
      console.log('中国地图注册成功');
    })
    .catch(error => {
      console.warn('在线地图加载失败，使用内置地图:', error);
    //   // 方式2：尝试使用内置地图
    //   try {
    //     // 这里需要确保 echarts/map/js/china.js 被正确引入
    //     console.log('使用内置地图数据');
    //   } catch (e) {
    //     console.error('所有地图加载方式都失败了:', e);
    //   }
    });
} catch (error) {
  console.warn('地图初始化异常:', error);
}

window.echarts = echarts
app.provide('echarts', echarts)
app.use(createPinia())
app.use(router)
app.mount('#app')