import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8080',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

/**
 * 获取全球碳排放数据
 * @returns {Promise} 返回碳排放数据
 */
export const getCarbonEmissionData = async () => {
  try {
    const response = await api.get('/api/doris/carbon/dwd_all_country_Total_carbon_2024')
    return response
  } catch (error) {
    console.error('获取碳排放数据失败:', error)
    throw error
  }
}

/**
 * 获取五国碳排放趋势数据（2019-2024）
 * bottomLeft 组件使用的接口
 * @returns {Promise} 返回五国碳排放趋势数据
 * 数据格式: {
 *   total: number,
 *   code: number,
 *   data: [{
 *     area: string,    // 国家名称
 *     co2_mt: number,  // 碳排放量(百万吨)
 *     year: number,    // 年份
 *     id: number,      // ID
 *     sector: string   // 部门(Total表示总计)
 *   }]
 * }
 */
export const getFiveCountryTotalCarbon = async () => {
  try {
    const response = await api.get('/api/doris/carbon/dwd_five_country_Total_carbon_2019_2024')
    return response
  } catch (error) {
    console.error('获取五国碳排放数据失败:', error)
    throw error
  }
}

/**
 * 获取中国碳排放行业分析数据
 * bottomRight 组件使用的接口
 * @returns {Promise} 返回中国碳排放行业分析数据
 * 数据格式: {
 *   total: number,
 *   code: number,
 *   data: [{
 *     area: string,    // 地区(China)
 *     co2_mt: number,  // 碳排放量(百万吨)
 *     year: number,    // 年份
 *     id: number,      // ID
 *     sector: string   // 行业部门
 *   }]
 * }
 */
export const getChinaCarbonSectorData = async () => {
  try {
    const response = await api.get('/api/doris/carbon/dwd_china_carbon_sector_2024')
    return response
  } catch (error) {
    console.error('获取中国碳排放行业数据失败:', error)
    throw error
  }
}

/**
 * 获取碳排放行业列表
 * @returns {Promise} 返回行业列表
 * 数据格式: {
 *   total: number,
 *   code: number,
 *   data: [string] // 行业名称列表
 * }
 */
export const getCarbonSectorList = async () => {
  try {
    // 这里我们使用同一个API，但是会提取出所有唯一的行业名称
    const response = await api.get('/api/doris/carbon/dwd_china_carbon_sector_2024')
    
    if (response && response.code === 200 && response.data) {
      // 提取所有唯一的行业名称
      const sectors = [...new Set(response.data.map(item => item.sector))]
      return {
        code: 200,
        total: sectors.length,
        data: sectors
      }
    }
    
    return response
  } catch (error) {
    console.error('获取碳排放行业列表失败:', error)
    throw error
  }
}

