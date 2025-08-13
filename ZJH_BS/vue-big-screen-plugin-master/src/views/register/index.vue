<template>
  <div class="register-container">
    <div class="register-box">
      <h2 class="title">注册新账号</h2>
      <div class="register-form">
        <div class="form-item">
          <input v-model="form.username" type="text" placeholder="请输入用户名" />
        </div>
        <div class="form-item">
          <input v-model="form.password" type="password" placeholder="请输入密码" />
        </div>
        <div class="form-item">
          <input v-model="form.confirmPassword" type="password" placeholder="请确认密码" />
        </div>
        <div class="form-item">
          <button class="register-btn" :disabled="loading" @click="handleRegister">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
        <div class="form-item">
          <button class="login-btn" type="button" @click="goLogin">返回登录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Register',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const form = reactive({
      username: '',
      password: '',
      confirmPassword: ''
    })

    const handleRegister = async () => {
      if (!form.username || !form.password || !form.confirmPassword) {
        alert('请填写完整信息')
        return
      }
      if (form.password !== form.confirmPassword) {
        alert('两次密码输入不一致')
        return
      }
      loading.value = true
      setTimeout(() => {
        alert('注册成功！请登录')
        loading.value = false
        router.push('/login')
      }, 1000)
    }
    const goLogin = () => {
      router.push('/login')
    }
    return {
      form,
      loading,
      handleRegister,
      goLogin
    }
  }
})
</script>

<style lang="scss" scoped>
.register-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #50e3c2 0%, #67a1e5 100%);
}
.register-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  text-align: center;
}
.title {
  color: #fff;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 30px;
}
.register-form {
  .form-item {
    margin-bottom: 20px;
    input {
      width: 100%;
      height: 45px;
      border-radius: 10px;
      border: none;
      padding: 0 15px;
      font-size: 16px;
      background: rgba(255,255,255,0.2);
      color: #fff;
      outline: none;
      &::placeholder {
        color: rgba(255,255,255,0.6);
      }
    }
    .register-btn, .login-btn {
      width: 100%;
      height: 45px;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-weight: bold;
      color: #fff;
      cursor: pointer;
      transition: all 0.3s;
    }
    .register-btn {
      background: linear-gradient(45deg, #67a1e5, #50e3c2);
      margin-bottom: 10px;
      &:hover:not(:disabled) {
        box-shadow: 0 4px 12px rgba(80, 227, 194, 0.4);
        transform: translateY(-2px);
      }
      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
    .login-btn {
      background: linear-gradient(45deg, #50e3c2, #67a1e5);
      &:hover {
        box-shadow: 0 4px 12px rgba(80, 227, 194, 0.4);
        transform: translateY(-2px);
      }
    }
  }
}
</style> 