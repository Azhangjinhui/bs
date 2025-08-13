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
 * 获取中国各省碳排放数据
 * @returns {Promise} 返回中国各省碳排放数据
 */
export const getChinaCarbonData = async () => {
  try {
    const response = await api.get('/api/doris/carbon/dwd_china_provincial_total_carbon_2024')
    return response
  } catch (error) {
    console.error('获取中国碳排放数据失败:', error)
    throw error
  }
}

/**
 * 获取中国各行业碳排放数据
 * @returns {Promise} 返回中国各行业碳排放数据
 */
export const getChinaCarbonSectorData = async () => {
  try {
    const response = await api.get('/api/doris/carbon/dwd_china_carbon_sector_2024')
    return response
  } catch (error) {
    console.error('获取中国行业碳排放数据失败:', error)
    throw error
  }
}
