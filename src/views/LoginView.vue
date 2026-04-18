<template>
  <div class="login-page">
    <div class="login-header">
      <div class="logo">🦆</div>
      <h1>识盘鸭</h1>
      <p class="subtitle">股票学习小助手</p>
    </div>
    <div class="login-form">
      <van-field
        v-model="phone"
        type="tel"
        label="手机号"
        placeholder="请输入11位手机号"
        maxlength="11"
        clearable
        :error-message="errorMsg"
        @keyup.enter="handleLogin"
      />
      <van-button
        type="primary"
        block
        round
        :loading="loading"
        :disabled="phone.length !== 11"
        @click="handleLogin"
        class="login-btn"
      >
        登录
      </van-button>
      <p class="tip">输入手机号即可登录，无需密码</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { showToast } from 'vant'

const router = useRouter()
const userStore = useUserStore()
const phone = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  if (!/^1[3-9]\d{9}$/.test(phone.value)) {
    errorMsg.value = '请输入正确的11位手机号'
    return
  }
  errorMsg.value = ''
  loading.value = true
  try {
    await userStore.loginWithPhone(phone.value)
    router.push('/')
  } catch (e: any) {
    showToast(e.message || '登录失败')
  } finally {
    loading.value = false
  }
}

// 如果已登录直接跳转
if (userStore.isLoggedIn) {
  router.push('/')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
}
.login-header {
  text-align: center;
  margin-bottom: 40px;
}
.logo {
  font-size: 64px;
  margin-bottom: 8px;
}
h1 {
  color: #fff;
  font-size: 28px;
  margin: 0;
}
.subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin-top: 4px;
}
.login-form {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  width: 85%;
  max-width: 400px;
}
.login-btn {
  margin-top: 20px;
  height: 44px;
  font-size: 16px;
}
.tip {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 12px;
}
</style>
