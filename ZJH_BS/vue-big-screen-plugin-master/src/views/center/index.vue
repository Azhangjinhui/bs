<template>
  <div class="center">
    <!-- 地图组件 -->
    <div class="map-wrapper bg-color-black">
      <div class="map-header">
        <span class="map-title">
          <svg class="map-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="22" height="22">
            <path d="M85.333333 469.717333C85.333333 451.829333 99.658667 437.333333 117.333333 437.333333s32 14.506667 32 32.384V786.133333c0 5.962667 4.778667 10.794667 10.666667 10.794667a10.56 10.56 0 0 0 5.045333-1.28l154.848-84.021333a73.898667 73.898667 0 0 1 72.853334 1.290666l252.544 148.842667a10.56 10.56 0 0 0 10.122666 0.341333l213.333334-107.264c3.626667-1.824 5.92-5.568 5.92-9.664V469.717333C874.666667 451.829333 888.992 437.333333 906.666667 437.333333s32 14.506667 32 32.384V745.173333c0 28.682667-16.053333 54.890667-41.44 67.658667l-213.333334 107.264a73.898667 73.898667 0 0 1-70.805333-2.378667L360.533333 768.896a10.56 10.56 0 0 0-10.410666-0.192l-154.848 84.032a73.973333 73.973333 0 0 1-35.285334 8.96c-41.237333 0-74.666667-33.813333-74.666666-75.552V469.717333z m672-132.266666c0 87.808-73.173333 192.917333-217.056 320.288a42.666667 42.666667 0 0 1-56.554666 0C339.829333 530.378667 266.666667 425.258667 266.666667 337.450667 266.666667 203.968 376.64 96 512 96s245.333333 107.968 245.333333 241.450667z m-426.666666 0c0 61.514667 59.712 149.557333 181.333333 259.701333 121.621333-110.144 181.333333-198.186667 181.333333-259.701333C693.333333 239.584 612.277333 160 512 160s-181.333333 79.573333-181.333333 177.450667zM512 405.333333a64 64 0 1 1 0-128 64 64 0 0 1 0 128z" fill="#3fc0fb" />
          </svg>
          全国各省碳排放数据分布图
        </span>
        <div class="map-legend">
          <span class="legend-item">
            <span class="legend-dot" style="background-color: #00e4ff;"></span>
            核心城市
          </span>
          <span class="legend-item">
            <span class="legend-dot" style="background-color: #fffc00;"></span>
            重点区域
          </span>
        </div>
      </div>
      <div class="map-content">
        <dv-border-box-7 :color="['#4a90e2', '#50e3c2']">
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">正在加载数据...</div>
          </div>
          <map-chart v-else :mapData="mapData" />
        </dv-border-box-7>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs, onMounted } from 'vue'
import MapChart from '../center/chart/map'
import { getChinaCarbonData } from '@/api/china-carbon.js'

export default defineComponent({
  name: 'CenterView',
  components: {
    MapChart
  },
  setup() {
    // 响应式数据状态
    const state = reactive({
      mapData: [],
      loading: false,
      error: null
    })

    const { mapData, loading, error } = toRefs(state)

    // 加载中国各省碳排放数据
    const loadChinaCarbonData = async () => {
      try {
        state.loading = true
        state.error = null
        
        const response = await getChinaCarbonData()
        
        if (response.code === 200 && response.data) {
          // 转换API数据为地图显示格式 - 使用co2_mt值进行染色
          state.mapData = response.data.map(item => ({
            name: item.province,
            value: item.co2_mt, // 直接使用co2_mt值进行染色，不四舍五入
            co2_mt: item.co2_mt,
            year: item.year,
            sector: item.sector
          }))
          
          console.log('中国碳排放数据加载成功:', state.mapData)
        } else {
          throw new Error('数据格式错误')
        }
      } catch (error) {
        console.error('加载中国碳排放数据失败:', error)
        state.error = error.message
        
        // 使用默认数据作为备用
        state.mapData = getDefaultMapData()
      } finally {
        state.loading = false
      }
    }

    // 默认数据（作为备用） - 使用真实API数据
    const getDefaultMapData = () => {
      return [
        { name: '北京', value: 115.001836, co2_mt: 115.001836 },
        { name: '天津', value: 200.287836, co2_mt: 200.287836 },
        { name: '上海', value: 128.650125, co2_mt: 128.650125 },
        { name: '重庆', value: 130.853833, co2_mt: 130.853833 },
        { name: '河北', value: 916.242035, co2_mt: 916.242035 },
        { name: '河南', value: 431.237159, co2_mt: 431.237159 },
        { name: '云南', value: 242.908762, co2_mt: 242.908762 },
        { name: '辽宁', value: 455.001458, co2_mt: 455.001458 },
        { name: '黑龙江', value: 196.802888, co2_mt: 196.802888 },
        { name: '湖南', value: 206.261455, co2_mt: 206.261455 },
        { name: '安徽', value: 417.851032, co2_mt: 417.851032 },
        { name: '山东', value: 950.619527, co2_mt: 950.619527 },
        { name: '江苏', value: 805.760727, co2_mt: 805.760727 },
        { name: '浙江', value: 391.920027, co2_mt: 391.920027 },
        { name: '江西', value: 205.059577, co2_mt: 205.059577 },
        { name: '湖北', value: 430.623619, co2_mt: 430.623619 },
        { name: '广西', value: 258.201247, co2_mt: 258.201247 },
        { name: '甘肃', value: 180.646895, co2_mt: 180.646895 },
        { name: '山西', value: 523.999158, co2_mt: 523.999158 },
        { name: '陕西', value: 347.467349, co2_mt: 347.467349 },
        { name: '吉林', value: 177.989757, co2_mt: 177.989757 },
        { name: '福建', value: 267.644802, co2_mt: 267.644802 },
        { name: '贵州', value: 217.038586, co2_mt: 217.038586 },
        { name: '广东', value: 483.131752, co2_mt: 483.131752 },
        { name: '青海', value: 78.196526, co2_mt: 78.196526 },
        { name: '西藏', value: 31.092379, co2_mt: 31.092379 },
        { name: '四川', value: 273.498362, co2_mt: 273.498362 },
        { name: '宁夏', value: 180.974854, co2_mt: 180.974854 },
        { name: '海南', value: 57.382410, co2_mt: 57.382410 },
        { name: '新疆', value: 404.725221, co2_mt: 404.725221 },
        { name: '内蒙古', value: 732.455615, co2_mt: 732.455615 }
      ]
    }

    // 生命周期钩子
    onMounted(async () => {
      await loadChinaCarbonData()
    })

    return {
      mapData,
      loading,
      error
    }
  }
})
</script>

<style lang="scss" scoped>
.center {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  
  // 地图样式
  .map-wrapper {
    margin: 0;
    border-radius: 6px;
    padding: 10px;
    height: 100%;
    width: 100%;
    
    .map-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      
      .map-title {
        font-size: 16px;
        color: #3fc0fb;
        font-weight: bold;
        
        .map-icon {
          margin-right: 5px;
          vertical-align: middle;
        }
      }
      
      .map-legend {
        display: flex;
        
        .legend-item {
          display: flex;
          align-items: center;
          margin-left: 15px;
          font-size: 12px;
          color: #cccccc;
          
          .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
            box-shadow: 0 0 5px currentColor;
          }
        }
      }
    }
    
    .map-content {
      height: calc(100% - 30px);
      width: 100%;
      
      :deep(.dv-border-box-7) {
        width: 100%;
        height: 100%;
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
        align-items: center;
        justify-content: center;
        height: 100%;
        
        .error-text {
          font-size: 14px;
          color: #ff6b6b;
          text-align: center;
        }
      }
    }
  }

}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
