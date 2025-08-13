<template>
  <div class="bottomLeft">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <i class="iconfont icon-chart-line" style="color: #4a90e2;" />
        </span>
        <div class="d-flex">
          <span class="title-text mx-2">碳排放趋势分析</span>
        </div>
      </div>
      <div>
        <chart />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Chart from "./chart/index";
export default defineComponent({
  name: 'BottomLeftView',
  components: {
    Chart
  }
})
</script>

<style lang="scss" scoped>
$box-height: 520px;
$box-width: 100%;
.bottomLeft {
  padding: 20px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    height: $box-height - 35px;
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
  .chart-box {
    margin-top: 16px;
    width: 170px;
    height: 170px;
    .active-ring-name {
      padding-top: 10px;
    }
  }
}
</style>