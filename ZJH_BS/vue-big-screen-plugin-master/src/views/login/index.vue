<template>
  <div class="login-container">
    <Particles
      id="tsparticles"
      :options="particlesOptions"
      class="particles-bg"
    />
    <div class="login-bg">
      <div class="dynamic-gradient-bg"></div>
      <div class="login-box">
        <div class="login-header">
          <h2 class="title">{{ title }}</h2>
          <p class="subtitle">数据可视化平台登录</p>
        </div>

        <div class="login-form">
          <div class="form-item">
            <div class="input-wrapper">
              <i class="iconfont icon-user"></i>
              <input
                v-model="loginForm.username"
                type="text"
                placeholder="请输入用户名"
                @keyup.enter="handleLogin"
              />
            </div>
          </div>

          <div class="form-item">
            <div class="input-wrapper">
              <i class="iconfont icon-lock"></i>
              <input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                @keyup.enter="handleLogin"
              />
            </div>
          </div>

          <div class="form-item btn-row">
            <button class="login-btn" :disabled="loading" @click="handleLogin">
              {{ loading ? "登录中..." : "登录" }}
            </button>
            <button class="register-btn" type="button" @click="goRegister">
              去注册
            </button>
          </div>

          <div class="demo-info">
            <p>演示账号：admin / 123456</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store";
import { title } from "@/constant/index";

export default defineComponent({
  name: "Login",
  setup() {
    const router = useRouter();
    const userStore = useUserStore();
    const loading = ref(false);

    const loginForm = reactive({
      username: "",
      password: "",
    });

    // 粒子参数
    const particlesOptions = {
      background: {
        color: {
          value: "#222a3a",
        },
      },
      fpsLimit: 60,
      interactivity: {
        events: {
          onClick: { enable: true, mode: "push" },
          onHover: { enable: true, mode: "repulse" },
          resize: true,
        },
        modes: {
          push: { quantity: 4 },
          repulse: { distance: 100, duration: 0.4 },
        },
      },
      particles: {
        color: { value: "#50e3c2" },
        links: {
          color: "#50e3c2",
          distance: 150,
          enable: true,
          opacity: 0.3,
          width: 1,
        },
        collisions: { enable: true },
        move: {
          direction: "none",
          enable: true,
          outModes: { default: "bounce" },
          random: false,
          speed: 2,
          straight: false,
        },
        number: {
          density: { enable: true, area: 800 },
          value: 60,
        },
        opacity: { value: 0.5 },
        shape: { type: "circle" },
        size: { value: { min: 2, max: 5 } },
      },
      detectRetina: true,
    };

    const handleLogin = async () => {
      if (!loginForm.username || !loginForm.password) {
        alert("请输入用户名和密码");
        return;
      }

      loading.value = true;

      try {
        await userStore.login({
          username: loginForm.username,
          password: loginForm.password,
        });

        // 登录成功，跳转到大屏页面
        router.push("/dashboard");
      } catch (error) {
        alert(error instanceof Error ? error.message : "登录失败，请重试");
      } finally {
        loading.value = false;
      }
    };
    // 新增注册跳转方法
    const goRegister = () => {
      router.push("/register");
    };
    return {
      title,
      loginForm,
      loading,
      handleLogin,
      particlesOptions,
      goRegister,
    };
  },
});
</script>

<style lang="scss" scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;

  .particles-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
  }

  .login-bg {
    position: relative;
    width: 100%;
    height: 100%;
    background: url("@/assets/pageBg.png") no-repeat center center;
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;

    .dynamic-gradient-bg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      pointer-events: none;
      opacity: 0.7;
      background: linear-gradient(270deg, #50e3c2, #67a1e5, #764ba2, #50e3c2);
      background-size: 600% 600%;
      animation: gradientMove 16s ease infinite;
    }

    &::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.3);
      z-index: 2;
    }
  }

  .login-box {
    position: relative;
    z-index: 3;
    width: 400px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);

    .login-header {
      text-align: center;
      margin-bottom: 40px;

      .title {
        color: #fff;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
      }

      .subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 16px;
        margin: 0;
      }
    }

    .login-form {
      .form-item {
        margin-bottom: 20px;

        .input-wrapper {
          position: relative;
          display: flex;
          align-items: center;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
          border: 1px solid rgba(255, 255, 255, 0.2);
          padding: 0 15px;
          transition: all 0.3s ease;

          &:focus-within {
            border-color: #50e3c2;
            box-shadow: 0 0 0 2px rgba(80, 227, 194, 0.2);
          }

          i {
            color: rgba(255, 255, 255, 0.7);
            font-size: 18px;
            margin-right: 10px;
          }

          input {
            flex: 1;
            height: 50px;
            background: transparent;
            border: none;
            outline: none;
            color: #fff;
            font-size: 16px;

            &::placeholder {
              color: rgba(255, 255, 255, 0.5);
            }
          }
        }

        .login-btn,
        .register-btn {
        }
        .register-btn {
        }
      }

      .demo-info {
        text-align: center;
        margin-top: 20px;

        p {
          color: rgba(255, 255, 255, 0.6);
          font-size: 14px;
          margin: 0;
        }
      }
    }
    .btn-row {
      display: flex;
      gap: 10px;
      .login-btn,
      .register-btn {
        width: 50%;
        height: 50px;
        background: linear-gradient(45deg, #50e3c2, #67a1e5);
        border: none;
        border-radius: 10px;
        color: #fff;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
      }
      .register-btn {
        background: linear-gradient(45deg, #67a1e5, #50e3c2);
      }
      .login-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
      .login-btn:hover:not(:disabled),
      .register-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(80, 227, 194, 0.4);
      }
    }
  }
}

@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style> 