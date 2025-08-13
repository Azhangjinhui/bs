<template>
  <div class="centerRight1">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <i class="iconfont icon-rank" />
        </span>
        <span class="title-text mx-2">碳排放量省份排行榜</span>
      </div>
      <div class="ranking-container">
        <dv-scroll-ranking-board 
          :config="rankingConfig" 
          class="ranking-board"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive, onMounted } from 'vue'
import { getChinaCarbonData } from '@/api/china-carbon.js'

export default defineComponent({
  name: 'CenterRight1View',
  setup() {
    const rankingConfig = reactive({
      data: [],
      unit: 'MT',
      carousel: 'single', // 整页滚动
      rowNum: 10, // 每页显示10行
      waitTime: 1500, // 每页停留1.5秒
      valueFormatter: item => item.value + ' MT',
      // 自定义样式配置
      columnWidths: [50, 150, 100],
      align: ['center', 'left', 'right'],
      // 进度条颜色配置
      colors: ['#ff4757', '#ff6b7a', '#ff7675', '#fd79a8', '#fdcb6e', '#e17055', '#00b894', '#00cec9', '#0984e3', '#6c5ce7']
    })

    const loadRankingData = async () => {
      try {
        const response = await getChinaCarbonData()
        if (response.code === 200 && response.data) {
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
          const list = response.data
            .map(item => {
              const mappedName = nameMap[item.province] || (item.province + '省')
              return {
                name: mappedName,
                value: item.co2_mt
              }
            })
            .sort((a, b) => b.value - a.value)
          rankingConfig.data = list
        } else {
          throw new Error('数据格式错误')
        }
      } catch (error) {
        console.error('获取排行数据失败:', error)
        // 使用默认数据作为备用
        rankingConfig.data = getDefaultRankingData()
      }
    }

    // 默认排行数据（作为备用）
    const getDefaultRankingData = () => {
      return [
        { name: '山东省', value: 950.62 },
        { name: '河北省', value: 916.24 },
        { name: '江苏省', value: 805.76 },
        { name: '内蒙古自治区', value: 732.46 },
        { name: '山西省', value: 524.00 },
        { name: '广东省', value: 483.13 },
        { name: '辽宁省', value: 455.00 },
        { name: '湖北省', value: 430.62 },
        { name: '安徽省', value: 417.85 },
        { name: '新疆维吾尔自治区', value: 404.73 },
        { name: '浙江省', value: 391.92 },
        { name: '陕西省', value: 347.47 },
        { name: '四川省', value: 273.50 },
        { name: '福建省', value: 267.64 },
        { name: '广西壮族自治区', value: 258.20 },
        { name: '云南省', value: 242.91 },
        { name: '贵州省', value: 217.04 },
        { name: '湖南省', value: 206.26 },
        { name: '江西省', value: 205.06 },
        { name: '天津市', value: 200.29 },
        { name: '黑龙江省', value: 196.80 },
        { name: '宁夏回族自治区', value: 180.97 },
        { name: '甘肃省', value: 180.65 },
        { name: '吉林省', value: 177.99 },
        { name: '重庆市', value: 130.85 },
        { name: '上海市', value: 128.65 },
        { name: '北京市', value: 115.00 },
        { name: '青海省', value: 78.20 },
        { name: '海南省', value: 57.38 },
        { name: '西藏自治区', value: 31.09 }
      ]
    }

    onMounted(() => {
      loadRankingData()
    })

    return {
      rankingConfig
    }
  }
})
</script>

<style lang="scss" scoped>
$box-height: 400px;
$box-width: 340px;
.centerRight1 {
  padding: 5px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    padding: 15px;
    height: $box-height;
    width: $box-width;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
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
    margin-bottom: 15px;
    flex-shrink: 0;
  }
  .ranking-container {
    flex: 1;
    padding: 0 10px 10px 10px;
    display: flex;
    align-items: center;

    .ranking-board {
      width: 100%;
      height: 100%;
      max-height: 300px;
    }
  }
}
</style>