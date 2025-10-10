<!-- my-vue-app/src/components/layout/FooterSlider.vue -->
<template>
  <div class="footer-slider">
    <div class="slider-container">
      <button class="slider-btn prev" @click="prevTab">&lt;</button>
      
      <ul class="slider-list">
        <li 
          v-for="(tab, index) in tabs" 
          :key="tab.name"
          :class="{ active: isActive(tab.name) }"
          @click="switchTab(tab.name)"
        >
          {{ tab.label }}
        </li>
      </ul>
      
      <button class="slider-btn next" @click="nextTab">&gt;</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 标签页配置
const tabs = [
  { name: 'ImageRepair', label: '图像修复' },
  { name: 'Dashboard', label: '修复数据' },
  { name: 'Profile', label: '个人中心' },
  { name: 'AppValue', label: '应用价值' },
  { name: 'TechRoadmap', label: '技术路线' }
]

// 计算当前活跃的标签页
const currentTab = computed(() => {
  return route.name || 'ImageRepair'
})

// 检查是否为当前活跃页
const isActive = (tabName) => {
  return currentTab.value === tabName
}

// 切换标签页
const switchTab = (tabName) => {
  router.push({ name: tabName })
}

// 上一个标签页
const prevTab = () => {
  const currentIndex = tabs.findIndex(tab => tab.name === currentTab.value)
  const prevIndex = (currentIndex - 1 + tabs.length) % tabs.length
  switchTab(tabs[prevIndex].name)
}

// 下一个标签页
const nextTab = () => {
  const currentIndex = tabs.findIndex(tab => tab.name === currentTab.value)
  const nextIndex = (currentIndex + 1) % tabs.length
  switchTab(tabs[nextIndex].name)
}
</script>

<style scoped>
/* Footer 主容器 */
.footer-slider {
    width: 100%;                    /* 占满整个宽度 */
    padding: 20px 0;                /* 上下内边距，减少高度 */
    background: rgba(8, 23, 41, 0.95); /* 深蓝色半透明背景 */
    text-align: center;             /* 内容居中 */
    position: relative;             /* 相对定位用于伪元素 */
    margin-top: 10px;               /* 顶部外边距 */
    backdrop-filter: blur(10px);    /* 背景模糊效果 */
    border-top: 1px solid rgba(0, 216, 255, 0.2); /* 顶部边框 */
    border-bottom: 1px solid rgba(0, 216, 255, 0.1); /* 底部边框 */
     margin-top: -60px;
}

/* 背景网格效果 - 增加科技感 */
.footer-slider::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    /* 创建网格背景 */
    background: 
        linear-gradient(rgba(0, 216, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 216, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;     /* 网格大小 */
    pointer-events: none;           /* 不干扰鼠标事件 */
}

/* 滑动导航栏容器 */
.slider-container {
    display: flex;                  /* 弹性布局 */
    justify-content: center;        /* 水平居中 */
    align-items: center;            /* 垂直居中 */
    gap: 20px;                      /* 减少元素间距，让内容更紧凑 */
    position: relative;
    z-index: 2;
}

/* 左右滑动按钮 */
.slider-btn {
    background: transparent;        /* 透明背景 */
    border: none;                   /* 移除边框 */
    color: #00d8ff;                /* 科技蓝色 */
    font-size: 18px;                /* 减小字体大小 */
    cursor: pointer;                /* 手型光标 */
    transition: all 0.3s ease;      /* 平滑过渡效果 */
    width: auto;                    /* 自动宽度 */
    height: auto;                   /* 自动高度 */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 8px 12px;              /* 内边距 */
    opacity: 0.7;                   /* 半透明 */
}

/* 按钮悬停效果 */
.slider-btn:hover {
    opacity: 1;                     /* 完全不透明 */
    color: #00f7ff;                 /* 更亮的蓝色 */
    text-shadow: 0 0 10px rgba(0, 216, 255, 0.5); /* 发光效果 */
    transform: scale(1.1);          /* 轻微放大 */
}

/* 导航标签列表 */
.slider-list {
    display: flex;                  /* 弹性布局 */
    list-style: none;               /* 移除列表样式 */
    gap: 10px;                      /* 减少标签间距，更紧凑 */
    padding: 0;
    margin: 0;
}

/* 单个导航标签 - 椭圆边框设计 */
.slider-list li {
    background: rgba(16, 42, 67, 0.6); /* 半透明深蓝背景 */
    border: 1px solid rgba(0, 216, 255, 0.3); /* 半透明边框 */
    border-radius: 25px;            /* 椭圆圆角，更圆润 */
    padding: 8px 20px;              /* 减小内边距，整体变小 */
    font-size: 14px;                /* 减小字体大小 */
    color: #e0f7ff;                 /* 浅蓝色文字 */
    transition: all 0.3s ease;      /* 平滑过渡 */
    cursor: pointer;                /* 手型光标 */
    position: relative;
    overflow: hidden;
    font-weight: 500;               /* 中等字重 */
    letter-spacing: 0.5px;          /* 字间距 */
}

/* 标签底部光效 */
.slider-list li::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background: #00d8ff;            /* 蓝色光效 */
    transition: all 0.3s ease;      /* 平滑过渡 */
    transform: translateX(-50%);    /* 水平居中 */
}

/* 当前活跃的导航标签 */
.slider-list li.active {
    background: rgba(0, 216, 255, 0.15); /* 半透明蓝色背景 */
    border-color: #00d8ff;          /* 实线蓝色边框 */
    color: #00d8ff;                 /* 蓝色文字 */
    box-shadow: 
        inset 0 0 20px rgba(0, 216, 255, 0.1), /* 内发光 */
        0 0 20px rgba(0, 216, 255, 0.2); /* 外发光 */
}

.slider-list li.active::after {
    width: 60%;                     /* 底部光条宽度 */
}

/* 导航标签的悬停效果 */
.slider-list li:hover {
    background: rgba(0, 216, 255, 0.1); /* 半透明蓝色背景 */
    border-color: rgba(0, 216, 255, 0.6); /* 更明显的边框 */
    color: #00d8ff;                 /* 蓝色文字 */
    transform: translateY(-1px);    /* 轻微上浮 */
}

.slider-list li:hover::after {
    width: 40%;                     /* 悬停时底部光条 */
}

/* 底部数据流效果 */
.footer-slider::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    /* 渐变色数据流 */
    background: linear-gradient(90deg, 
        transparent, 
        #00d8ff, 
        #0077ff, 
        #00d8ff, 
        transparent
    );
    opacity: 0.3;                   /* 半透明 */
}

/* 整体浮动动画 */
@keyframes gentleFloat {
    0%, 100% { transform: translateY(0); }     /* 起始和结束位置 */
    50% { transform: translateY(-2px); }       /* 中间上浮位置 */
}

.slider-container {
    animation: gentleFloat 8s ease-in-out infinite; /* 无限循环浮动 */
}

/* 响应式调整 - 移动端适配 */
@media (max-width: 768px) {
    .slider-container {
        gap: 15px;                  /* 移动端更小间距 */
    }
    
    .slider-list {
        gap: 10px;                  /* 移动端更紧凑 */
    }
    
    .slider-list li {
        padding: 6px 15px;          /* 移动端更小内边距 */
        font-size: 12px;            /* 移动端更小字体 */
    }
    
    .slider-btn {
        font-size: 16px;            /* 移动端按钮字体 */
        padding: 6px 10px;          /* 移动端按钮内边距 */
    }
}
</style>