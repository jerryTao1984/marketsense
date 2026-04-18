<template>
  <div class="profile-page">
    <div class="profile-header">
      <van-icon name="arrow-left" size="20" @click="$router.back()" />
      <span>个人中心</span>
    </div>

    <div class="user-card" v-if="profile">
      <div class="avatar">{{ profile.nickname?.charAt(0) || '用' }}</div>
      <div class="info">
        <div class="nickname">{{ profile.nickname }}</div>
        <div class="phone">{{ maskPhone(profile.phone) }}</div>
        <div class="created">注册时间 {{ formatDate(profile.created_at) }}</div>
      </div>
    </div>

    <div class="stats-card" v-if="profile">
      <div class="stat-item">
        <van-circle
          :current-rate="profile.overall_accuracy"
          :rate="100"
          :size="80"
          :stroke-width="8"
          :color="accuracyColor"
        >
          <span class="rate-text">{{ profile.overall_accuracy }}%</span>
        </van-circle>
        <div class="stat-label">总正确率</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-value">{{ profile.total_attempts }}</div>
        <div class="stat-label">总答题数</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-value">{{ profile.total_correct }}</div>
        <div class="stat-label">正确数</div>
      </div>
    </div>

    <div class="level-stats" v-if="profile?.level_stats?.length">
      <h3>关卡正确率</h3>
      <van-cell-group inset>
        <van-cell
          v-for="s in profile.level_stats"
          :key="s.level_id"
          :title="getLevelName(s.level_id)"
          :value="`${s.accuracy}% (${s.correct}/${s.total})`"
        >
          <template #right-icon>
            <div class="accuracy-bar">
              <div class="accuracy-fill" :style="{ width: s.accuracy + '%', background: accuracyColor(s.accuracy) }"></div>
            </div>
          </template>
        </van-cell>
      </van-cell-group>
    </div>

    <div class="action-buttons">
      <van-button block round type="primary" to="/wrong-answers" icon="records">
        错题本
      </van-button>
      <van-button block round type="primary" to="/history" icon="records">
        做题记录
      </van-button>
      <van-button block round plain type="default" @click="handleLogout" icon="sign-out">
        退出登录
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getUserProfile, type UserProfile } from '../api'

const router = useRouter()
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

function handleLogout() {
  userStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (userStore.userId) {
    profile.value = await getUserProfile(userStore.userId)
  }
})
</script>

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
}
.phone {
  color: #999;
  font-size: 13px;
  margin-top: 2px;
}
.created {
  color: #bbb;
  font-size: 11px;
  margin-top: 4px;
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
}
.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}
.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}
.rate-text {
  font-size: 14px;
  font-weight: 600;
}
.stat-divider {
  width: 1px;
  height: 40px;
  background: #eee;
}
.level-stats {
  margin: 0 12px 12px;
}
.level-stats h3 {
  font-size: 15px;
  padding: 12px 0 8px;
  color: #333;
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
  transition: width 0.3s;
}
.action-buttons {
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
