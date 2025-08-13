<template>
  <div class="bottomRight">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <i class="iconfont icon-chart-bar" style="color: #4a90e2;" />
        </span>
        <div class="d-flex">
          <span class="title-text mx-2">中国碳排放行业分析</span>
        </div>
      </div>
      <div class="chart-container">
        <chart />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Chart from "./chart/index.vue";

export default defineComponent({
  name: 'BottomRightView',
  components: {
    Chart
  }
})
</script>

<style lang="scss" scoped>
$box-height: 520px;
$box-width: 100%;
.bottomRight {
  padding: 14px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  .text {
    color: #c3cbde;
  }
  
  .title-text {
    color: #3fc0fb;
    font-size: 16px;
    font-weight: bold;
  }
  .chart-container {
    padding: 10px 20px;
    height: calc(100% - 60px);
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>