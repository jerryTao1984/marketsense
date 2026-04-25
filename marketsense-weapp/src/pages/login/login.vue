<template>
  <view class="login-page">
    <view class="login-header">
      <view class="logo">🦆</view>
      <view class="h1">识盘鸭</view>
      <text class="subtitle">股票学习小助手</text>
    </view>
    
    <view class="login-form">
      <view class="input-group">
        <text class="label">手机号</text>
        <input 
          class="phone-input"
          v-model="phone" 
          type="number" 
          placeholder="请输入11位手机号" 
          maxlength="11"
        />
      </view>
      <text v-if="errorMsg" class="error-msg">{{ errorMsg }}</text>
      
      <button 
        class="login-btn" 
        :class="{ 'btn-disabled': phone.length !== 11, 'btn-loading': loading }"
        :disabled="phone.length !== 11 || loading"
        @click="handleLogin"
      >
        {{ loading ? '登录中...' : '登录' }}
      </button>
      
      <text class="tip">输入手机号即可登录，无需密码</text>
      
      <!-- 未来可在此处添加微信一键登录按钮 -->
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'

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
    uni.reLaunch({ url: '/pages/index/index' })
  } catch (e: any) {
    uni.showToast({
      title: e.message || '登录失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

onLoad(() => {
  // 如果已登录直接跳转
  userStore.restoreLogin()
  if (userStore.isLoggedIn) {
    uni.reLaunch({ url: '/pages/index/index' })
  }
})
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
.h1 {
  color: #fff;
  font-size: 28px;
  font-weight: bold;
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
  box-sizing: border-box;
}

.input-group {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ebedf0;
  padding: 10px 0;
  margin-bottom: 8px;
}
.label {
  width: 60px;
  font-size: 14px;
  color: #323233;
}
.phone-input {
  flex: 1;
  font-size: 14px;
  height: 24px;
  line-height: 24px;
}

.error-msg {
  color: #ee0a24;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.login-btn {
  margin-top: 24px;
  height: 44px;
  line-height: 44px;
  font-size: 16px;
  background-color: #07c160; /* 微信绿 */
  color: #fff;
  border-radius: 22px;
  border: none;
}
.login-btn::after {
  border: none;
}
.btn-disabled {
  background-color: #a8e4c0;
  color: #fff;
}
.btn-loading {
  opacity: 0.8;
}

.tip {
  display: block;
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 16px;
}
</style>
