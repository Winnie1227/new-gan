//文档内容已复制进Dashboard.vue，该文档已可安全删除

// window.initDashboardCharts = function() {
//   console.log('开始初始化外部图表...');

//   // 添加安全检查
//   if (typeof echarts === 'undefined') {
//     console.error('ECharts 未加载');
//     return;
//   }

//   // 依次初始化图表，如果容器不存在则跳过
//   initChart1();
//   initChart2();
//   initChart3();
//   initChart4();

//   function initChart1() {
//     const container = document.getElementById('external-chart1');
//     if (!container) {
//       console.warn('external-chart1 容器未找到，跳过初始化');
//       return;
//     }

//     try {
//       var myChart = echarts.init(container);
//       const images = ['图像1','图像2','图像3','图像4','图像5','图像6'];
//       const psnr = [28.4, 27.1, 26.5, 25.0, 24.2, 22.8];
//       const ssim = [0.82, 0.80, 0.78, 0.75, 0.72, 0.68];
//       const lpips = [0.148, 0.155, 0.160, 0.172, 0.185, 0.200];

//       const option = {
//         tooltip: { trigger: 'axis' },
//         toolbox: {
//           show: true,
//           feature: {
//             dataView: { show: true, readOnly: false },
//             magicType: { show: true, type: ['line','bar'] },
//             restore: { show: true },
//             saveAsImage: { show: true }
//           }
//         },
//         legend: { data: ['PSNR','SSIM','LPIPS'], textStyle: { color:'#fff' } },
//         xAxis: [{ type:'category', data:images, axisLine:{lineStyle:{color:'#01FCE3'}}, axisLabel:{color:'#ebf8ac'} }],
//         yAxis: [
//           { type:'value', name:'PSNR / SSIM', min:0, axisLine:{lineStyle:{color:'#01FCE3'}}, axisLabel:{color:'#2EC7C9'} },
//           { type:'value', name:'LPIPS', axisLine:{lineStyle:{color:'#01FCE3'}}, axisLabel:{color:'#2EC7C9'} }
//         ],
//         color: ['#00FFE3','#C1B2EA','#FFDC60'],
//         series: [
//           { name:'PSNR', type:'bar', data:psnr, barBorderRadius:5 },
//           { name:'SSIM', type:'bar', data:ssim, barBorderRadius:5 },
//           { name:'LPIPS', type:'line', yAxisIndex:1, data:lpips, smooth:true }
//         ]
//       };
//       myChart.setOption(option);
//       window.addEventListener('resize', () => myChart.resize());
//       console.log('external-chart1 初始化成功');
//     } catch (error) {
//       console.error('external-chart1 初始化失败:', error);
//     }
//   }

//   function initChart2() {
//     const container = document.getElementById('external-chart2');
//     if (!container) {
//       console.warn('external-chart2 容器未找到，跳过初始化');
//       return;
//     }

//     try {
//       var myChart = echarts.init(container);
//       const models = ['ModelZ','ModelY','ModelX','RealESRGAN','ESRGAN'];
//       const mos = [1550,1500,1450,1400,1350];
//       const color = ['#8d7fec','#5085f2','#e75fc3','#f87be2','#f2719a'];
//       const data = models.map((m,i) => ({ name:m, value:mos[i] }));

//       const option = {
//         tooltip: { trigger:'item', formatter:'{b}: {c} (Elo)' },
//         legend: { bottom:0, textStyle:{color:'#fff'} },
//         color,
//         series:[{
//           name:'Model Avg MOS',
//           type:'pie',
//           radius:['40%','70%'],
//           data,
//           label:{ color:'#fff', formatter:'{b}: {d}%' }
//         }]
//       };
//       myChart.setOption(option);
//       myChart.on('mouseover', params => myChart.dispatchAction({ type:'highlight', seriesIndex:0, dataIndex:0 }));
//       window.addEventListener('resize', () => myChart.resize());
//       console.log('external-chart2 初始化成功');
//     } catch (error) {
//       console.error('external-chart2 初始化失败:', error);
//     }
//   }

//   function initChart3() {
//     const container = document.getElementById('external-chart3');
//     if (!container) {
//       console.warn('external-chart3 容器未找到，跳过初始化');
//       return;
//     }

//     try {
//       var myChart = echarts.init(container);
//       const models = ['ModelZ','ModelY','ModelX','RealESRGAN','ESRGAN'];
//       const mos = [1550,1500,1450,1400,1350];
//       const color = ['#FEE449','#00FFFF','#00FFA8','#9F17FF','#FFE400'];
//       const data = models.map((m,i) => ({ name:m, value: mos[i] }));

//       const option = {
//         legend:{ orient:'vertical', left:'left', textStyle:{color:'#fff'}, data:models, icon:'circle' },
//         series:[{
//           name:'模型占比',
//           type:'pie',
//           roseType:'radius',
//           radius:['20%','70%'],
//           center:['50%','50%'],
//           data,
//           label:{ color:'#fff', formatter:'{b}: {d}%' },
//           labelLine:{ length:10, length2:10 }
//         }]
//       };
//       myChart.setOption(option);
//       window.addEventListener('resize', () => myChart.resize());
//       console.log('external-chart3 初始化成功');
//     } catch (error) {
//       console.error('external-chart3 初始化失败:', error);
//     }
//   }

//   function initChart4() {
//     const container = document.getElementById('external-chart4');
//     if (!container) {
//       console.warn('external-chart4 容器未找到，跳过初始化');
//       return;
//     }
    
//     try {
//       var myChart = echarts.init(container);
//       const models = ['ModelZ','ModelY','ModelX','RealESRGAN','ESRGAN'];
//       const mos = [1550,1500,1450,1400,1350];
//       const lpips = [0.148,0.155,0.160,0.172,0.185];
//       const colors = ['rgb(46,199,201)','rgb(90,177,239)','rgb(255,185,128)'];

//       const option = {
//         tooltip:{ trigger:'axis', axisPointer:{ type:'cross' } },
//         legend:{ data:['MOS Elo','LPIPS'], textStyle:{color:'#fff'} },
//         xAxis:[{ type:'category', data:models, axisLine:{ lineStyle:{color:'#fff'} } }],
//         yAxis:[
//           { type:'value', name:'MOS(Elo)', axisLine:{lineStyle:{color:colors[0]}}, axisLabel:{formatter:'{value}'} },
//           { type:'value', name:'LPIPS', position:'right', offset:50, axisLine:{lineStyle:{color:colors[1]}}, axisLabel:{formatter:'{value}'} }
//         ],
//         color: colors,
//         series:[
//           { name:'MOS Elo', type:'bar', data:mos },
//           { name:'LPIPS', type:'line', yAxisIndex:1, data:lpips, smooth:true }
//         ]
//       };
//       myChart.setOption(option);
//       window.addEventListener('resize', () => myChart.resize());
//       console.log('external-chart4 初始化成功');
//     } catch (error) {
//       console.error('external-chart4 初始化失败:', error);
//     }
//   }

//   console.log('所有图表初始化完成');
// };