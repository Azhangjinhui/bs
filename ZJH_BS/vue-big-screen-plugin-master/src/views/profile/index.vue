<template>
  <div class="card-page">
    <h3>个人信息</h3>
    <div class="profile-avatar">
      <img src="https://api.multiavatar.com/Anime.png" alt="avatar" />
    </div>
    <ul>
      <li>用户名：{{ userStore.username }}</li>
      <li>登录时间：{{ userStore.userInfo?.loginTime }}</li>
      <li>用户角色：管理员</li>
      <li>联系方式：admin@example.com</li>
      <li>登录IP：{{ ipInfo.query || '获取中...' }}</li>
      <li>登录地址：{{ ipInfo.country ? ipInfo.country + '·' + ipInfo.regionName  : '获取中...' }}</li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store'
export default {
  name: 'ProfilePage',
  setup() {
    const userStore = useUserStore()
    const ipInfo = ref({})
    onMounted(async () => {
      try {
        const res = await fetch('http://ip-api.com/json')
        ipInfo.value = await res.json()
      } catch (e) {
        ipInfo.value = { query: '获取失败', country: '', regionName: '', city: '' }
      }
    })
    return { userStore, ipInfo }
  }
}
</script>

<style scoped>
.card-page {
  background: #fff;
  border-radius: 10px;
  padding: 30px 40px;
  min-width: 320px;
  max-width: 480px;
  margin: 0 auto;
}
.card-page h3 {
  margin-bottom: 18px;
  color: #232946;
  text-align: center;
}
.profile-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 18px;
}
.profile-avatar img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  border: 3px solid #e6e6e6;
  background: #fff;
  object-fit: cover;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}
.card-page ul {
  padding-left: 0;
  list-style: none;
}
.card-page li {
  margin-bottom: 10px;
  color: #3e497a;
  font-size: 16px;
}
</style> 