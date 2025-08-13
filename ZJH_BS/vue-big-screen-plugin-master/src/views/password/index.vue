<template>
  <div class="card-page">
    <h3>修改密码</h3>
    <form @submit.prevent="handleChangePwd">
      <div class="form-item">
        <input v-model="form.oldPwd" type="password" placeholder="原密码" />
      </div>
      <div class="form-item">
        <input v-model="form.newPwd" type="password" placeholder="新密码" />
      </div>
      <div class="form-item">
        <input v-model="form.confirmPwd" type="password" placeholder="确认新密码" />
      </div>
      <div class="form-item">
        <button class="save-btn" type="submit">保存</button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'PasswordPage',
  setup() {
    const form = ref({ oldPwd: '', newPwd: '', confirmPwd: '' })
    const handleChangePwd = () => {
      if (!form.value.oldPwd || !form.value.newPwd || !form.value.confirmPwd) {
        alert('请填写完整')
        return
      }
      if (form.value.newPwd !== form.value.confirmPwd) {
        alert('两次新密码不一致')
        return
      }
      // 这里只做演示
      alert('密码修改成功！')
      form.value.oldPwd = ''
      form.value.newPwd = ''
      form.value.confirmPwd = ''
    }
    return { form, handleChangePwd }
  }
}
</script>

<style lang="scss" scoped>
.card-page {
  background: #fff;
  border-radius: 10px;
  padding: 30px 40px;
  min-width: 320px;
  max-width: 480px;
  margin: 0 auto;
  
  h3 {
    margin-bottom: 18px;
    color: #232946;
  }
  
  form {
    .form-item {
      margin-bottom: 18px;
      
      input {
        width: 100%;
        height: 40px;
        border-radius: 8px;
        border: 1px solid #eee;
        padding: 0 12px;
        font-size: 15px;
      }
    }
    
    .save-btn {
      width: 100%;
      height: 40px;
      background: linear-gradient(45deg, #67a1e5, #50e3c2);
      border: none;
      border-radius: 8px;
      color: #fff;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        box-shadow: 0 4px 12px rgba(80, 227, 194, 0.2);
        transform: translateY(-2px);
      }
    }
  }
}
</style>
