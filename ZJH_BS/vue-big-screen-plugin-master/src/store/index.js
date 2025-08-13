import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    userInfo: null
  }),
  actions: {
    setLoginStatus(status) {
      this.isLoggedIn = status
    },
    setUserInfo(userInfo) {
      this.userInfo = userInfo
    },
    logout() {
      this.isLoggedIn = false
      this.userInfo = null
    },
    async login({ username, password }) {
      // 模拟登录
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (username === 'admin' && password === '123456') {
            const userInfo = {
              username,
              loginTime: new Date().toISOString()
            }
            this.setLoginStatus(true)
            this.setUserInfo(userInfo)
            resolve(userInfo)
          } else {
            reject(new Error('用户名或密码错误'))
          }
        }, 1000)
      })
    },
    initApp() {
      // Pinia 持久化自动恢复，无需手动 localStorage
    }
  },
  getters: {
    username: (state) => state.userInfo?.username
  },
  persist: true
})
