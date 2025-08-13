<template>
  <div class="map-container" ref="mapRef"></div>
</template>

<script>
import { defineComponent, ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'MapChart',
  props: {
    mapData: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const mapRef = ref(null)
    let mapChart = null
    
    // 初始化地图
    const initMap = async () => {
      if (!mapRef.value) return
      
      // 销毁之前的实例
      if (mapChart) {
        mapChart.dispose()
      }
      
      // 创建新的实例
      mapChart = echarts.init(mapRef.value)
      
      try {
        // 加载中国地图数据
        const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
        const chinaGeoJson = await response.json()
        
        // 注册地图
        echarts.registerMap('china', chinaGeoJson)
        
        // 设置地图配置项
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              console.log('Tooltip params:', params)
              if (params.seriesType === 'map') {
                const data = params.data
                if (data && data.co2_mt) {
                  return `${params.name}<br/>碳排放量: ${data.co2_mt.toFixed(2)} MT<br/>年份: 2024`
                } else {
                  return `${params.name}<br/>碳排放量: ${params.value || 0} MT`
                }
              }
              return `${params.name}<br/>碳排放量: ${params.value || 0} MT`
            },
            backgroundColor: 'rgba(0,0,0,0.8)',
            borderColor: '#00a8ff',
            textStyle: {
              color: '#fff'
            }
          },
          visualMap: {
            min: 0,
            max: 1000,
            left: 'left',
            bottom: '10%',
            text: ['高排放', '低排放'],
            inRange: {
              color: ['#0f1c30', '#1d3b53', '#ff7e00', '#ff4500', '#dc143c']
            },
            textStyle: {
              color: '#cccccc'
            },
            calculable: true,
            formatter: function(value) {
              return value + ' MT'
            }
          },
          series: [
            {
              name: '碳排放数据',
              type: 'map',
              map: 'china',
              aspectScale: 0.75,
              zoom: 1.2,
              roam: true,
              scaleLimit: {
                min: 1,
                max: 3
              },
              itemStyle: {
                normal: {
                  borderColor: '#00a8ff',
                  borderWidth: 1
                },
                emphasis: {
                  areaColor: 'rgba(255,126,0,0.6)',
                  shadowColor: 'rgba(255,126,0,0.8)',
                  shadowBlur: 15,
                  borderWidth: 2
                }
              },
              data: generateCarbonEmissionData(),
              // 确保使用value字段进行染色
              emphasis: {
                itemStyle: {
                  areaColor: 'rgba(255,126,0,0.6)',
                  shadowColor: 'rgba(255,126,0,0.8)',
                  shadowBlur: 15,
                  borderWidth: 2
                }
              }
            }
          ]
        }
        
        // 设置配置项并渲染
        mapChart.setOption(option)
        
      } catch (error) {
        console.error('加载地图数据失败:', error)
        // 如果加载失败，显示一个简单的图表
        showFallbackChart()
      }
      
      // 添加窗口大小变化的监听
      window.addEventListener('resize', handleResize)
    }
    
    // 备用图表显示
    const showFallbackChart = () => {
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '地图数据加载中...',
          left: 'center',
          top: 'middle',
          textStyle: {
            color: '#cccccc',
            fontSize: 18
          }
        },
        series: [
          {
            name: '数据分布',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            data: generateCarbonEmissionData().slice(0, 10),
            itemStyle: {
              borderRadius: 10,
              borderColor: '#00a8ff',
              borderWidth: 2
            },
            label: {
              show: true,
              color: '#cccccc'
            }
          }
        ]
      }
      mapChart.setOption(option)
    }
    
    // 生成碳排放数据 - 确保使用co2_mt值进行染色
const generateCarbonEmissionData = () => {
      console.log('MapChart接收到的数据:', props.mapData)
      console.log('props.mapData长度:', props.mapData ? props.mapData.length : 0)
        // 名称映射以匹配GeoJSON中的区域名称，普通省份自动添加“省”后缀
      const nameMap = {
        '内蒙古': '内蒙古自治区',
        '新疆': '新疆维吾尔自治区',
        '宁夏': '宁夏回族自治区',
        '西藏': '西藏自治区',
        '广西': '广西壮族自治区',
        '北京': '北京市',
        '天津': '天津市',
        '上海': '上海市',
        '重庆': '重庆市'
      }
      if (props.mapData && props.mapData.length > 0) {
        const apiData = props.mapData.map(item => {
          let mappedName = nameMap[item.name]
          // 普通省份添加“省”后缀
          if (!mappedName) {
            mappedName = item.name + '省'
          }
          return {
            name: mappedName,
            value: item.co2_mt,
            co2_mt: item.co2_mt
          }
        })
        console.log('使用API数据进行染色:', apiData)
        return apiData





      }
      
      return []
    }
    
    
    // 处理窗口大小变化
    const handleResize = () => {
      mapChart && mapChart.resize()
    }
    
    // 监听数据变化
    watch(() => props.mapData, () => {
      initMap()
    }, { deep: true })
    
    // 生命周期钩子
    onMounted(() => {
      initMap()
    })
    
    onUnmounted(() => {
      // 移除事件监听
      window.removeEventListener('resize', handleResize)
      // 销毁实例
      if (mapChart) {
        mapChart.dispose()
        mapChart = null
      }
    })
    
    return {
      mapRef
    }
  }
})
</script>

<style lang="scss" scoped>
.map-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>