<template>
  <div style="width:100%;height:380px;" class="chart-container">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
    <template v-else>
      <div class="chart-left">
        <dv-conical-column-chart :config="currentYearConfig" style="width:100%;height:100%;" />
      </div>
      <div class="chart-right">
        <div ref="radarChartRef" class="radar-chart"></div>
      </div>
      <div class="chart-controls">
        <div class="year-buttons">
          <div 
            v-for="(year, index) in years" 
            :key="year" 
            class="year-button" 
            :class="{ active: activeYearIndex === index }"
            @click="changeYear(index)"
          >
            <div>{{ year }}</div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { defineComponent, reactive, onMounted, ref, computed, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getChinaCarbonSectorData, getCarbonSectorList } from '@/api/carbon'

export default defineComponent({
  name: 'CarbonIndustryChart',
  setup() {
    const radarChartRef = ref(null)
    let radarChart = null
    const loading = ref(true)
    
    // 年份数据
    const years = ['2019', '2020', '2021', '2022', '2023', '2024']
    const activeYearIndex = ref(5) // 默认显示2024年
    
    // 行业列表
    const sectors = ref([])
    
    // 各年份的碳排放行业分布数据
    const yearData = reactive({
      '2019': [],
      '2020': [],
      '2021': [],
      '2022': [],
      '2023': [],
      '2024': []
    })
    
    // 加载行业列表
    const loadSectorList = async () => {
      try {
        const response = await getCarbonSectorList()
        if (response && response.code === 200 && response.data) {
          sectors.value = response.data
        } else {
          // 如果API请求失败，使用默认行业列表
          sectors.value = ['电力', '工业', '地面交通', '住宅', '国内航空', '国际航空']
        }
      } catch (error) {
        console.error('获取行业列表失败:', error)
        // 使用默认行业列表
        sectors.value = ['电力', '工业', '地面交通', '住宅', '国内航空', '国际航空']
      }
    }
    
    // 加载API数据
    const loadSectorData = async () => {
      loading.value = true
      try {
        // 首先加载行业列表
        await loadSectorList()
        
        const response = await getChinaCarbonSectorData()
        if (response && response.code === 200 && response.data) {
          // 按年份分组数据
          const dataByYear = {}
          
          response.data.forEach(item => {
            const year = item.year.toString()
            if (!dataByYear[year]) {
              dataByYear[year] = []
            }
            
            // 计算每个行业的百分比值（这里假设需要转换为百分比）
            // 实际应用中可能需要根据总量计算或直接使用原始数据
            dataByYear[year].push({
              name: item.sector,
              value: parseFloat(item.co2_mt.toFixed(1))
            })
          })
          
          // 更新年份数据
          Object.keys(dataByYear).forEach(year => {
            if (yearData[year]) {
              yearData[year] = dataByYear[year]
            }
          })
          
          // 更新雷达图数据
          updateRadarDataFromAPI(dataByYear)
        }
      } catch (error) {
        console.error('加载中国碳排放行业数据失败:', error)
        // 使用默认数据作为备份
        useDefaultData()
      } finally {
        loading.value = false
      }
    }
    
    // 使用默认数据（当API请求失败时）
    const useDefaultData = () => {
      // 确保sectors有默认值
      if (sectors.value.length === 0) {
        sectors.value = ['电力', '工业', '地面交通', '住宅', '国内航空', '国际航空']
      }
      
      // 默认数据作为备份
      const defaultData = {
        '2019': [
          { name: '电力', value: 48.5 },
          { name: '工业', value: 32.0 },
          { name: '地面交通', value: 12.0 },
          { name: '住宅', value: 6.0 },
          { name: '国内航空', value: 1.0 },
          { name: '国际航空', value: 0.5 }
        ],
        '2020': [
          { name: '电力', value: 47.8 },
          { name: '工业', value: 31.5 },
          { name: '地面交通', value: 12.5 },
          { name: '住宅', value: 6.5 },
          { name: '国内航空', value: 1.2 },
          { name: '国际航空', value: 0.5 }
        ],
        '2021': [
          { name: '电力', value: 46.5 },
          { name: '工业', value: 31.0 },
          { name: '地面交通', value: 13.0 },
          { name: '住宅', value: 7.0 },
          { name: '国内航空', value: 1.5 },
          { name: '国际航空', value: 1.0 }
        ],
        '2022': [
          { name: '电力', value: 45.2 },
          { name: '工业', value: 30.5 },
          { name: '地面交通', value: 13.8 },
          { name: '住宅', value: 7.5 },
          { name: '国内航空', value: 2.0 },
          { name: '国际航空', value: 1.0 }
        ],
        '2023': [
          { name: '电力', value: 43.8 },
          { name: '工业', value: 29.6 },
          { name: '地面交通', value: 14.5 },
          { name: '住宅', value: 8.2 },
          { name: '国内航空', value: 2.5 },
          { name: '国际航空', value: 1.4 }
        ],
        '2024': [
          { name: '电力', value: 42.5 },
          { name: '工业', value: 28.8 },
          { name: '地面交通', value: 15.2 },
          { name: '住宅', value: 8.9 },
          { name: '国内航空', value: 3.1 },
          { name: '国际航空', value: 1.5 }
        ]
      }
      
      // 更新年份数据
      Object.keys(defaultData).forEach(year => {
        if (yearData[year]) {
          yearData[year] = defaultData[year]
        }
      })
      
      // 使用默认雷达图数据
      radarData = {
        '2019': [[75, 100, 50, 35, 20, 30]],
        '2020': [[78, 98, 53, 38, 23, 33]],
        '2021': [[80, 97, 57, 42, 27, 37]],
        '2022': [[85, 95, 60, 45, 30, 40]],
        '2023': [[90, 90, 65, 50, 35, 45]],
        '2024': [[95, 85, 70, 55, 40, 50]]
      }
    }
    
    // 基础配置
    const config = reactive({
      img: [
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="powerGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#powerGrad)" d="M11.5 2L6.5 8h4v6l5-6h-4V2z"/><circle cx="12" cy="18" r="2" fill="url(#powerGrad)" opacity="0.8"/></svg>'), // 电力 - 闪电图标
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="industryGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#industryGrad)" d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"/><rect x="8" y="15" width="2" height="2" fill="url(#industryGrad)" opacity="0.7"/><rect x="14" y="15" width="2" height="2" fill="url(#industryGrad)" opacity="0.7"/></svg>'), // 工业 - 工厂图标
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="transportGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#transportGrad)" d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11C5.84 5 5.28 5.42 5.08 6.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>'), // 地面交通 - 汽车图标
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="houseGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#houseGrad)" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/><rect x="9" y="16" width="2" height="2" fill="url(#houseGrad)" opacity="0.8"/><rect x="13" y="16" width="2" height="2" fill="url(#houseGrad)" opacity="0.8"/></svg>'), // 住宅 - 房屋图标
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="planeGrad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#planeGrad1)" d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/><circle cx="12" cy="12" r="1" fill="url(#planeGrad1)" opacity="0.6"/></svg>'), // 国内航空 - 飞机图标
        'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="planeGrad2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" /><stop offset="100%" style="stop-color:#6cb6ff;stop-opacity:1" /></linearGradient></defs><path fill="url(#planeGrad2)" d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/><path fill="url(#planeGrad2)" d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z" opacity="0.7"/></svg>') // 国际航空 - 飞机图标（带装饰）
      ],
      fontSize: 12,
      imgSide: 'left',
      columnColor: 'rgba(74, 144, 226, 0.8)',
      textColor: '#c3cbde',
      showValue: true,
      valueFormatter: '{value}%'
    })
    
    // 根据当前选中的年份生成配置
    const currentYearConfig = computed(() => {
      return {
        ...config,
        data: yearData[years[activeYearIndex.value]]
      }
    })

    // 碳排放行业雷达图数据
    let radarData = {
      '2019': [[75, 100, 50, 35, 20, 30]],
      '2020': [[78, 98, 53, 38, 23, 33]],
      '2021': [[80, 97, 57, 42, 27, 37]],
      '2022': [[85, 95, 60, 45, 30, 40]],
      '2023': [[90, 90, 65, 50, 35, 45]],
      '2024': [[95, 85, 70, 55, 40, 50]]
    }
    
    // 从API数据更新雷达图数据
    const updateRadarDataFromAPI = (dataByYear) => {
      // 为每个年份更新雷达图数据
      Object.keys(dataByYear).forEach(year => {
        if (!radarData[year]) return
        
        // 创建一个新的雷达图数据数组
        const newRadarData = []
        
        // 根据行业列表映射数据
        sectors.value.forEach((sector, index) => {
          // 查找对应行业的数据
          const sectorData = dataByYear[year].find(item => item.name === sector)
          
          // 如果找到数据，使用其值；否则使用默认值
          const value = sectorData ? 
            // 将实际值映射到0-100的范围（这里使用简单映射，实际应用可能需要更复杂的计算）
            Math.min(100, Math.max(0, sectorData.value * 2)) : 
            (radarData[year][0] && radarData[year][0][index]) || 50
          
          newRadarData.push(value)
        })
        
        // 更新雷达图数据
        radarData[year] = [newRadarData]
      })
    }
    
    // 颜色映射
    const yearColors = {
      '2019': '#9370DB', // 紫色
      '2020': '#3498DB', // 蓝色
      '2021': '#1ABC9C', // 青绿色
      '2022': '#FFD700', // 黄色
      '2023': '#FF8C00', // 橙色
      '2024': '#4CAF50'  // 绿色
    }
    
    // 切换年份
    const changeYear = (index) => {
      activeYearIndex.value = index
      console.log(`切换到年份: ${years[index]}`)
      updateRadarChart()
    }
    
    // 计算总碳排放量
    const calculateTotalEmission = (year) => {
      if (!yearData[year] || yearData[year].length === 0) return 0
      return yearData[year].reduce((sum, item) => sum + item.value, 0)
    }
    
    // 更新雷达图
    const updateRadarChart = () => {
      if (!radarChart) {
        console.warn('雷达图实例不存在，无法更新')
        return
      }
      
      const currentYear = years[activeYearIndex.value]
      const currentColor = yearColors[currentYear]
      
      // 确保数据存在
      if (!radarData[currentYear] || !radarData[currentYear][0]) {
        console.warn(`${currentYear}年数据不存在，无法更新雷达图`)
        return
      }
      
      try {
        const areaColor = currentColor.includes('rgb') ? 
          currentColor.replace(')', ', 0.5)').replace('rgb', 'rgba') :
          currentColor + '80' // 如果是十六进制颜色，添加透明度
          
        console.log(`更新雷达图: ${currentYear}年, 颜色: ${currentColor}, 区域颜色: ${areaColor}`)
        
        radarChart.setOption({
          radar: {
            indicator: sectors.value.map(sector => ({ name: sector, max: 100 }))
          },
          series: [
            {
              name: currentYear,
              type: 'radar',
              lineStyle: {
                width: 2,
                opacity: 0.8,
                color: currentColor
              },
              data: radarData[currentYear] || [[50, 50, 50, 50, 50, 50]], // 确保有默认数据
              symbol: 'none',
              itemStyle: {
                color: currentColor
              },
              areaStyle: {
                opacity: 0.5,
                color: areaColor
              }
            }
          ]
        })
      } catch (error) {
        console.error('更新雷达图时出错:', error)
      }
    }
    
    // 初始化雷达图
    const initRadarChart = () => {
      if (!radarChartRef.value) {
        console.warn('雷达图DOM元素不存在，无法初始化')
        return
      }
      
      try {
        // 确保在DOM更新后初始化图表
        radarChart = echarts.init(radarChartRef.value)
        
        // 使用当前选中的年份（默认2024年）
        const currentYear = years[activeYearIndex.value]
        const currentColor = yearColors[currentYear]
        
        const option = {
          backgroundColor: 'transparent',
          title: {
            left: 'center',
            top: 0,
            textStyle: {
              color: '#c3cbde',
              fontSize: 10
            }
          },
          tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(14, 29, 52, 0.85)',
            borderColor: '#4a90e2',
            borderWidth: 1,
            textStyle: {
              color: '#fff',
              fontSize: 12
            },
            formatter: function(params) {
              const currentYear = years[activeYearIndex.value];
              const values = params.value;
              
              let html = `<div style="font-weight:bold;color:#4a90e2;margin-bottom:5px;font-size:14px;">${currentYear}年碳排放指数</div>`;
              html += '<table style="width:100%">';
              
              sectors.value.forEach((name, index) => {
                // 查找对应行业的实际碳排放量
                const sectorData = yearData[currentYear].find(item => item.name === name);
                const actualValue = sectorData ? sectorData.value : '暂无数据';
                const indexValue = values[index];
                
                html += `
                  <tr>
                    <td style="padding:3px 10px 3px 0;color:#c3cbde;">${name}:</td>
                    <td style="padding:3px 0;text-align:right;color:#fff;">${indexValue}</td>
                    <td style="padding:3px 0 3px 10px;text-align:right;color:#4a90e2;">${actualValue} Mt</td>
                  </tr>
                `;
              
              });
              
              html += '</table>';
              
              // 添加总排放量
              const totalEmission = calculateTotalEmission(currentYear);
              if (totalEmission > 0) {
                html += `<div style="margin-top:5px;padding-top:5px;border-top:1px dashed rgba(74, 144, 226, 0.5);text-align:right;">
                  <span style="color:#c3cbde;">总排放量:</span> 
                  <span style="color:#4CAF50;font-weight:bold;">${totalEmission.toFixed(1)} Mt</span>
                </div>`;
              }
              
              return html;
            }
          },
          radar: {
            indicator: sectors.value.map(sector => ({ name: sector, max: 100 })),
            shape: 'circle',
            splitNumber: 5,
            axisName: {
              color: 'rgb(74, 144, 226)'
            },
            splitLine: {
              lineStyle: {
                color: [
                  'rgba(74, 144, 226, 0.1)',
                  'rgba(74, 144, 226, 0.2)',
                  'rgba(74, 144, 226, 0.4)',
                  'rgba(74, 144, 226, 0.6)',
                  'rgba(74, 144, 226, 0.8)',
                  'rgba(74, 144, 226, 1)'
                ].reverse()
              }
            },
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: 'rgba(74, 144, 226, 0.5)'
              }
            }
          },
          series: [
            {
              name: currentYear,
              type: 'radar',
              lineStyle: {
                width: 2,
                opacity: 0.8,
                color: currentColor
              },
              data: radarData[currentYear] || [[95, 85, 70, 55, 40, 50]], // 确保有默认数据
              symbol: 'none',
              itemStyle: {
                color: currentColor
              },
              areaStyle: {
                opacity: 0.5,
                color: currentColor.includes('rgb') ? 
                  currentColor.replace(')', ', 0.5)').replace('rgb', 'rgba') :
                  currentColor + '80' // 如果是十六进制颜色，添加透明度
              }
            }
          ]
        }
        
        radarChart.setOption(option)
        console.log(`雷达图初始化完成，当前年份: ${currentYear}, 颜色: ${currentColor}`)
        
        window.addEventListener('resize', () => {
          radarChart && radarChart.resize()
        })
      } catch (error) {
        console.error('初始化雷达图时出错:', error)
      }
    }
    
    onMounted(() => {
      // 加载API数据
      loadSectorData().then(() => {
        // 确保默认显示2024年数据
        activeYearIndex.value = 5
        // 初始化雷达图
        nextTick(() => {
          initRadarChart()
          // 确保雷达图显示2024年的数据和样式
          setTimeout(() => {
            updateRadarChart()
          }, 100)
        })
      })
    })
    
    // 监听年份变化
    watch(activeYearIndex, () => {
      updateRadarChart()
    })
    
    return {
      currentYearConfig,
      radarChartRef,
      years,
      activeYearIndex,
      changeYear,
      loading,
      sectors
    }
  }
})
</script>

<style scoped>
.chart-container {
  display: flex;
  width: 100%;
  height: 100%;
  position: relative;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(74, 144, 226, 0.3);
  border-radius: 50%;
  border-top-color: #4a90e2;
  animation: spin 1s ease-in-out infinite;
}

.loading-text {
  margin-top: 10px;
  color: #c3cbde;
  font-size: 14px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.chart-controls {
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  height: 0px;
  z-index: 10;
}

.year-buttons {
  display: flex;
  background: rgba(14, 29, 52, 0.7);
  border-radius: 4px;
  padding: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.year-button {
  padding: 5px 16px;
  cursor: pointer;
  color: #c3cbde;
  font-size: 16px;
  transition: all 0.3s;
  border-radius: 6px;
  margin: 0 35px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60px;
}

.year-button.active {
  background: #4a90e2;
  color: #fff;
  font-weight: bold;
}

.year-button:hover:not(.active) {
  background: rgba(74, 144, 226, 0.3);
}

.chart-left {
  flex: 1;
  height: 100%;
  width: 70%;
}

.chart-right {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 35%;
  height: 55%;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}

.radar-chart {
  width: 100%;
  height: 100%;
}
</style>
