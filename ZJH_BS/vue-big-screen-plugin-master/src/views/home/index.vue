<template>
  <div class="home-page">
    <h2>欢迎来到后台首页</h2>
    <div class="stats">
      <div class="stat-item">今日访问：<span>123</span></div>
      <div class="stat-item">注册用户：<span>456</span></div>
      <div class="stat-item">系统消息：<span>3</span></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style lang="scss" scoped>
.home-page {
  h2 {
    margin-bottom: 30px;
    color: #232946;
  }

  .stats {
    display: flex;
    gap: 40px;

    .stat-item {
      background: #fff;
      border-radius: 10px;
      padding: 24px 40px;
      font-size: 18px;
      color: #232946;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

      span {
        color: #3e497a;
        font-weight: bold;
        font-size: 22px;
        margin-left: 8px;
      }
    }
  }
}
</style>
