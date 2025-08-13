<template>
  <div class="centerRight2">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <i class="iconfont icon-chart-pie-alt" />
        </span>
        <span class="title-text mx-2">碳中和进度监测</span>
      </div>
      <div class="dashboard-container">
        <div class="main-gauge" ref="mainGaugeRef"></div>
        <div class="progress-info">
          <div class="progress-item">
            <div class="progress-label">当前进度</div>
            <div class="progress-value current">{{ currentProgress.toFixed(1) }}%</div>
          </div>
          <div class="progress-item">
            <div class="progress-label">目标年份</div>
            <div class="progress-value target">{{ targetYear }}年</div>
          </div>
          <div class="progress-item">
            <div class="progress-label">剩余时间</div>
            <div class="progress-value remaining">{{ remainingYears }}年</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'CenterRight2View',
  setup() {
    const mainGaugeRef = ref(null)
    let gaugeChart = null
    
    // 获取当前年份
    const currentYear = new Date().getFullYear()
    
    // 目标年份和进度数据
    const targetYear = 2060
    const currentProgress = ref(23)
    
    // 计算剩余年数
    const remainingYears = computed(() => {
      return targetYear - currentYear
    })
    
    // 初始化仪表盘
    const initGauge = () => {
      if (!mainGaugeRef.value) return
      
      // 销毁之前的实例
      if (gaugeChart) {
        gaugeChart.dispose()
      }
      
      // 创建新的实例
      gaugeChart = echarts.init(mainGaugeRef.value)
      
      const option = {
        series: [
          {
            type: 'gauge',
            center: ['50%', '60%'],
            radius: '85%',
            min: 0,
            max: 100,
            splitNumber: 10,
            axisLine: {
              lineStyle: {
                width: 10,
                color: [
                  [0.3, '#ff4757'], // 红色区域 0-30%
                  [0.7, '#ffa726'], // 橙色区域 30-70%
                  [1, '#2ed573']    // 绿色区域 70-100%
                ]
              }
            },
            pointer: {
              itemStyle: {
                color: '#4a90e2'
              }
            },
            axisTick: {
              distance: -10,
              length: 8,
              lineStyle: {
                color: '#fff',
                width: 2
              }
            },
            splitLine: {
              distance: -15,
              length: 15,
              lineStyle: {
                color: '#fff',
                width: 3
              }
            },
            axisLabel: {
              color: '#c3cbde',
              fontSize: 12,
              distance: -25,
              formatter: function (value) {
                return value + '%'
              }
            },
            detail: {
              fontSize: 24,
              fontWeight: 'bold',
              color: '#4a90e2',
              valueAnimation: true,
              formatter: function (value) {
                // 格式化数值，保留一位小数
                return value.toFixed(1) + '%'
              },
              offsetCenter: [0, '25%']
            },
            title: {
              fontSize: 14,
              color: '#c3cbde',
              offsetCenter: [0, '-15%']
            },
            data: [
              {
                value: currentProgress.value,
                name: '全球碳中和进度'
              }
            ]
          }
        ]
      }
      
      gaugeChart.setOption(option)
      
      // 添加窗口大小变化的监听
      window.addEventListener('resize', handleResize)
      
      // 模拟数据更新
      startDataUpdate()
    }
    
    // 模拟数据更新
    const startDataUpdate = () => {
      setInterval(() => {
        // 模拟进度缓慢增长
        if (Math.random() > 0.7) {
          // 增加进度并四舍五入到一位小数，避免长小数
          const increment = 0.1
          currentProgress.value = Math.round((currentProgress.value + increment) * 10) / 10
          currentProgress.value = Math.min(currentProgress.value, 100)
          
          if (gaugeChart) {
            gaugeChart.setOption({
              series: [{
                data: [{
                  value: currentProgress.value,
                  name: '全球碳中和进度'
                }]
              }]
            })
          }
        }
      }, 3000)
    }
    
    // 处理窗口大小变化
    const handleResize = () => {
      gaugeChart && gaugeChart.resize()
    }
    
    // 生命周期钩子
    onMounted(() => {
      setTimeout(() => {
        initGauge()
      }, 100)
    })
    
    onUnmounted(() => {
      // 移除事件监听
      window.removeEventListener('resize', handleResize)
      // 销毁实例
      if (gaugeChart) {
        gaugeChart.dispose()
        gaugeChart = null
      }
    })
    
    return {
      mainGaugeRef,
      currentProgress,
      targetYear,
      remainingYears
    }
  }
})
</script>

<style lang="scss" scoped>
$box-height: 410px;
$box-width: 300px;

.centerRight2 {
  padding: 16px;
  padding-top: 20px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    background: transparent;
    border: none;
  }
  
  .text {
    color: #c3cbde;
  }
  
  .title-text {
    font-size: 16px;
    color: #3fc0fb;
    font-weight: bold;
  }
  
  
  
  .d-flex {
    margin-bottom: 10px;
    flex-shrink: 0;
  }
  
  .dashboard-container {
    flex: 1;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    
    .main-gauge {
      height: 200px;
      width: 100%;
      margin-bottom: 20px;
    }
    
    .progress-info {
      display: flex;
      justify-content: space-between;
      padding: 0 20px;
      
      .progress-item {
        text-align: center;
        
        .progress-label {
          font-size: 12px;
          color: #c3cbde;
          margin-bottom: 6px;
        }
        
        .progress-value {
          font-size: 16px;
          font-weight: bold;
          
          &.current {
            color: #4a90e2;
          }
          
          &.target {
            color: #2ed573;
          }
          
          &.remaining {
            color: #ffa726;
          }
        }
      }
    }
  }
}

// 响应式适配
@media (max-width: 1920px) {
  .centerRight2 {
    transform: scale(0.95);
  }
}

@media (max-width: 1440px) {
  .centerRight2 {
    transform: scale(0.85);
  }
}

@media (max-width: 1200px) {
  .centerRight2 {
    transform: scale(0.75);
  }
}
</style>