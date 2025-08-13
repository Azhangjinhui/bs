<template>
  <div>
    <div ref="chartRef" style="height: 450px; width: 100%;"></div>
  </div>
</template>

<script>
import { defineComponent, watch, ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'CarbonTrendDraw',
  props: {
    cdata: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const chartRef = ref()
    let chartInstance = null
    
    const initChart = async (options) => {
      await nextTick()
      
      if (!chartRef.value) return
      
      // 销毁之前的实例
      if (chartInstance) {
        chartInstance.dispose()
      }
      
      // 创建新的实例
      chartInstance = echarts.init(chartRef.value)
      chartInstance.setOption(options)
    }
    
    const handleResize = () => {
      if (chartInstance) {
        chartInstance.resize()
      }
    }

    // 监听数据变化
    watch(
      () => props.cdata,
      async (val) => {
        if (!val || !val.countries || !val.years) return
        
        const options = {
          title: {
            text: '全球主要国家碳排放趋势',
            textStyle: {
              color: '#c3cbde',
              fontSize: 18,
              fontWeight: 'bold'
            },
            left: 'center',
            top: 10
          },
          tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(0,0,0,0.85)',
            borderColor: 'rgba(74, 144, 226, 0.8)',
            borderWidth: 2,
            textStyle: {
              color: '#fff',
              fontSize: 12
            },
            formatter: function(params) {
              // 如果只有一个数据点，说明是悬浮在线条上
              if (params.length === 1) {
                const param = params[0];
                const value = typeof param.value === 'number' ? param.value.toFixed(2) : param.value;
                return `
                  <div style="padding:8px;">
                    <div style="font-weight:bold;margin-bottom:8px;color:#4a90e2;font-size:15px;">
                      ${param.name}年
                    </div>
                    <div style="display:flex;align-items:center;margin:6px 0;">
                      <span style="display:inline-block;width:12px;height:12px;background:${param.color};margin-right:10px;border-radius:50%;border:2px solid #fff;"></span>
                      <span style="color:#fff;font-size:14px;font-weight:bold;">${param.seriesName}</span>
                    </div>
                    <div style="margin-top:8px;text-align:center;">
                      <span style="font-weight:bold;color:#4a90e2;font-size:16px;">${value}</span>
                      <span style="color:#c3cbde;font-size:12px;margin-left:4px;">百万吨CO₂</span>
                    </div>
                  </div>
                `;
              }
              
              // 多个数据点，说明是悬浮在空白处，显示所有国家数据
              let result = `<div style="font-weight:bold;margin-bottom:8px;color:#4a90e2;font-size:14px;">${params[0].name}年 碳排放数据</div>`;
              
              // 按数值大小排序显示
              const sortedParams = params.sort((a, b) => b.value - a.value);
              
              sortedParams.forEach(item => {
                const value = typeof item.value === 'number' ? item.value.toFixed(2) : item.value;
                result += `<div style="display:flex;align-items:center;margin:6px 0;padding:2px 0;">
                  <span style="display:inline-block;width:10px;height:10px;background:${item.color};margin-right:10px;border-radius:50%;border:1px solid #fff;"></span>
                  <span style="min-width:70px;color:#fff;font-size:12px;">${item.seriesName}:</span>
                  <span style="font-weight:bold;color:#4a90e2;margin-left:8px;font-size:13px;">${value} 百万吨CO₂</span>
                </div>`;
              });
              
              return result;
            }
          },
          legend: {
            data: val.countries.map(c => c.name),
            textStyle: {
              color: '#c3cbde',
              fontSize: 12
            },
            top: 45,
            icon: 'circle',
            itemWidth: 12,
            itemHeight: 12
          },
          grid: {
            left: '5%',
            right: '5%',
            bottom: '8%',
            top: '85px',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: val.years,
            axisLine: {
              lineStyle: {
                color: '#c3cbde',
                width: 2
              }
            },
            axisLabel: {
              color: '#c3cbde',
              fontSize: 11,
              formatter: '{value}年'
            },
            axisTick: {
              show: true,
              lineStyle: {
                color: '#c3cbde'
              }
            }
          },
          yAxis: {
            type: 'value',
            name: '碳排放量 (百万吨CO₂)',
            min: 0,
            max: 40000,
            interval: 5000,
            nameTextStyle: {
              color: '#c3cbde',
              fontSize: 12,
              padding: [0, 0, 0, 50]
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: '#c3cbde',
                width: 2
              }
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(195, 203, 222, 0.3)',
                type: 'dashed'
              }
            },
            axisLabel: {
              color: '#c3cbde',
              fontSize: 11,
              formatter: '{value}'
            }
          },
          series: [
            // 各国碳排放数据
            ...val.countries.map(country => {
              return {
                name: country.name,
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 6,
                showSymbol: true,
                lineStyle: {
                  width: 3,
                  color: country.color
                },
                itemStyle: {
                  color: country.color,
                  borderWidth: 2,
                  borderColor: '#fff'
                },
                areaStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {
                      offset: 0,
                      color: echarts.color.modifyAlpha(country.color, 0.4)
                    },
                    {
                      offset: 1,
                      color: echarts.color.modifyAlpha(country.color, 0.05)
                    }
                  ])
                },
                data: country.data,
                emphasis: {
                  focus: 'series'
                }
              }
            })
          ]
        }
        
        await initChart(options)
      },
      {
        immediate: true,
        deep: true
      }
    )
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      
      // 延迟初始化确保数据已加载
      setTimeout(() => {
        if (props.cdata) {
          // 手动触发watch
          const event = new CustomEvent('dataReady')
          window.dispatchEvent(event)
        }
      }, 200)
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
      }
    })
    
    return {
      chartRef
    }
  }
})
</script>