<template>
  <div class="tab-panel active dashboard-panel">
    <div class="dashboard">
      <!-- 左侧区域 -->
      <div class="dashboard-left">
        <!-- 修复图片总数及完成率面板 -->
        <div class="content-panel">
          <h3>修复图片总数及完成率</h3>
          <div ref="chart4" class="chart-container" :style="{ height: '350px' }"></div>
        </div>
        <!--数据集来源及修复时间 -->
        <div class="content-panel">
          <h3>数据集来源及修复时间</h3>
          <div ref="externalChart1" class="chart-container" :style="{ height: '350px' }"></div>
        </div>
      </div>

      <!-- 中间区域 - 放置地图模型 -->
      <div class="dashboard-center">
        <div class="content-panel map-panel">
          <div class="map-container" :style="{ height: '720px' }">
            <!-- 这里放置地图组件 -->
            <div ref="mapChart" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- 右侧区域 -->
      <div class="dashboard-right">
        <!-- 建筑类型占比面板 -->
        <div class="content-panel">
          <h3>建筑类型占比</h3>
          <div ref="chart3" class="chart-container" :style="{ height: '200px' }"></div>
        </div>

        <!-- 实时榜单面板 -->
        <div class="content-panel">
          <h3>实时榜单</h3>
          <div class="realtime-ranking" :style="{ height: '200px' }">
            <ul ref="rankingList">
              <li><span class="rank-item">图像001</span><span class="rank-time">用时2.1s</span></li>
              <li><span class="rank-item">图像002</span><span class="rank-time">用时1.8s</span></li>
              <li><span class="rank-item">图像003</span><span class="rank-time">用时2.4s</span></li>
              <li><span class="rank-item">图像004</span><span class="rank-time">用时1.9s</span></li>
              <li><span class="rank-item">图像005</span><span class="rank-time">用时2.2s</span></li>
            </ul>
          </div>
        </div>

        <!-- 建筑地理位置显示面板 -->
        <div class="content-panel">
          <h3>建筑地理位置显示</h3>
          <div ref="chart2" class="chart-container" :style="{ height: '200px' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, onUnmounted, ref, inject } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const echarts = inject('echarts');
    
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

        // 在 initCharts 函数中添加调试
if (mapChart.value) {
  const mapInstance = echarts.init(mapChart.value);
  try {
    const mapOption = getMapOption();
    console.log('地图配置:', mapOption);
    console.log('地图数据:', mapOption.series[0].data);
    
    mapInstance.setOption(mapOption);
    
    // 检查设置后的数据
    setTimeout(() => {
      const currentOption = mapInstance.getOption();
      console.log('当前地图数据:', currentOption.series[0].data);
    }, 1000);
    
    chartInstances.push(mapInstance);
    console.log('地图初始化完成');
  } catch (mapError) {
    console.error('地图初始化失败:', mapError);
  }
}


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

  const getMapOption = () => {
  const mapData = [
    { name: '广东', value: 450 },
    { name: '北京', value: 120 },
    { name: '上海', value: 90 },
    { name: '浙江', value: 180 },
    { name: '江苏', value: 200 },
    { name: '四川', value: 150 },
    { name: '福建', value: 130 },
    { name: '山东', value: 160 },
    { name: '湖北', value: 110 },
    { name: '湖南', value: 100 },
    { name: '河南', value: 95 },
    { name: '河北', value: 85 }
  ];

  console.log('地图数据准备:', mapData);

  return {
    title: {
      text: '图像修复地理位置分布',
      left: 'center',
      textStyle: {
        color: '#fff',
        fontSize: 18
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        console.log('Tooltip参数:', params);
        if (params.data) {
          return `${params.name}<br/>修复数量: ${params.data.value || 0}`;
        }
        return `${params.name}<br/>修复数量: 0`;
      }
    },
    visualMap: {
      type: 'continuous',
      min: 0,
      max: 500,
      text: ['高', '低'],
      realtime: false,
      calculable: true,
      inRange: {
        color: ['#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027']
      },
      textStyle: {
        color: '#fff'
      },
      left: 'left',
      top: 'bottom'
    },
    series: [{
      name: '修复图像数量',
      type: 'map',
      map: 'china',
      roam: true,
      center: [105, 36], // 调整地图中心点位置 [经度, 纬度]
      zoom: 1.5, // 调整地图缩放级别，数值越大显示越大
      emphasis: {
        label: {
          show: true,
          color: '#fff'
        },
        itemStyle: {
          areaColor: '#ff6b6b'
        }
      },
      itemStyle: {
        areaColor: '#2B91B7',
        borderColor: '#00FFFF',
        borderWidth: 1
      },
      data: mapData,
      // 添加名称映射，确保省份名称匹配
      nameMap: {
        '广东省': '广东',
        '北京市': '北京',
        '上海市': '上海',
        '浙江省': '浙江',
        '江苏省': '江苏',
        '四川省': '四川',
        '福建省': '福建',
        '山东省': '山东',
        '湖北省': '湖北',
        '湖南省': '湖南',
        '河南省': '河南',
        '河北省': '河北'
      }
    }]
  };
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
    data: ['粤西碉楼遗产群', '潮汕祠堂影像集', '江门古塔影像集', '江门民居影像集', '江门牌坊影像集', '江门会馆影像集', '江门庙宇影像集', '江门宗祠影像集'], 
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

    return {
      chart2,
      chart3,
      chart4,
      rankingList,
      externalChart1,
      mapChart
    };
  }
};
</script>

<style scoped>
/* 仪表板主面板样式 */
.dashboard-panel {
  height: 100vh; /* 全屏高度 */
}

/* 仪表板容器布局 */
.dashboard {
  display: flex; /* 使用弹性布局 */
  gap: 1rem; /* 子元素间距 */
  padding: 15rem 0 0 0; /* 内边距 */
  height: 100%; /* 继承父容器高度 */
  min-height: 800px; /* 最小高度 */
  box-sizing: border-box; /* 盒模型计算方式 */
}

/* 左侧区域样式 */
.dashboard-left {
  flex: 2; /* 占据2份空间 */
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 280px;
  min-height: 630px;
}

/* 调整左侧内部容器比例 */
.dashboard-left .content-panel:nth-child(1) {
  flex: 1; /* 上面容器占据1份 */
  min-height: 200px; /* 可以设置更小的高度 */
}

.dashboard-left .content-panel:nth-child(2) {
  flex: 2; /* 下面容器占据2份，高度是上面的2倍 */
  min-height: 350px;
}

/* 中间区域样式 */
.dashboard-center {
  flex: 3; /* 占据3份空间 */
  display: flex; /* 弹性布局 */
  flex-direction: column; /* 垂直排列 */
  gap: 1rem; /* 子元素间距 */
  min-height: 725px; /* 最小高度 */
}

/* 右侧区域样式 */
.dashboard-right {
  flex: 1; /* 占据1份空间 */
  display: flex; /* 弹性布局 */
  flex-direction: column; /* 垂直排列 */
  gap: 1rem; /* 子元素间距 */
  min-width: 300px; /* 最小宽度 */
  min-height: 600px; /* 最小高度 */
}

/* 内容面板通用样式 */
.content-panel {
  border-radius: 8px; /* 圆角边框 */
  padding: 1rem; /* 内边距 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* 阴影效果 */
  position: relative; /* 相对定位 */
  overflow: hidden; /* 隐藏溢出内容 */
  flex: 1; /* 弹性填充 */
  display: flex; /* 弹性布局 */
  flex-direction: column; /* 垂直排列 */
}

/* 内容面板顶部装饰线 */
.content-panel::before {
  content: ''; /* 伪元素内容 */
  position: absolute; /* 绝对定位 */
  top: 0; /* 顶部对齐 */
  left: 0; /* 左侧对齐 */
  right: 0; /* 右侧对齐 */
  height: 2px; /* 高度 */
  background: linear-gradient(to right, #00c2ff, #0066ff); /* 渐变背景 */
}

/* 面板标题样式 */
.content-panel h3 {
  margin: 0 0 1rem 0; /* 外边距 */
  color: #00c2ff; /* 文字颜色 */
  font-size: 1.1rem; /* 字体大小 */
  font-weight: 600; /* 字体粗细 */
  text-align: center; /* 文字居中 */
  flex-shrink: 0; /* 禁止收缩 */
}

/* 图表容器样式 */
.chart-container {
  flex: 1; /* 弹性填充 */
  min-height: 180px; /* 最小高度 */
}

/* 实时榜单容器样式 */
.realtime-ranking {
  flex: 1; /* 弹性填充 */
  overflow: hidden; /* 隐藏溢出内容 */
  position: relative; /* 相对定位 */
}

/* 榜单列表样式 */
.realtime-ranking ul {
  list-style: none; /* 去除列表样式 */
  padding: 0; /* 去除内边距 */
  margin: 0; /* 去除外边距 */
  height: 100%; /* 继承父容器高度 */
}

/* 榜单列表项样式 */
.realtime-ranking li {
  padding: 0.8rem 0.5rem; /* 内边距 */
  color: #fff; /* 文字颜色 */
  border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* 底部边框 */
  font-size: 0.9rem; /* 字体大小 */
  display: flex; /* 弹性布局 */
  justify-content: space-between; /* 两端对齐 */
  align-items: center; /* 垂直居中 */
  transition: all 0.3s ease; /* 过渡动画 */
  opacity: 0.7; /* 透明度 */
}

/* 激活状态的榜单项样式 */
.realtime-ranking li.active {
  opacity: 1; /* 不透明 */
  background: rgba(0, 194, 255, 0.1); /* 背景色 */
  border-left: 3px solid #00c2ff; /* 左侧边框 */
}

/* 榜单项目名称样式 */
.rank-item {
  font-weight: 500; /* 字体粗细 */
  color: #00f2ff;
}

/* 榜单时间样式 */
.rank-time {
  color: #00ff88; /* 文字颜色 */
  font-size: 0.8rem; /* 字体大小 */
}

/* 地图面板特殊样式 */
.map-panel {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: none !important; /* 移除阴影边框 */
  border: none !important; /* 移除边框 */
}

/* 移除地图面板的顶部装饰线 */
.map-panel::before {
  display: none !important;
}

.map-container {
  flex: 1;
  position: relative;
  height: 100%;
  min-height: 600px
}

/* 地图图表容器 */
.map-container .chart-container {
  width: 100% !important;
  height: 100% !important;
  min-height: 600px;
}



/* 移动端响应式 */
@media (max-width: 1200px) {
  .dashboard {
    flex-direction: column;
  }
  
  .dashboard-left,
  .dashboard-center,
  .dashboard-right {
    flex: 1;
    min-width: auto;
    min-height: auto;
  }
  
  .map-container {
    height: 500px !important;
    min-height: 500px;
  }
}
</style>