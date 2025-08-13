<template>
  <div class="centerLeft">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <i class="iconfont icon-monitoring" style="color: #3fc0fb;" />
        </span>
        <span class="title-text mx-2">全球碳排放监控</span>
      </div>
      <div class="chart-container">
        <!-- 加载状态 -->
        <div v-if="state.loading" class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">正在加载碳排放数据...</div>
        </div>
        
        <!-- 地球图表 -->
        <div class="earth-chart" ref="earthRef" v-show="!state.loading"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, onUnmounted, reactive } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'
// 导入地球纹理图片
import earthTexture from '@/assets/diqiu.png'
// 导入API服务
import { getCarbonEmissionData as fetchCarbonData } from '@/api/carbon.js'

export default defineComponent({
  name: 'CenterLeftView',
  setup() {
    const earthRef = ref(null)
    let earthChart = null
    let currentDistance = 180 // 当前缩放距离
    
    // 响应式数据状态
    const state = reactive({
      carbonData: [],
      loading: false,
      error: null
    })
    
    // 颜色配置数组
    const colorPalette = [
      '#f00', '#99CC66', '#9999FF', '#339966', 
      '#993366', '#996666', '#66CCFF', '#666666',
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
      '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
    ]
    
    // 获取API数据并转换为地球显示格式
    const loadCarbonData = async () => {
      try {
        state.loading = true
        state.error = null
        
        const response = await fetchCarbonData()
        
        if (response.code === 200 && response.data) {
          // 转换API数据为地球显示格式
          state.carbonData = response.data.map((item, index) => ({
            name: item.area,
            point: [item.longitude, item.latitude, 0],
            itemStyleColor: colorPalette[index % colorPalette.length],
            labelText: `${item.area}•${Math.round(item.co2_mt)}`,
            co2_mt: item.co2_mt,
            year: item.year,
            sector: item.sector
          }))
          
          console.log('碳排放数据加载成功:', state.carbonData)
        } else {
          throw new Error('数据格式错误')
        }
      } catch (error) {
        console.error('加载碳排放数据失败:', error)
        state.error = error.message
        
        // 使用默认数据作为备用
        state.carbonData = getDefaultCarbonData()
      } finally {
        state.loading = false
      }
    }
    
    // 默认数据（作为备用）
    const getDefaultCarbonData = () => {
      return [{
        name: '中国',
        point: [116.46, 39.92, 0],
        itemStyleColor: '#f00',
        labelText: '中国•3000',
        co2_mt: 3000
      }, {
        name: '印度',
        point: [78.96288, 20.593684, 0],
        itemStyleColor: '#99CC66',
        labelText: '印度•500',
        co2_mt: 500
      }, {
        name: '意大利',
        point: [12.56738, 41.87194, 0],
        itemStyleColor: '#9999FF',
        labelText: '意大利•285',
        co2_mt: 285.352214
      }, {
        name: '新西兰',
        point: [174.885971, -40.900557, 0],
        itemStyleColor: '#339966',
        labelText: '新西兰•10',
        co2_mt: 10
      }, {
        name: '英国',
        point: [-3.435973, 55.378051, 0],
        itemStyleColor: '#993366',
        labelText: '英国•1000',
        co2_mt: 1000
      }, {
        name: '德国',
        point: [10.451526, 51.165691, 0],
        itemStyleColor: '#996666',
        labelText: '德国•200',
        co2_mt: 200
      }, {
        name: '美国',
        point: [-95.712891, 37.09024, 0],
        itemStyleColor: '#66CCFF',
        labelText: '美国•2200',
        co2_mt: 2200
      }, {
        name: '日本',
        point: [138.252924, 36.204824, 0],
        itemStyleColor: '#666666',
        labelText: '日本•2500',
        co2_mt: 2500
      }]
    }
    
    // 初始化3D地球 - 使用API数据 + 缩放功能
    const initEarth = () => {
      if (!earthRef.value || state.carbonData.length === 0) return
      
      // 销毁之前的实例
      if (earthChart) {
        earthChart.dispose()
      }
      
      // 创建新的实例
      earthChart = echarts.init(earthRef.value)
      
      // 使用加载的碳排放数据
      const ds = state.carbonData
      
      // 点配置信息 - 所有点保持相同大小
      const series = ds.map(item => {
        return {
          name: item.name, // 是否显示左上角图例
          type: 'scatter3D',
          coordinateSystem: 'globe',
          blendMode: 'lighter',
          symbolSize: 12  , // 所有点位保持相同大小
          
          itemStyle: {
            color: item.itemStyleColor, // 各个点位的颜色设置
            opacity: 0.9, // 透明度
            borderWidth: 2, // 边框宽度
            borderColor: 'rgba(255,255,255,0.8)' // 边框颜色
          },
          label: {
            show: true, // 是否显示字体
            position: 'top', // 字体位置。top、left、right、bottom
            formatter: item.labelText, // 具体显示的值
            textStyle: {
              color: '#fff', // 字体颜色
              borderWidth: 1, // 字体边框宽度
              borderColor: 'rgba(0,0,0,0.8)', // 字体边框颜色
              fontFamily: 'Microsoft YaHei, sans-serif', // 字体格式
              fontSize: 14, // 字体大小
              fontWeight: 600 // 字体加粗
            }
          },
          data: [item.point] // 数据来源
        }
      })
      
      // 添加上面的配置项到地球上 - 完全按照您的示例 + 缩放功能
      const option = {
        // 图例设置
        legend: {
          selectedMode: 'multiple', // 启用多选模式以捕获点击事件
          x: 'right',
          y: 'center',
          data: ds.map(item => {
            return item.name // 数据来源
          }),
          padding: [0, 70, 0, 0], // 填充位置,上、右、下、左 - 往右移动
          orient: 'vertical', // 排列方式，vertical:垂直排列
          itemGap: 8, // 图例项之间的间距
          itemWidth: 14, // 图例标记的宽度
          itemHeight: 14, // 图例标记的高度
          textStyle: {
            color: '#fff', // 文字颜色
            fontSize: 12, // 字体大小
          },
          // 默认所有项都选中
          selected: ds.reduce((acc, item) => {
            acc[item.name] = true
            return acc
          }, {})
        },
       
        // 地球参数设置 + 缩放功能
        globe: {
          baseTexture: earthTexture, // 地球表面覆盖的图片,使用导入的本地资源
          shading: 'color', // 地球中三维图形的着色效果
          viewControl: {
            autoRotate: true, // 是否开启视角绕物体的自动旋转查看
            autoRotateSpeed: 3, // 物体自转的速度,单位为角度 / 秒，默认为10 ，也就是36秒转一圈。
            autoRotateAfterStill: 2, // 在鼠标静止操作后恢复自动旋转的时间间隔,默认 3s
            rotateSensitivity: 2, // 旋转操作的灵敏度，值越大越灵敏.设置为0后无法旋转。[1, 0]只能横向旋转.[0, 1]只能纵向旋转
            targetCoord: [116.46, 39.92], // 定位到北京
            // 缩放功能设置
            maxDistance: 300, // 最大缩放距离
            minDistance: 80,  // 最小缩放距离
            distance: currentDistance, // 当前距离
            zoomSensitivity: 1, // 缩放灵敏度
            panSensitivity: 1,  // 平移灵敏度
            // 启用鼠标滚轮缩放
            enableZoom: true,
            enablePan: true,
            enableRotate: true
          }
        },
        // 地球文字显示信息配置 - 完全按照您的示例
        series: series
      }
      
      // 设置配置项并渲染
      earthChart.setOption(option)
      
      // 临时启用图例选择模式来捕获点击事件
      earthChart.on('legendselectchanged', (params) => {
        console.log('图例点击事件触发:', params)
        
        // 立即恢复所有图例项为选中状态，保持所有点显示
        setTimeout(() => {
          const allSelected = {}
          ds.forEach(item => {
            allSelected[item.name] = true
          })
          
          earthChart.setOption({
            legend: {
              selected: allSelected
            }
          }, false)
        }, 50)
        
        // 找到被点击的国家并跳转
        const clickedCountry = ds.find(item => item.name === params.name)
        if (clickedCountry) {
          console.log('跳转到国家:', clickedCountry.name, clickedCountry.point)
          
          // 跳转到对应的点位置
          earthChart.setOption({
            globe: {
              viewControl: {
                targetCoord: [clickedCountry.point[0], clickedCountry.point[1]],
                distance: 150,
                autoRotate: false,
                autoRotateAfterStill: 3
              }
            }
          }, false)
        }
      })
      
      // 添加鼠标滚轮缩放事件监听
      earthRef.value.addEventListener('wheel', handleWheel, { passive: false })
      
      // 添加窗口大小变化的监听
      window.addEventListener('resize', handleResize)
    }
    
    // 处理鼠标滚轮缩放
    const handleWheel = (event) => {
      event.preventDefault()
      const delta = event.deltaY
      if (delta < 0) {
        // 向上滚动，放大
        currentDistance = Math.max(currentDistance - 20, 80)
      } else {
        // 向下滚动，缩小
        currentDistance = Math.min(currentDistance + 20, 300)
      }
      
      // 更新缩放
      if (earthChart) {
        earthChart.setOption({
          globe: {
            viewControl: {
              distance: currentDistance,
              // 保持其他设置不变
              autoRotate: true,
              autoRotateSpeed: 3,
              autoRotateAfterStill: 2,
              rotateSensitivity: 2,
              targetCoord: [116.46, 39.92],
              maxDistance: 300,
              minDistance: 80,
              // 启用缩放功能
              zoomSensitivity: 1,
              panSensitivity: 1
            }
          }
        })
      }
    }
    
    // 处理窗口大小变化
    const handleResize = () => {
      earthChart && earthChart.resize()
    }
    
    // 生命周期钩子
    onMounted(async () => {
      // 先加载数据，再初始化地球
      await loadCarbonData()
      setTimeout(() => {
        initEarth()
      }, 100)
    })
    
    onUnmounted(() => {
      // 移除事件监听
      if (earthRef.value) {
        earthRef.value.removeEventListener('wheel', handleWheel)
      }
      window.removeEventListener('resize', handleResize)
      // 销毁实例
      if (earthChart) {
        earthChart.dispose()
        earthChart = null
      }
    })
    
    return {
      earthRef,
      state
    }
  }
})
</script>

<style lang="scss" scoped>
$box-height: 410px; // 恢复到原来的标准高度
$box-width: 640px; // 合并后的宽度，占据两个组件的空间

.centerLeft {
  padding: 14px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  
  .text {
    color: #c3cbde;
  }
  
  .title-text {
    color: #3fc0fb;
    font-size: 16px;
    font-weight: bold;
  }
  
  
  .chart-container {
    padding: 10px 20px;
    height: calc(100% - 60px);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    
    .earth-chart {
      width: 100%;
      height: 100%;
      min-height: 280px;
      border-radius: 10px;
      overflow: hidden;
      cursor: grab;
      
      &:active {
        cursor: grabbing;
      }
    }
    
    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #3fc0fb;
      
      .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(63, 192, 251, 0.3);
        border-top: 3px solid #3fc0fb;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 15px;
      }
      
      .loading-text {
        font-size: 14px;
        color: #c3cbde;
      }
    }
    
    .error-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      
      .error-icon {
        font-size: 32px;
        margin-bottom: 10px;
      }
      
      .error-text {
        font-size: 14px;
        color: #ff6b6b;
        text-align: center;
      }
    }
    
    .earth-corner-icon {
      position: absolute;
      top: 20px;
      left: 30px;
      z-index: 10;
      filter: drop-shadow(0 0 4px rgba(0, 0, 0, 0.7));
    }
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
}

// 响应式适配
@media (max-width: 1920px) {
  .centerLeft {
    transform: scale(0.95);
  }
}

@media (max-width: 1440px) {
  .centerLeft {
    transform: scale(0.85);
  }
}

@media (max-width: 1200px) {
  .centerLeft {
    transform: scale(0.75);
  }
}
</style>