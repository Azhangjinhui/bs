import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import store from './store' // 移除 Vuex
import dataV from '@kjgl77/datav-vue3';
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// 引入 Arco Design Vue
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
// 引入全局css
import './assets/scss/style.scss';
// 引入图表（所有图标见 icon 目录下的 demo_index.html）
import './assets/icon/iconfont.css'
// 引入 全局注册组件
import PublicComponent from '@/components/componentInstall';
import Particles from 'vue3-particles'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(PublicComponent)
app.use(dataV)
app.use(pinia)
app.use(router)
app.use(Particles)
app.use(ElementPlus)
// 注册 Arco
app.use(ArcoVue)
app.mount('#app')
