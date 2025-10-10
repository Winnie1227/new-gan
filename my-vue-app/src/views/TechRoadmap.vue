<template>
  <div class="tech-roadmap">
    <div class="sci-fi-container">
      <div class="tech-header">
        <h2>修复核心技术路线</h2>
        <div class="tech-subtitle">从数据采集到专家验证的全流程技术体系</div>
        <div class="tech-decoration">
          <span class="decoration-line"></span>
          <i class="fas fa-atom"></i>
          <span class="decoration-line"></span>
        </div>
      </div>
      
      <div class="simple-flow">
        <div 
          v-for="(step, index) in flowSteps" 
          :key="step.id"
          class="flow-step"
          @click="showStepDetail(step.id)"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-name">{{ step.name }}</div>
        </div>
      </div>
      
      <div v-if="currentStep" class="dynamic-content-container">
  <h4>{{ currentStepData.title }}</h4>
  <div class="dynamic-content">
    <div class="detail-image">
      <img 
        :src="currentStepData.image" 
        :alt="currentStepData.title"
        @error="handleImageError"
      >
    </div>
    <div class="detail-list">
      <ul>
        <li v-for="(item, index) in currentStepData.items" :key="index" v-html="item"></li>
      </ul>
    </div>
  </div>
  <button @click="backToOriginal" class="back-button">
    ← 返回技术路线图
  </button>
</div>
      
      <div v-else class="original-image">
        <img src="/images/流程图.png" alt="技术路线原图">
        <div class="image-caption">网络模型技术路线图</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TechRoadmap',
  data() {
    return {
      currentStep: null,
      flowSteps: [
        { id: 'data-construction', name: '数据集构建' },
        { id: 'algorithm-design', name: '算法设计' },
        { id: 'model-testing', name: '模型测试' },
        { id: 'bigdata-analysis', name: '大数据分析' },
        { id: 'data-visualization', name: '数据可视化' },
        { id: 'expert-verification', name: '专家验证' }
      ],
      stepContents: {
        'data-construction': {
          title: '数据集构建',
          image: '/images/数据集构建.png',
          items: [
            '<i class="fas fa-map-marker-alt"></i> <strong>多源采集</strong>：江门侨乡文化遗产、增城博物馆实地采集',
            '<i class="fas fa-camera"></i> <strong>数据类型</strong>：高分辨率图像+多光谱数据+3D点云',
            '<i class="fas fa-brain"></i> <strong>增强技术</strong>：GAN模拟损毁+人工标注',
            '<i class="fas fa-database"></i> <strong>数据规模</strong>：10,000+图像样本，5种损坏类型',
            '<i class="fas fa-tags"></i> <strong>标注规范</strong>：专家团队制定损坏区域标注标准',
            '<i class="fas fa-cloud"></i> <strong>存储方案</strong>：分布式云存储确保数据安全'
          ]
        },
        'algorithm-design': {
          title: '算法设计',
          image: '/images/算法设计.png',
          items: [
            '<i class="fas fa-network-wired"></i> <strong>混合架构</strong>：GAN+Transformer+U-Net',
            '<i class="fas fa-lightbulb"></i> <strong>创新模块</strong>：文化风格特征提取子网络',
            '<i class="fas fa-project-diagram"></i> <strong>边缘引导</strong>：Canny检测+结构损失函数',
            '<i class="fas fa-layer-group"></i> <strong>技术指标</strong>：5层注意力机制，3种网络融合',
            '<i class="fas fa-code-branch"></i> <strong>多尺度特征</strong>：金字塔结构捕捉不同层次特征',
            '<i class="fas fa-palette"></i> <strong>风格迁移</strong>：基于VGG网络的风格损失计算'
          ]
        },
        'model-testing': {
          title: '模型测试',
          image: '/images/模型测试.png',
          items: [
            '<i class="fas fa-chart-line"></i> <strong>量化指标</strong>：PSNR ≥32dB，SSIM ≥0.91',
            '<i class="fas fa-robot"></i> <strong>优化策略</strong>：对抗训练+感知损失',
            '<i class="fas fa-server"></i> <strong>硬件加速</strong>：GPU集群并行测试',
            '<i class="fas fa-balance-scale"></i> <strong>对比基准</strong>：与传统方法进行AB测试',
            '<i class="fas fa-undo"></i> <strong>迭代优化</strong>：根据测试结果调整超参数',
            '<i class="fas fa-temperature-high"></i> <strong>压力测试</strong>：模拟极端损坏情况下的表现'
          ]
        },
        'bigdata-analysis': {
          title: '大数据分析',
          image: '/images/大数据分析.png',
          items: [
            '<i class="fas fa-database"></i> <strong>数据规模</strong>：10TB+修复过程数据',
            '<i class="fas fa-project-diagram"></i> <strong>分析维度</strong>：8维特征空间聚类',
            '<i class="fas fa-chart-pie"></i> <strong>损坏模式</strong>：常见损坏类型统计分析',
            '<i class="fas fa-link"></i> <strong>相关性研究</strong>：修复效果与损坏程度的关系',
            '<i class="fas fa-cloud"></i> <strong>计算平台</strong>：Spark分布式计算框架',
            '<i class="fas fa-filter"></i> <strong>数据清洗</strong>：异常值检测与处理'
          ]
        },
        'data-visualization': {
          title: '数据可视化',
          image: '/images/数据可视化.png',
          items: [
            '<i class="fas fa-chart-bar"></i> <strong>交互图表</strong>：15种可交互分析图表',
            '<i class="fas fa-cube"></i> <strong>三维展示</strong>：文物数字孪生模型',
            '<i class="fas fa-desktop"></i> <strong>实时渲染</strong>：WebGL加速的实时可视化',
            '<i class="fas fa-sliders-h"></i> <strong>动态对比</strong>：修复前后效果对比工具',
            '<i class="fas fa-map"></i> <strong>地理信息</strong>：文物出土地点GIS展示',
            '<i class="fas fa-vr-cardboard"></i> <strong>VR支持</strong>：虚拟现实环境下的文物展示'
          ]
        },
        'expert-verification': {
          title: '专家验证',
          image: '/images/专家验证.png',
          items: [
            '<i class="fas fa-user-tie"></i> <strong>专家团队</strong>：8位跨领域专家参与评估',
            '<i class="fas fa-clipboard-check"></i> <strong>评估体系</strong>：4级量化评估标准',
            '<i class="fas fa-x-ray"></i> <strong>科技手段</strong>：X射线/红外成像验证',
            '<i class="fas fa-book"></i> <strong>艺术评估</strong>：参照《元明清瓷器鉴定》标准',
            '<i class="fas fa-link"></i> <strong>区块链</strong>：关键决策上链存证',
            '<i class="fas fa-history"></i> <strong>版本管理</strong>：修复历史版本追溯'
          ]
        }
      }
    }
  },
  computed: {
    currentStepData() {
      return this.currentStep ? this.stepContents[this.currentStep] : null
    }
  },
  methods: {
  showStepDetail(stepId) {
    console.log('点击阶段:', stepId)
    console.log('stepContents中是否存在:', this.stepContents[stepId])
    
    // Vue 3 中直接赋值即可，不需要 $set
    this.currentStep = stepId
    
    console.log('currentStep设置后:', this.currentStep)
    console.log('currentStepData:', this.currentStepData)
  },
  
  backToOriginal() {
    console.log('返回原图')
    this.currentStep = null
  },
  
  handleImageError(event) {
    console.error('图片加载失败:', event.target.src)
    event.target.style.display = 'none'
  }
}
}
</script>

<style scoped>
/* 主容器样式 - 设置整个技术路线图组件的基本布局 */
.tech-roadmap {
  min-height: 10vh;  /* 最小高度为整个视口高度，确保占满屏幕 */
  padding: 2rem;    /* 内边距，使用 rem 单位适配不同屏幕 */
  margin-top: 30rem; /* 添加这个，让整个组件向下移动 */
}

/* 科幻风格容器 - 主要的内容区域，具有科技感的背景和边框 */
.sci-fi-container {
  background: rgba(3, 29, 53, 0.7);  /* 半透明深蓝色背景，营造科技感 */
  border: 1px solid #00a8ff;         /* 亮蓝色边框 */
  border-radius: 1rem;             /* 圆角边框 */
  padding: 10rem;                   /* 内边距 */
  position: relative;                /* 相对定位，为子元素定位做准备 */
  overflow: hidden;                  /* 隐藏溢出内容 */
  box-shadow: 0 0 0.5rem rgba(0, 168, 255, 0.2);  /* 蓝色发光阴影效果 */
  z-index: 1;                       /* 设置层级，确保在正确层叠上下文中 */
}

/* 技术标题样式 */
.tech-header h2 {
  color: #00d8ff;      /* 亮青色文字 */
  font-size: 8rem;  /* 字体大小 */
  margin-bottom: 2rem; /* 底部外边距 */
  text-align: center;  /* 文字居中 */
}

/* 副标题样式 */
.tech-subtitle {
  color: #a0f0ff;     /* 浅蓝色文字 */
  font-size: 0.18rem;  /* 字体大小 */
  text-align: center;  /* 文字居中 */
  margin-bottom: 0.2rem; /* 底部外边距 */
}

/* 装饰元素容器 - 用于放置装饰性线条和图标 */
.tech-decoration {
  display: flex;           /* 弹性布局 */
  align-items: center;     /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  margin: 2rem 0;       /* 上下外边距 */
}

/* 装饰线条 - 渐变色分隔线 */
.decoration-line {
  flex: 1;  /* 占据剩余空间 */
  height: 1px;  /* 线条高度 */
  background: linear-gradient(90deg, transparent, #00a8ff, transparent);  /* 渐变色背景 */
}

/* 装饰图标 */
.tech-decoration i {
  color: #00a8ff;
  font-size: 5rem;
  margin: 0 1.5rem;
}

/* 旋转动画 */
@keyframes rotate-center {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}


/* 简单流程容器 - 步骤按钮的布局容器 */
.simple-flow {
  display: flex;           /* 弹性布局 */
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  flex-wrap: wrap;        /* 允许换行 */
  margin: 0.3rem 0;       /* 上下外边距 */
  gap: 1rem;            /* 子元素间距 */
  position: relative;     /* 相对定位 */
  z-index: 2;            /* 设置层级 */
}

/* 流程步骤按钮 - 每个可点击的步骤 */
/* 流程步骤按钮 - 科幻胶囊设计 */
.flow-step {
  background: linear-gradient(135deg, rgba(11, 61, 102, 0.9), rgba(8, 42, 80, 0.9)); /* 渐变背景 */
  border: none;                           /* 移除边框 */
  border-radius: 0.5rem;                  /* 大圆角，胶囊形状 */
  padding: 2rem 4rem;                 /* 调整内边距 */
  cursor: pointer !important;             /* 手型光标，强制生效 */
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* 平滑过渡动画 */
  min-width: 1.5rem;                      /* 最小宽度 */
  text-align: center;                     /* 文字居中 */
  margin: 0.2rem;                         /* 减小外边距 */
  pointer-events: auto !important;        /* 确保可以点击，强制生效 */
  position: relative;                     /* 为伪元素定位 */
  overflow: hidden;                       /* 隐藏溢出的伪元素 */
  color: #e0f7ff;                        /* 浅蓝色文字 */
  box-shadow: 
    0 0.1rem 0.3rem rgba(0, 0, 0, 0.3),  /* 基础阴影 */
    inset 0 1px 0 rgba(255, 255, 255, 0.1); /* 内阴影增加立体感 */
}

/* 添加光效边框 */
.flow-step::before {
  content: '';                           /* 伪元素内容 */
  position: absolute;                    /* 绝对定位 */
  top: 0;                               /* 顶部对齐 */
  left: 0;                              /* 左侧对齐 */
  right: 0;                             /* 右侧对齐 */
  bottom: 0;                            /* 底部对齐 */
  border-radius: 0.5rem;                /* 匹配按钮圆角 */
  background: linear-gradient(135deg, rgba(0, 168, 255, 0.3), rgba(0, 216, 255, 0.1)); /* 渐变光效 */
  opacity: 0;                           /* 默认隐藏 */
  transition: opacity 0.3s ease;        /* 透明度过渡 */
  z-index: 1;                           /* 置于内容上层 */
}

/* 添加扫描线效果 */
.flow-step::after {
  content: '';                          /* 伪元素内容 */
  position: absolute;                   /* 绝对定位 */
  top: -100%;                          /* 初始位置在顶部以上 */
  left: 0;                             /* 左侧对齐 */
  width: 100%;                         /* 全宽 */
  height: 0.1rem;                      /* 细线高度 */
  background: linear-gradient(90deg, transparent, #00d8ff, transparent); /* 扫描线渐变 */
  opacity: 0;                          /* 默认隐藏 */
  transition: all 0.5s ease;           /* 过渡动画 */
}

/* 步骤按钮悬停效果 */
.flow-step:hover {
  transform: translateY(-0.1rem) scale(1.05); /* 上浮并放大 */
  box-shadow: 
    0 0.2rem 0.6rem rgba(0, 168, 255, 0.4), /* 外发光 */
    inset 0 1px 0 rgba(255, 255, 255, 0.2); /* 增强内阴影 */
  background: linear-gradient(135deg, rgba(0, 120, 215, 0.9), rgba(0, 80, 160, 0.9)); /* 悬停渐变 */
}

.flow-step:hover::before {
  opacity: 1;                          /* 显示光效 */
}

.flow-step:hover::after {
  opacity: 0.8;                        /* 显示扫描线 */
  top: 100%;                          /* 从顶部扫描到底部 */
}

/* 激活状态 */
.flow-step.active {
  background: linear-gradient(135deg, rgba(0, 216, 255, 0.9), rgba(0, 150, 255, 0.9)); /* 激活状态渐变 */
  box-shadow: 
    0 0 0.4rem #00d8ff,               /* 强发光 */
    0 0.2rem 0.8rem rgba(0, 216, 255, 0.6); /* 扩散阴影 */
  color: #000;                         /* 深色文字提高可读性 */
  transform: scale(1.08);              /* 轻微放大 */
}

.flow-step.active::before {
  opacity: 0.6;                        /* 增强光效 */
  animation: pulseGlow 2s infinite;    /* 脉冲光效动画 */
}

/* 脉冲光效动画 */
@keyframes pulseGlow {
  0%, 100% { 
    opacity: 0.6; 
    background: linear-gradient(135deg, rgba(0, 216, 255, 0.4), rgba(0, 150, 255, 0.2));
  }
  50% { 
    opacity: 0.9; 
    background: linear-gradient(135deg, rgba(0, 216, 255, 0.7), rgba(0, 150, 255, 0.5));
  }
}

/* 步骤数字样式 */
.step-number {
  font-size: 0.2rem;                   /* 调整字体大小 */
  font-weight: bold;                   /* 粗体 */
  color: #00d8ff;                      /* 亮青色 */
  position: relative;                  /* 相对定位 */
  z-index: 2;                          /* 置于光效上层 */
  text-shadow: 0 0 0.1rem rgba(0, 216, 255, 0.5); /* 文字发光 */
}

/* 步骤名称样式 */
.step-name {
  font-size: 0.16rem;                  /* 调整字体大小 */
  color: #ffffff;                      /* 白色文字 */
  position: relative;                  /* 相对定位 */
  z-index: 2;                          /* 置于光效上层 */
  text-shadow: 0 0 0.1rem rgba(255, 255, 255, 0.3); /* 文字微光 */
}

/* 原始图片容器 - 显示技术路线原图 */
.original-image {
  margin-top: 5rem;                  /* 顶部外边距 */
  border: 1px solid #0b3d66;          /* 边框 */
  padding: 1rem;                     /* 内边距 */
  background: rgba(3, 29, 53, 0.8);   /* 半透明背景 */
  max-width: 60%;                      /* 最大宽度 */
  margin-left: auto;                   /* 自动左外边距 */
  margin-right: auto;                  /* 自动右外边距，实现居中 */
}

/* 原始图片样式 */
.original-image img {
  max-width: 100%;  /* 最大宽度为容器宽度 */
  display: block;   /* 块级显示 */
  margin: 0 auto;   /* 水平居中 */
}

/* 图片标题样式 */
.image-caption {
  font-size: 5rem;  /* 字体大小 */
  color: #00d8ff;      /* 亮青色 */
  text-align: center;  /* 文字居中 */
  margin-top: 5rem;  /* 顶部外边距 */
}

/* 动态内容区域样式 - 点击步骤后显示详细内容的容器 */
.dynamic-content-container {
  /* 保证显示的基础属性 */
  display: block !important;        /* 块级显示，强制生效 */
  opacity: 1 !important;           /* 完全不透明，强制生效 */
  visibility: visible !important;  /* 可见，强制生效 */
  
  /* 恢复原有样式 */
  margin-top: 0.3rem;                  /* 顶部外边距 */
  border: 1px solid #0b3d66;          /* 边框 */
  padding: 2rem;                     /* 内边距 */
  background: rgba(3, 29, 53, 0.7);   /* 半透明背景 */
  border-radius: 0.08rem;              /* 圆角 */
  animation: fadeIn 0.5s ease;         /* 淡入动画 */
  position: relative;                  /* 相对定位 */
  z-index: 10;                        /* 设置较高层级 */
}

/* 动态内容标题 */
.dynamic-content-container h4 {
  color: #00d8ff;          /* 亮青色 */
  font-size: 5rem;      /* 字体大小 */
  margin-bottom: 1.5rem;  /* 底部外边距 */
  text-align: center;      /* 文字居中 */
  border-bottom: 1px solid #0b3d66;  /* 底部边框 */
  padding-bottom: 1rem;  /* 底部内边距 */
}

/* 动态内容布局 - 图片和列表的排列 */
.dynamic-content {
  display: flex;     /* 弹性布局 */
  gap: 3rem;       /* 子元素间距 */
  margin-top: 5rem; /* 顶部外边距 */
}

/* 详情图片区域 */
.detail-image {
  width: 45%;  /* 宽度占比45% */
}

/* 详情图片 */
.detail-image img {
  width: 100%;                /* 宽度充满容器 */
  border: 1px solid #0b3d66;  /* 边框 */
  border-radius: 0.05rem;     /* 圆角 */
}

/* 详情列表区域 */
.detail-list {
  width: 55%;  /* 宽度占比55% */
}

/* 详情列表 */
.detail-list ul {
  list-style: none;  /* 移除列表默认样式 */
  padding: 0;        /* 移除内边距 */
  margin: 0;         /* 移除外边距 */
}

/* 详情列表项 */
.detail-list li {
  padding: 1rem 0;                     /* 上下内边距 */
  line-height: 4;                      /* 行高 */
  font-size: 1.6rem;                    /* 字体大小 */
  color: #a0f0ff;                        /* 浅蓝色文字 */
  display: flex;                         /* 弹性布局 */
  align-items: flex-start;               /* 顶部对齐 */
  border-bottom: 1px dashed rgba(11, 61, 102, 0.5);  /* 底部虚线边框 */
}

/* 最后一个列表项 */
.detail-list li:last-child {
  border-bottom: none;  /* 移除底部边框 */
}

/* 列表项图标 */
.detail-list i {
  margin-right: 1rem;  /* 右外边距 */
  color: #00f5d4;        /* 青绿色 */
  font-size: 1.4rem;    /* 图标大小 */
  min-width: 2rem;     /* 最小宽度 */
  text-align: center;    /* 文字居中 */
  margin-top: 0.03rem;   /* 顶部外边距，微调垂直对齐 */
}

/* 返回按钮 */
.back-button {
  background: none;                  /* 透明背景 */
  border: 1px solid #00a8ff;        /* 蓝色边框 */
  color: #00a8ff;                   /* 蓝色文字 */
  font-size: 1.6rem;               /* 字体大小 */
  cursor: pointer;                  /* 手型光标 */
  margin-top: 0.15rem;              /* 顶部外边距 */
  padding: 0.8rem 0.2rem;          /* 内边距 */
  border-radius: 0.05rem;           /* 圆角 */
  transition: all 0.3s;             /* 过渡动画 */
  display: block;                   /* 块级显示 */
  margin-left: auto;                /* 自动左外边距 */
  margin-right: auto;               /* 自动右外边距，实现居中 */
}

/* 返回按钮悬停效果 */
.back-button:hover {
  background: rgba(0,168,255,0.2);  /* 半透明蓝色背景 */
  color: #00d8ff;                   /* 亮青色文字 */
}

/* 淡入动画定义 */
@keyframes fadeIn {
  from { 
    opacity: 0;                    /* 完全透明 */
    transform: translateY(10px);   /* 向下偏移 */
  }
  to { 
    opacity: 1;                    /* 完全不透明 */
    transform: translateY(0);      /* 回到原位 */
  }
}

/* 响应式调整 - 针对小屏幕设备的样式优化 */
@media (max-width: 768px) {
  .dynamic-content {
    flex-direction: column;  /* 改为垂直排列 */
  }
  .detail-image,
  .detail-list {
    width: 100%;  /* 宽度充满容器 */
  }
}
</style>