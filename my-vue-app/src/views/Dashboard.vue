<template>
  <div class="tab-panel active dashboard-panel">
    <div class="dashboard">
      <!-- 左侧区域 -->
      <div class="dashboard-left">
        <!-- 修复图片总数及完成率面板 - 压缩 -->
        <div class="content-panel panel-small">
          <h3>修复图片总数及完成率</h3>
          <!-- 移除固定高度，让CSS控制 -->
          <div ref="chart4" class="chart-container"></div>
        </div>
        <!-- 数据集来源及修复时间 - 加长 -->
        <div class="content-panel panel-large">
          <h3>数据集来源及修复时间</h3>
          <!-- 移除固定高度 -->
          <div ref="externalChart1" class="chart-container"></div>
        </div>
      </div>

      <!-- 中间地图  -->
      <div class="dashboard-center">
        <div class="content-panel map-panel">
          <div style="position:absolute;top:10px;left:50%;transform:translateX(-50%);z-index:9">
            <select v-model="currentMap"
              style="width:120px;height:28px;background:rgba(0,0,0,.5);color:#00c2ff;border:1px solid #00c2ff;border-radius:4px;padding-left:6px">
              <option value="guangxi">广西</option>
              <option value="fujian">福建</option>
              <option value="guangdong">广东</option>
            </select>
          </div>
          <!-- 地图高度稍微减小 -->
          <div ref="mapChart" class="chart-container" :style="{height:'520px'}"></div>
        </div>
      </div>

      <!-- 右侧区域 - 下移 -->
      <div class="dashboard-right">
        <!-- 建筑类型占比 - 增大 -->
        <div class="content-panel panel-top">
          <h3>建筑类型占比</h3>
          <!-- 移除固定高度 -->
          <div ref="chart3" class="chart-container"></div>
        </div>

        <!-- 实时榜单 -->
        <div class="content-panel">
          <h3>实时榜单</h3>
          <div class="realtime-ranking">
            <ul ref="rankingList">
              <li><span class="rank-item">图像001</span><span class="rank-time">用时5.1s</span></li>
              <li><span class="rank-item">图像002</span><span class="rank-time">用时6.8s</span></li>
              <li><span class="rank-item">图像003</span><span class="rank-time">用时3.4s</span></li>
              <li><span class="rank-item">图像004</span><span class="rank-time">用时8.9s</span></li>
              <li><span class="rank-item">图像005</span><span class="rank-time">用时4.2s</span></li>
            </ul>
          </div>
        </div>

        <!-- 建筑地理位置显示 -->
        <div class="content-panel">
          <h3>建筑地理位置显示</h3>
          <!-- 移除固定高度 -->
          <div ref="chart2" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, onUnmounted, ref, inject, watch } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const echarts = inject('echarts');

    const currentMap = ref('guangxi')   // 默认广西
    let mapInstance = null
    
    // 原有图表引用
    const chart2 = ref(null);
    const chart3 = ref(null);
    const chart4 = ref(null);
    const rankingList = ref(null);
    
    // 外部图表引用
    const externalChart1 = ref(null);
      // 地图引用
    const mapChart = ref(null);
    
    let chartInstances = [];
    let scrollInterval = null;

    const initCharts = () => {
      try {
        if (!echarts) {
          console.error('ECharts 未正确注入');
          return;
        }

        console.log('开始初始化图表...');
        console.log('地图是否注册:', echarts.getMap('china'));

        // 初始化左侧图表
        if (chart4.value) {
          const chart4Instance = echarts.init(chart4.value);
          chart4Instance.setOption(getChart4Option());
          chartInstances.push(chart4Instance);
          console.log('图表4初始化完成');
        }

        initMap()


        // 初始化右侧图表
        if (chart3.value) {
          const chart3Instance = echarts.init(chart3.value);
          chart3Instance.setOption(getChart3Option());
          chartInstances.push(chart3Instance);
          console.log('图表3初始化完成');
        }

        if (chart2.value) {
          const chart2Instance = echarts.init(chart2.value);
          chart2Instance.setOption(getChart2Option());
          chartInstances.push(chart2Instance);
          console.log('图表2初始化完成');
        }

        // 初始化外部图表
        initExternalCharts();

        console.log('所有图表初始化完成');

        // 窗口调整大小处理
        const handleResize = () => {
          chartInstances.forEach(instance => {
            try {
              instance.resize();
            } catch (error) {
              console.error('图表调整大小失败:', error);
            }
          });
        };

        window.addEventListener('resize', handleResize);

        return () => {
          window.removeEventListener('resize', handleResize);
        };

      } catch (error) {
        console.error('初始化图表失败:', error);
      }
    };


const getSimpleMapOption = () => {
  return {
    title: {
      text: '图像修复地理位置分布',
      left: 'center',
      textStyle: {
        color: '#fff',
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item'
    },
    series: [{
      type: 'pie',
      radius: '70%',
      data: [
        { name: '广东省', value: 450 },
        { name: '其他地区', value: 650 }
      ],
      label: {
        color: '#fff'
      }
    }]
  };
};

    // 初始化外部图表
    const initExternalCharts = () => {
      try {
        // 外部图表1 - 数据集来源
        if (externalChart1.value) {
          const chartInstance = echarts.init(externalChart1.value);
          chartInstance.setOption(getExternalChart1Option());
          chartInstances.push(chartInstance);
          console.log('外部图表1初始化完成');
        }

      } catch (error) {
        console.error('初始化外部图表失败:', error);
      }
    };

    const initScrollEffect = () => {
      if (!rankingList.value) return;

      const items = rankingList.value.querySelectorAll('li');
      if (items.length === 0) return;

      let currentIndex = 0;
      
      items[currentIndex].classList.add('active');

      scrollInterval = setInterval(() => {
        items.forEach(item => item.classList.remove('active'));
        
        currentIndex = (currentIndex + 1) % items.length;
        items[currentIndex].classList.add('active');
      }, 2000);
    };

    const getChart2Option = () => ({
  title: {
    left: 'center',
    textStyle: {
      color: '#fff',
      fontSize: 14
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  series: [
    {
      name: '地区分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#0b3d66',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '14',
          fontWeight: 'bold',
          color: '#fff'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 250, name: '江门地区', itemStyle: { color: '#00c2ff' } },
        { value: 120, name: '粤西地区', itemStyle: { color: '#00ff88' } },
        { value: 80, name: '潮汕地区', itemStyle: { color: '#ff6b6b' } }
      ]
    }
  ]
});

        /* ===== 新增 2 ===== */
    // 动态注册地图
    const registerMap = async (adcode) => {
    if (echarts.getMap(adcode)) return;
    const res = await fetch(`/src/geo/${adcode}.json`);
    const geo = await res.json();
    echarts.registerMap(adcode, geo);
  };

    // 地图配置（动态地图名）
 const getMapOption = () => {
  // 根据当前地图返回对应的数据
  let mapData = []
  if (currentMap.value === 'guangxi') {
    mapData = [
      { name: '南宁市', value: 220 },
      { name: '横州市', value: 100 },
      { name: '崇左市', value: 95 },
      { name: '柳州市', value: 80 },
      { name: '贵港市', value: 80 },
      { name: '钦州市', value: 77 },
      { name: '百色市', value: 70 },
      { name: '桂林市', value: 60 }
    ]
  } else if (currentMap.value === 'fujian') {
    mapData = [
      { name: '泉州市', value: 420 },
      { name: '厦门市', value: 140 },
      { name: '龙岩市', value: 120 },
      { name: '福州市', value: 90 },
      { name: '漳州市', value: 70 }
    ]
  } else if (currentMap.value === 'guangdong') {
    mapData = [
      { name: '广州市', value: 350 },
      { name: '深圳市', value: 420 },
      { name: '佛山市', value: 280 },
      { name: '东莞市', value: 250 },
      { name: '惠州市', value: 180 },
      { name: '中山市', value: 150 },
      { name: '珠海市', value: 120 },
      { name: '江门市', value: 110 },
      { name: '肇庆市', value: 90 },
      { name: '汕头市', value: 85 },
      { name: '湛江市', value: 80 },
      { name: '茂名市', value: 75 },
      { name: '梅州市', value: 70 },
      { name: '清远市', value: 65 },
      { name: '揭阳市', value: 60 },
      { name: '韶关市', value: 55 },
      { name: '阳江市', value: 50 },
      { name: '潮州市', value: 45 },
      { name: '河源市', value: 40 },
      { name: '汕尾市', value: 35 },
      { name: '云浮市', value: 30 }
    ]
  }

  return {
    title: { show: false },
    tooltip: { trigger: 'item' },
    visualMap: {
      type: 'continuous',
      min: 0,
      max: 500,
      text: ['高', '低'],
      calculable: true,
      inRange: { color: ['#4575b4', '#74add1', '#abd9e9', '#ffffbf', '#fdae61', '#d73027'] },
      textStyle: { color: '#fff' },
      left: 'left', bottom: 'bottom'
    },
    series: [{
      name: '修复数量',
      type: 'map',
      map: currentMap.value,
      roam: true,
      emphasis: { label: { show: true, color: '#fff' } },
      data: mapData
    }]
  }
}
    /* ================= */

    const getChart3Option = () => ({
  title: {
    left: 'center',
    textStyle: {
      color: '#fff',
      fontSize: 14
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  series: [
    {
      name: '建筑类型占比',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 28, name: '碉楼', itemStyle: { color: '#00c2ff' } },
        { value: 19, name: '祠堂', itemStyle: { color: '#00ff88' } },
        { value: 16, name: '民居', itemStyle: { color: '#ff6b6b' } },
        { value: 12, name: '宗祠', itemStyle: { color: '#ffd166' } },
        { value: 9, name: '会馆', itemStyle: { color: '#9d4edd' } },
        { value: 8, name: '庙宇', itemStyle: { color: '#4ecdc4' } },
        { value: 7, name: '古塔', itemStyle: { color: '#f9c74f' } },
        { value: 6, name: '牌坊', itemStyle: { color: '#f8961e' } }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      label: {
        color: '#fff',
        formatter: '{b}'
      }
    }
  ]
});

const getChart4Option = () => ({
  title: {
    textStyle: {
      color: '#fff',
      fontSize: 14
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    data: ['修复图片总数', '完成率'],
    textStyle: {
      color: '#fff'
    },
    top: '10%'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '20%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['碉楼', '祠堂', '古塔', '民居', '牌坊', '会馆', '庙宇', '宗祠'],
    axisLine: {
      lineStyle: {
        color: '#4ecdc4',
        width: 2
      }
    },
    axisLabel: {
      color: '#4ecdc4'
    }
  },
  yAxis: [
    {
      type: 'value',
      name: '图片数量',
      nameTextStyle: {
        color: '#4ecdc4',
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: '#4ecdc4',
          width: 2
        }
      },
      axisLabel: {
        color: '#4ecdc4',
        formatter: '{value}'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(78, 205, 196, 0.3)',
          type: 'dashed'
        }
      }
    },
    {
      type: 'value',
      name: '完成率',
      nameTextStyle: {
        color: '#ff6b6b',
        fontSize: 12
      },
      min: 0,
      max: 100,
      axisLine: {
        lineStyle: {
          color: '#ff6b6b',
          width: 2
        }
      },
      axisLabel: {
        color: '#ff6b6b',
        formatter: '{value}%'
      },
      splitLine: {
        show: false // 右侧Y轴不显示网格线，避免重叠
      }
    }
  ],
  series: [
    {
      name: '修复图片总数',
      type: 'bar',
      yAxisIndex: 0,
      data: [120, 80, 30, 70, 25, 40, 35, 50],
      itemStyle: {
        color: '#4ecdc4',
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '40%'
    },
    {
      name: '完成率',
      type: 'bar',
      yAxisIndex: 1,
      data: [90, 85, 70, 80, 75, 88, 82, 86],
      itemStyle: {
        color: '#ff6b6b',
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '40%'
    }
  ]
});

  const getExternalChart1Option = () => ({
  tooltip: { 
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function(params) {
      let result = params[0].name + '<br/>';
      params.forEach(param => {
        if (param.seriesName === '图片数量') {
          result += `${param.seriesName}: ${param.value}<br/>`;
        } else {
          result += `${param.seriesName}: ${param.value} h<br/>`;
        }
      });
      return result;
    }
  },
  toolbox: {
    show: true,
    orient: 'horizontal', // 改为水平排列
    bottom: 0, // 距离底部10px
    left: 'center', // 水平居中
    feature: {
      dataView: { 
        show: true, 
        readOnly: false,
        title: '数据视图',
        lang: ['数据视图', '关闭', '刷新'],
        optionToContent: function(opt) {
          const axisData = opt.xAxis[0].data;
          const series = opt.series;
          let table = '<table style="width:100%; text-align:center; border-collapse: collapse; font-size:12px; line-height:1.6;">';
          // 表头
          table += '<thead><tr style="background:#2c3e50;">';
          table += '<th style="padding:8px 12px; border:1px solid #555; min-width:120px;">数据集名称</th>';
          table += '<th style="padding:8px 12px; border:1px solid #555; min-width:80px;">图片数量</th>';
          table += '<th style="padding:8px 12px; border:1px solid #555; min-width:100px;">平均修复时间(h)</th>';
          table += '</tr></thead>';
          // 表格内容
          table += '<tbody>';
          for (let i = 0; i < axisData.length; i++) {
            table += '<tr>';
            table += `<td style="padding:8px 12px; border:1px solid #555; text-align:left;">${axisData[i]}</td>`;
            table += `<td style="padding:8px 12px; border:1px solid #555;">${series[0].data[i]}</td>`;
            table += `<td style="padding:8px 12px; border:1px solid #555;">${series[1].data[i]}</td>`;
            table += '</tr>';
          }
          table += '</tbody></table>';
          return table;
        }
      },
      magicType: { 
        show: true, 
        type: ['line','bar'],
        title: {
          line: '折线图',
          bar: '柱状图'
        }
      },
      restore: { 
        show: true,
        title: '还原'
      },
      saveAsImage: { 
        show: true,
        title: '保存图片',
        pixelRatio: 2
      }
    },
    iconStyle: {
      borderColor: '#00FFE3'
    },
    emphasis: {
      iconStyle: {
        borderColor: '#FFDC60'
      }
    }
  },
  legend: { 
    data: ['图片数量', '平均修复时间'], 
    textStyle: { color:'#fff' },
    top: '8%'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '15%', // 增加底部间距，为工具箱留出空间
    top: '20%',
    containLabel: true
  },
  xAxis: [{ 
    type:'category', 
    data: ['横州市云表镇伏波庙', '崇左市左江归龙斜塔', '桂林市兴安县灵渠', '百色市西林岑氏家族建筑群', '钦州市灵山县佛子镇大芦古村', '贵港市君子垌客家围屋群', '泉州市鲤城区西街', '福州市鼓楼区中山路'], 
    axisLine: { lineStyle: { color:'#00FFE3' } }, 
    axisLabel: { 
      color:'#ebf8ac',
      rotate: 30,
      interval: 0
    } 
  }],
  yAxis: [
    { 
      type:'value', 
      name:'图片数量', 
      min:0, 
      axisLine: { lineStyle: { color:'#00FFE3' } }, 
      axisLabel: { color:'#2EC7C9' } 
    },
    { 
      type:'value', 
      name:'修复时间(h)', 
      axisLine: { lineStyle: { color:'#FFDC60' } }, 
      axisLabel: { color:'#FFDC60' },
      min: 0,
      max: 5
    }
  ],
  color: ['#00FFE3','#FFDC60'],
  series: [
    { 
      name:'图片数量', 
      type:'bar', 
      data: [120, 80, 30, 70, 25, 40, 35, 50], 
      barBorderRadius: 5,
      barWidth: '40%'
    },
    { 
      name:'平均修复时间', 
      type:'line', 
      yAxisIndex: 1, 
      data: [3.5, 2.8, 4.2, 2.5, 2.0, 3.0, 2.7, 3.2], 
      smooth: true,
      lineStyle: {
        width: 3
      },
      symbolSize: 8,
      symbol: 'circle'
    }
  ]
});

const initMap = async () => {
  try {
    // 先注册地图
    await registerMap(currentMap.value)
    
    if (!mapInstance) {
      mapInstance = echarts.init(mapChart.value)
      chartInstances.push(mapInstance)
    }
    mapInstance.setOption(getMapOption(), true)
  } catch (error) {
    console.error('地图初始化失败:', error)
  }
}

    onMounted(() => {
      console.log('Dashboard 组件已挂载');
      
      setTimeout(() => {
        initCharts();
        initScrollEffect();
      }, 1000);
    });

    onUnmounted(() => {
      console.log('Dashboard 组件已卸载');
      if (scrollInterval) clearInterval(scrollInterval);
      
      chartInstances.forEach(instance => {
        if (instance && typeof instance.dispose === 'function') {
          instance.dispose();
        }
      });
    });

    watch(currentMap, v => {
  console.log('切换到地图：', v)
  initMap()
})

// 生命周期
onMounted(() => {
  initCharts()      // 你原来的其他图
  initMap()         // 地图
  initScrollEffect()
})

    return {
      chart2,
      chart3,
      chart4,
      rankingList,
      externalChart1,
      mapChart,
      currentMap
    };
  }
};
</script>




<style scoped>
/* ========== 仪表板主面板 ========== */
.dashboard-panel {
  height: 100vh;
  padding: 10px;
  box-sizing: border-box;
}

/* ========== 仪表板容器 ========== */
.dashboard {
  display: flex;
  gap: 10px;
  padding: 5px 0 0 0;
  height: 100%;
  min-height: 800px !important;
  box-sizing: border-box;
  margin-top: 5px;
}

/* ========== 左侧区域 - 保持不动 ========== */
.dashboard-left {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 260px;
  min-height: 700px !important;
  margin-left: -10px;
  margin-top: 20px;
  height: auto !important;
}

.dashboard-left .panel-small {
  flex: 2.5 !important;
  min-height: 300px !important;
  height: 300px !important;
}

.dashboard-left .panel-small .chart-container {
  height: 260px !important;
  min-height: 260px !important;
  max-height: none !important;
}

.dashboard-left .panel-large {
  flex: 2 !important;
  min-height: 350px !important;
  height: 350px !important;
}

.dashboard-left .panel-large .chart-container {
  height: 310px !important;
  min-height: 310px !important;
}

/* ========== 中间区域 - 拉长面板，放大地图 ========== */
.dashboard-center {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 8px;
  /* 关键：拉长中间面板 */
  min-height: 650px !important;  /* 从 500px 增大到 650px */
  margin-top: 80px !important;
  margin-bottom: 20px !important;
  height: auto !important;
}

.map-panel {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: none !important;
  border: none !important;
  position: relative;
  overflow: visible;
}

.map-panel::before {
  display: none !important;
}

/* 关键：放大地图 */
.map-panel .chart-container {
  flex: 1;
  position: relative;
  height: 100% !important;
  /* 放大地图 */
  min-height: 550px !important;  /* 从 400px 增大到 550px */
  max-height: 580px !important;  /* 相应增大 */
}

.map-panel select {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9;
}

/* ========== 右侧区域 - 保持不动 ========== */
.dashboard-right {
  flex: 0.9;
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 240px;
  min-height: 700px !important;
  margin-top: 30px !important;
  height: auto !important;
}

.dashboard-right .panel-top {
  flex: none;
  min-height: 200px;
}

.dashboard-right .panel-top .chart-container {
  height: 160px !important;
  min-height: 160px;
}

.dashboard-right .content-panel:nth-child(2) {
  flex: none;
  min-height: 150px;
}

.dashboard-right .realtime-ranking {
  height: 120px !important;
  min-height: 120px;
}

.dashboard-right .content-panel:nth-child(3) {
  flex: 1;
  min-height: 200px;
}

.dashboard-right .content-panel:nth-child(3) .chart-container {
  height: 160px !important;
  min-height: 160px;
}

/* ========== 内容面板通用 ========== */
.content-panel {
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.content-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #00c2ff, #0066ff);
}

.content-panel h3 {
  margin: 0 0 6px 0;
  color: #00c2ff;
  font-size: 13px;
  font-weight: 600;
  text-align: center;
  flex-shrink: 0;
}

.realtime-ranking {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.realtime-ranking ul {
  list-style: none;
  padding: 0;
  margin: 0;
  height: 100%;
}

.realtime-ranking li {
  padding: 4px 8px;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  opacity: 0.7;
}

.realtime-ranking li.active {
  opacity: 1;
  background: rgba(0, 194, 255, 0.1);
  border-left: 3px solid #00c2ff;
}

.rank-item {
  font-weight: 500;
  color: #00f2ff;
}

.rank-time {
  color: #00ff88;
  font-size: 11px;
}

@media (max-width: 1200px) {
  .dashboard {
    flex-direction: column;
    margin-top: 5px;
    min-height: auto !important;
  }
  .dashboard-left,
  .dashboard-center,
  .dashboard-right {
    flex: 1;
    min-width: auto;
    max-width: none;
    margin-left: 0;
    margin-top: 0 !important;
    width: 100%;
    min-height: auto !important;
  }
  .dashboard-center {
    margin-top: 20px !important;
    margin-bottom: 20px !important;
  }
  .dashboard-left .panel-large .chart-container {
    height: 400px !important;
  }
}

@media (max-width: 768px) {
  .dashboard-panel {
    padding: 8px;
  }
  .dashboard {
    gap: 8px;
    margin-top: 0;
    min-height: auto !important;
  }
  .content-panel {
    padding: 8px;
  }
  .content-panel h3 {
    font-size: 12px;
  }
  .map-panel .chart-container {
    height: 400px !important;
    min-height: 400px !important;
  }
}
</style>