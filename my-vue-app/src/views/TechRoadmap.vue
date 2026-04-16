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
/* 主容器样式 - 整体缩小并下移 */
.tech-roadmap {
  min-height: auto;
  padding: 5px;
  margin-top: 40px;  /* 增加上边距，向下移动避免遮挡 */
  margin-bottom: 20px;
  transform: scale(0.95);
  transform-origin: top center;
}

/* 科幻风格容器 */
.sci-fi-container {
  background: rgba(3, 29, 53, 0.7);
  border: 1px solid #00a8ff;
  border-radius: 10px;
  padding: 12px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 6px rgba(0, 168, 255, 0.2);
  z-index: 1;
}

/* 技术标题样式 */
.tech-header h2 {
  color: #00d8ff;
  font-size: 22px;  /* 从20px加大到22px */
  margin-bottom: 5px;
  text-align: center;
}

/* 副标题样式 */
.tech-subtitle {
  color: #a0f0ff;
  font-size: 13px;  /* 从12px加大到13px */
  text-align: center;
  margin-bottom: 8px;
}

/* 装饰元素容器 */
.tech-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 8px 0;
}

/* 装饰线条 */
.decoration-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00a8ff, transparent);
}

/* 装饰图标 */
.tech-decoration i {
  color: #00a8ff;
  font-size: 16px;  /* 从14px加大到16px */
  margin: 0 10px;
}

/* 简单流程容器 */
.simple-flow {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin: 12px 0;  /* 增加一点间距 */
  gap: 10px;
  position: relative;
  z-index: 2;
}

/* 流程步骤按钮 */
.flow-step {
  background: linear-gradient(135deg, rgba(11, 61, 102, 0.9), rgba(8, 42, 80, 0.9));
  border: none;
  border-radius: 6px;
  padding: 6px 14px;  /* 稍微加大内边距 */
  cursor: pointer !important;
  transition: all 0.3s ease;
  min-width: 75px;
  text-align: center;
  margin: 2px;
  pointer-events: auto !important;
  position: relative;
  overflow: hidden;
  color: #e0f7ff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

/* 步骤数字样式 */
.step-number {
  font-size: 12px;  /* 从11px加大到12px */
  font-weight: bold;
  color: #00d8ff;
  position: relative;
  z-index: 2;
}

/* 步骤名称样式 */
.step-name {
  font-size: 12px;  /* 从11px加大到12px */
  color: #ffffff;
  position: relative;
  z-index: 2;
}

/* 原始图片容器 */
.original-image {
  margin-top: 15px;  /* 增加上边距 */
  border: 1px solid #0b3d66;
  padding: 10px;
  background: rgba(3, 29, 53, 0.8);
  max-width: 65%;
  margin-left: auto;
  margin-right: auto;
}

/* 原始图片样式 */
.original-image img {
  max-width: 100%;
  display: block;
  margin: 0 auto;
}

/* 图片标题样式 */
.image-caption {
  font-size: 12px;  /* 从11px加大到12px */
  color: #00d8ff;
  text-align: center;
  margin-top: 8px;
}

/* 动态内容区域样式 */
.dynamic-content-container {
  display: block !important;
  opacity: 1 !important;
  visibility: visible !important;
  margin-top: 15px;
  border: 1px solid #0b3d66;
  padding: 15px;
  background: rgba(3, 29, 53, 0.7);
  border-radius: 6px;
  animation: fadeIn 0.4s ease;
  position: relative;
  z-index: 10;
}

/* 动态内容标题 */
.dynamic-content-container h4 {
  color: #00d8ff;
  font-size: 18px;  /* 从16px加大到18px */
  margin-bottom: 12px;
  text-align: center;
  border-bottom: 1px solid #0b3d66;
  padding-bottom: 8px;
}

/* 动态内容布局 */
.dynamic-content {
  display: flex;
  gap: 18px;
  margin-top: 10px;
}

/* 详情图片区域 */
.detail-image {
  width: 45%;
}

/* 详情图片 */
.detail-image img {
  width: 100%;
  border: 1px solid #0b3d66;
  border-radius: 4px;
}

/* 详情列表区域 */
.detail-list {
  width: 55%;
}

/* 详情列表 */
.detail-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* 详情列表项 */
.detail-list li {
  padding: 8px 0;  /* 从6px加大到8px */
  line-height: 1.5;
  font-size: 13px;  /* 从11px加大到13px */
  color: #a0f0ff;
  display: flex;
  align-items: flex-start;
  border-bottom: 1px dashed rgba(11, 61, 102, 0.5);
}

/* 最后一个列表项 */
.detail-list li:last-child {
  border-bottom: none;
}

/* 列表项图标 */
.detail-list i {
  margin-right: 8px;
  color: #00f5d4;
  font-size: 13px;  /* 从11px加大到13px */
  min-width: 18px;
  text-align: center;
  margin-top: 2px;
}

/* 返回按钮 */
.back-button {
  background: none;
  border: 1px solid #00a8ff;
  color: #00a8ff;
  font-size: 12px;  /* 从11px加大到12px */
  cursor: pointer;
  margin-top: 15px;
  padding: 5px 14px;
  border-radius: 4px;
  transition: all 0.3s;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

/* 返回按钮悬停效果 */
.back-button:hover {
  background: rgba(0, 168, 255, 0.2);
  color: #00d8ff;
}

/* 淡入动画定义 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .tech-roadmap {
    transform: scale(0.94);
    margin-top: 30px;  /* 手机端也向下移动 */
    padding: 3px;
  }
  
  .sci-fi-container {
    padding: 10px;
  }
  
  .tech-header h2 {
    font-size: 20px;
  }
  
  .tech-subtitle {
    font-size: 12px;
  }
  
  .flow-step {
    padding: 5px 12px;
    min-width: 65px;
  }
  
  .step-number,
  .step-name {
    font-size: 11px;
  }
  
  .dynamic-content {
    flex-direction: column;
    gap: 12px;
  }
  
  .detail-image,
  .detail-list {
    width: 100%;
  }
  
  .original-image {
    max-width: 90%;
    padding: 8px;
  }
  
  .image-caption {
    font-size: 11px;
  }
  
  .dynamic-content-container h4 {
    font-size: 16px;
  }
  
  .detail-list li {
    font-size: 12px;
    padding: 6px 0;
  }
  
  .back-button {
    font-size: 11px;
    padding: 4px 12px;
  }
}
</style>