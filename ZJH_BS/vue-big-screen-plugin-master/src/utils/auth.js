// 认证相关工具函数

/**
 * 检查是否已登录
 */
export const isLoggedIn = () => {
  const loginStatus = localStorage.getItem('isLoggedIn')
  return loginStatus === 'true'
}

/**
 * 获取用户信息
 */
export const getUserInfo = () => {
  const userInfo = localStorage.getItem('userInfo')
  return userInfo ? JSON.parse(userInfo) : null
}

/**
 * 清除登录信息
 */
export const clearAuth = () => {
  localStorage.removeItem('isLoggedIn')
  localStorage.removeItem('userInfo')
}

/**
 * 设置登录信息
 */
export const setAuth = (userInfo) => {
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('userInfo', JSON.stringify(userInfo))
}

/**
 * 模拟登录API
 */
export const loginAPI = (credentials) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (credentials.username === 'admin' && credentials.password === '123456') {
        const userInfo = {
          username: credentials.username,
          loginTime: new Date().toISOString(),
          token: 'mock-token-' + Date.now()
        }
        resolve(userInfo)
      } else {
        reject(new Error('用户名或密码错误'))
      }
    }, 1000)
  })
}

/**
 * 模拟登出API
 */
export const logoutAPI = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve()
    }, 500)
  })
} 