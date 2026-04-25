<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}
.profile-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 17px;
  font-weight: 500;
}
.back-btn {
  font-size: 18px;
  color: white;
  margin-right: 8px;
}
.user-card {
  background: #fff;
  margin: 12px;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: bold;
}
.nickname {
  font-size: 18px;
  font-weight: 600;
  display: block;
}
.phone {
  color: #999;
  font-size: 13px;
  margin-top: 2px;
  display: block;
}
.created {
  color: #bbb;
  font-size: 11px;
  margin-top: 4px;
  display: block;
}
.stats-card {
  background: #fff;
  margin: 0 12px 12px;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.stat-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}
.stat-label {
  font-size: 12px;
  color: #999;
}
.rate-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 4px solid #07c160;
  display: flex;
  align-items: center;
  justify-content: center;
}
.rate-text {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}
.stat-divider {
  width: 1px;
  height: 40px;
  background: #eee;
}
.level-stats {
  margin: 0 12px 12px;
  background: white;
  border-radius: 12px;
  padding: 16px;
}
.level-stats-title {
  font-size: 15px;
  color: #333;
  margin-bottom: 12px;
  display: block;
  font-weight: bold;
}
.level-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.level-item:last-child {
  border-bottom: none;
}
.level-name {
  font-size: 14px;
  color: #333;
}
.level-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.level-val {
  font-size: 13px;
  color: #666;
}
.accuracy-bar {
  width: 60px;
  height: 6px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}
.accuracy-fill {
  height: 100%;
  border-radius: 3px;
}
.action-buttons {
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.btn {
  height: 44px;
  line-height: 44px;
  border-radius: 22px;
  font-size: 16px;
  background: #fff;
  border: 1px solid #eee;
}
.btn::after {
  border: none;
}
.btn-primary {
  background: #07c160;
  color: #fff;
  border-color: #07c160;
}
.btn-default {
  color: #666;
}
</style>

<template>
  <view class="profile-page">
    <view class="user-card" v-if="profile">
      <view class="avatar">{{ profile.nickname?.charAt(0) || '用' }}</view>
      <view class="info">
        <text class="nickname">{{ profile.nickname }}</text>
        <text class="phone">{{ maskPhone(profile.phone) }}</text>
        <text class="created">注册时间 {{ formatDate(profile.created_at) }}</text>
      </view>
    </view>

    <view class="stats-card" v-if="profile">
      <view class="stat-item">
        <view class="rate-circle" :style="{ borderColor: accuracyColor(profile.overall_accuracy) }">
          <text class="rate-text">{{ profile.overall_accuracy }}%</text>
        </view>
        <text class="stat-label">总正确率</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">{{ profile.total_attempts }}</text>
        <text class="stat-label">总答题数</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">{{ profile.total_correct }}</text>
        <text class="stat-label">正确数</text>
      </view>
    </view>

    <view class="level-stats" v-if="profile?.level_stats?.length">
      <text class="level-stats-title">关卡正确率</text>
      <view class="level-item" v-for="s in profile.level_stats" :key="s.level_id">
        <text class="level-name">{{ getLevelName(s.level_id) }}</text>
        <view class="level-right">
          <text class="level-val">{{ s.accuracy }}% ({{ s.correct }}/{{ s.total }})</text>
          <view class="accuracy-bar">
            <view class="accuracy-fill" :style="{ width: s.accuracy + '%', background: accuracyColor(s.accuracy) }"></view>
          </view>
        </view>
      </view>
    </view>

    <view class="action-buttons">
      <button class="btn btn-primary" @click="goTo('/pages/wrong/wrong')">📝 错题本</button>
      <button class="btn btn-primary" @click="goTo('/pages/history/history')">📅 做题记录</button>
      <button class="btn btn-default" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getUserProfile, type UserProfile } from '../../api'

const userStore = useUserStore()
const profile = ref<UserProfile | null>(null)

const levelNames: Record<string, string> = {
  L1: '市场基础', L2: '财务报表', L3: '技术指标', L4: '投资策略',
  T1: '海豚交易法', T2: '海龟交易法', T3: '深度估值', T4: '波动率反转',
  K1: '单根K线', K2: 'K线组合', K3: '趋势形态', K4: '量价分析',
  P1: '下周涨跌预测', P2: '趋势转折预测', P3: '支撑压力预测',
}

function getLevelName(id: string) {
  return levelNames[id] || id
}

function maskPhone(p: string | null) {
  if (!p) return ''
  return p.slice(0, 3) + '****' + p.slice(7)
}

function formatDate(d: string) {
  return d?.slice(0, 10) || ''
}

function accuracyColor(val: number) {
  if (val >= 80) return '#07c160'
  if (val >= 60) return '#ff976a'
  return '#ee0a24'
}

function goTo(url: string) {
  uni.navigateTo({ url })
}

function handleLogout() {
  userStore.logout()
  uni.reLaunch({ url: '/pages/login/login' })
}

onLoad(async () => {
  if (userStore.userId) {
    profile.value = await getUserProfile(userStore.userId)
  }
})
</script>
