<template>
  <div>
    <Draw :cdata="data" />
  </div>
</template>

<script>
import { defineComponent, reactive, onMounted } from 'vue'
import Draw from './draw.vue'
import { getFiveCountryTotalCarbon } from '@/api/carbon'

export default defineComponent({
  name: 'CarbonEmissionTrend',
  components: {
    Draw
  },
  setup() {
    // 碳排放趋势数据
    const data = reactive({
      years: [],
      countries: [],
      global: []
    })

    // 获取数据
    const fetchData = async () => {
      try {
        const response = await getFiveCountryTotalCarbon()
        console.log('bottomLeft接口数据:', response)
        
        if (response && response.code === 200 && response.data) {
          processChartData(response.data)
        }
      } catch (error) {
        console.error('获取五国碳排放数据失败:', error)
        // 如果接口失败，使用默认数据
        setDefaultData()
      }
    }

    // 处理图表数据
    const processChartData = (apiData) => {
      // 按年份分组数据
      const yearGroups = {}
      const countryColors = {
        '中国': '#ff4757',
        '美国': '#3742fa', 
        '印度': '#2ed573',
        '日本': '#747d8c',
        '德国': '#5f27cd',
        '俄罗斯': '#ff6b6b',
        '英国': '#4834d4',
        '韩国': '#00d2d3',
        '加拿大': '#ff9ff3',
        '法国': '#54a0ff'
      }

      apiData.forEach(item => {
        if (!yearGroups[item.year]) {
          yearGroups[item.year] = {}
        }
        yearGroups[item.year][item.area] = item.co2_mt
      })

      // 获取所有年份并排序
      const years = Object.keys(yearGroups).sort()
      data.years = years

      // 获取所有国家
      const countries = new Set()
      apiData.forEach(item => countries.add(item.area))
      
      // 构建国家数据
      data.countries = Array.from(countries).map(country => {
        const countryData = years.map(year => {
          return yearGroups[year][country] || 0
        })
        
        return {
          name: country,
          color: countryColors[country] || '#95a5a6',
          data: countryData
        }
      })

      // 计算全球总量（所有国家的总和）
      data.global = years.map(year => {
        return Object.values(yearGroups[year] || {}).reduce((sum, value) => sum + value, 0)
      })
    }

    // 设置默认数据（当接口失败时使用）
    const setDefaultData = () => {
      data.years = ['2019', '2020', '2021', '2022', '2023', '2024']
      data.countries = [
        {
          name: '中国',
          color: '#ff4757',
          data: [9825, 9680, 9450, 9180, 8750, 8420]
        },
        {
          name: '美国',
          color: '#3742fa',
          data: [5150, 4820, 4950, 4720, 4580, 4380]
        },
        {
          name: '印度',
          color: '#2ed573',
          data: [2580, 2720, 2890, 3080, 3180, 3280]
        },
        {
          name: '俄罗斯',
          color: '#ff6b6b',
          data: [1580, 1520, 1563, 1540, 1480, 1420]
        },
        {
          name: '日本',
          color: '#747d8c',
          data: [1160, 1120, 1080, 1040, 1000, 960]
        }
      ]
      data.global = [20295, 19862, 20933, 20560, 19990, 19460]
    }

    onMounted(() => {
      fetchData()
    })

    return {
      data
    }
  }
})
</script>