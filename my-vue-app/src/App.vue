<!-- 简化App.vue 入口文件 -->
<template>
  <div id="app">
    <!-- 登录页面单独显示 -->
    <template v-if="isLoginPage">
      <router-view></router-view>
    </template>
    
    <!-- 主应用布局 -->
    <template v-else>
      <!-- 头部组件 -->
      <AppHeader />
      
      <!-- 主要内容区域 -->
      <main class="main-content">
        <router-view></router-view>
      </main>
      
      <!-- 底部导航 -->
      <FooterSlider />
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/layout/Header.vue'
import FooterSlider from './components/layout/FooterSlider.vue'

const route = useRoute()

// 判断当前是否是登录页面
const isLoginPage = computed(() => route.name === 'Login')
</script>

<style>
/* 全局样式 */
@import url('./assets/styles/main.css');

/* 重置基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: 1rem;
  overflow: auto;
}

/* 确保所有面板正常显示 */
[id*="panel"],
.tab-panel {
  display: block !important;
  visibility: visible !important;
  height: 100%;
}
</style>