<!-- my-vue-app/src/components/layout/Header.vue -->
<template>
  <div class="header">
    <!-- 左侧时间 -->
    <div class="header-left fl">
      {{ currentTime }}
    </div>
    
    <!-- 中间标题和背景 -->
    <div class="header-center fl">
      <div class="header-title">
        文化遗产图像智能修复系统
      </div>
      <div class="header-img"></div>
    </div>
    
    <!-- 右侧空白 -->
    <div class="header-right fl"></div>
    
    <!-- 底部装饰 -->
    <div class="header-bottom fl"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentTime = ref('')

// 时间格式化函数
const fillZero = (str) => {
  return (str < 10) ? ('0' + str) : str
}

// 更新时间函数
const updateTime = () => {
  const myDate = new Date()
  const myYear = myDate.getFullYear()
  const myMonth = fillZero(myDate.getMonth() + 1)
  const myToday = fillZero(myDate.getDate())
  const myDay = myDate.getDay()
  const myHour = fillZero(myDate.getHours())
  const myMinute = fillZero(myDate.getMinutes())
  const mySecond = fillZero(myDate.getSeconds())
  const week = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  
  currentTime.value = `${myYear}-${myMonth}-${myToday} ${myHour}:${myMinute}:${mySecond} ${week[myDay]}`
}

let timeInterval

onMounted(() => {
  updateTime() // 立即执行一次
  timeInterval = setInterval(updateTime, 1000) // 每秒更新
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Header 主容器 */
.header {
    width: 100%;           /* 宽度占满父容器 */
    height: 1.5rem;        /* 固定高度，使用rem单位适配不同屏幕 */
    margin-top: 10rem;  /* 添加顶部外边距 */
    padding-top: 0.1rem; /* 或者添加内边距 */
}

/* 左侧时间显示区域 */
.header .header-left {
    width: 25%;            /* 占据头部宽度的25% */
    height: 10rem;       /* 内容区域高度 */
    color: white;          /* 文字颜色为白色 */
    text-align: center;    /* 文字居中对齐 */
    line-height: 1.5rem;  /* 行高等于高度，实现垂直居中 */
}

/* 中间标题区域 */
.header .header-center {
    width: 50%;            /* 占据头部宽度的50% */
    height: 1.5rem;       /* 内容区域高度 */
    position: relative;    /* 相对定位，为子元素绝对定位做准备 */
}

/* 主标题文字样式 */
.header .header-center .header-title {
    text-align: center;    /* 文字居中对齐 */
    color: #ffffff;        /* 白色文字 */
    font-size: 8rem;      /* 较大的字体大小 */
    text-shadow: 0 0 7rem #00d8ff;  /* 蓝色发光文字阴影，增强科技感 */
    line-height: 1.05rem;  /* 行高等于高度，实现垂直居中 */
}

/* 头部背景装饰图片 */
.header .header-img {
    background: url("/images/head.gif") no-repeat center center;  /* 背景图居中显示，不重复 */
    background-size: 100%;         /* 背景图宽度填满容器 */
    height: 100%;                  /* 高度填满父容器 */
    width: 100%;                   /* 宽度填满父容器 */
    position: absolute;            /* 绝对定位，脱离文档流 */
    top: 5rem;                    /* 距离顶部0.4rem */
}

/* 右侧空白区域（预留未来功能） */
.header .header-right {
    width: 25%;            /* 占据头部宽度的25% */
    height: 1.05rem;       /* 内容区域高度 */
    /* 目前为空白区域，可添加用户信息、设置按钮等功能 */
}

/* 底部装饰线条 */
.header .header-bottom {
    width: calc(100% - .4rem);     /* 宽度计算：100%宽度减去0.4rem边距 */
    height: 1.6rem;                /* 很细的装饰线高度 */
    background: url("/images/header.png") no-repeat;  /* 使用图片作为背景装饰 */
    background-size: calc(100% - .2rem) 100%;  /* 背景图大小调整 */
    padding: 0.2rem;              /* 左右内边距 */
    margin-left: 0.3rem;            /* 左外边距，实现居中偏移效果 */
}
</style>