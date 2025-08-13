const component = Object.create(null)
/* eslint-disable */
import Echart from './echartCanvas/index'

component.install = function (vue) {
  // ECharts 图表渲染
  vue.component('echart', Echart)
}
export default component
