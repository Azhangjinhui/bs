<template>
  <div class="layout-container">
    <aside class="sidebar">
      <div class="logo">大屏后台</div>
      <div class="sidebar-avatar">
        <img src="https://img1.baidu.com/it/u=2910909552,2189629152&fm=253&fmt=auto&app=138&f=JPEG?w=200&h=200" alt="avatar" />
      </div>
      <el-menu
        class="el-menu-vertical-demo"
        :default-active="activeIndex"
        background-color="#fff"
        text-color="#232946"
        active-text-color="#36a3f7"
        @open="handleOpen"
        @close="handleClose"
        router
      >
        <el-menu-item index="/dashboard/home">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="screen" @click="openScreen">
          <el-icon><Monitor /></el-icon>
          <span>大屏系统</span>
        </el-menu-item>
        <el-sub-menu index="user">
          <template #title>
            <el-icon><UserFilled /></el-icon>
            <span>个人中心</span>
          </template>
          <el-menu-item index="/dashboard/profile">个人信息</el-menu-item>
          <el-menu-item index="/dashboard/password">修改密码</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/dashboard/data-table">
          <el-icon><i class="iconfont icon-shuju7" /></el-icon>
          <span>数据表格</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/data-analysis">
          <el-icon><i class="iconfont icon-fenxi7" /></el-icon>
          <span>数据分析表</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Monitor, UserFilled } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = ref(route.path)

watch(() => route.path, (val) => {
  activeIndex.value = val
})

const handleOpen = () => {}
const handleClose = () => {}
const openScreen = () => {
  window.open('#/screen', '_blank')
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  background: #f5f7fa;
}
.sidebar {
  width: 220px;
  background: #f5f7fa;
  color: #232946;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0,0,0,0.08);
}
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: bold;
  color: #232946;
  letter-spacing: 2px;
  background: #f5f7fa;
}
.sidebar-avatar {
  background: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  margin: 20px auto 10px auto;
}
.sidebar-avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}
.main-content {
  flex: 1;
  background: #fff;
  padding: 24px;
  overflow: auto;
}
.el-menu-vertical-demo {
  background: #f5f7fa !important;
  color: #232946 !important;
  border-right: none;
}
.el-menu-vertical-demo .el-menu-item.is-active {
  background: #e6f0fa !important;
  color: #36a3f7 !important;
}
.el-menu-vertical-demo .el-menu-item {
  color: #232946 !important;
}
</style> 