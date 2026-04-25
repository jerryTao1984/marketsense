<style scoped>
.history-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}
.list-container {
  padding: 12px;
}
.session-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}
.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.level-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}
.time {
  font-size: 12px;
  color: #999;
}
.session-stats {
  display: flex;
  gap: 16px;
  align-items: center;
}
.stat {
  font-size: 14px;
  color: #666;
}
.tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.tag-pass {
  background: #e8f5e9;
  color: #4CAF50;
}
.tag-fail {
  background: #ffebee;
  color: #f44336;
}
.empty {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 14px;
}
</style>

<template>
  <view class="history-page">
    <view class="list-container" v-if="sessions.length">
      <view class="session-card" v-for="(session, index) in sessions" :key="index">
        <view class="session-header">
          <text class="level-name">{{ getLevelName(session.level_id) }}</text>
          <text class="time">{{ formatDate(session.created_at) }}</text>
        </view>
        <view class="session-stats">
          <text class="stat">答对: {{ session.correct_count }}/{{ session.total_count }}</text>
          <text class="tag" :class="session.passed ? 'tag-pass' : 'tag-fail'">
            {{ session.passed ? '已通关' : '未通关' }}
          </text>
        </view>
      </view>
    </view>
    <view class="empty" v-else>
      暂无答题记录
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getUserProfile } from '../../api'

const userStore = useUserStore()
const sessions = ref<any[]>([])

const levelNames: Record<string, string> = {
  L1: '市场基础', L2: '财务报表', L3: '技术指标', L4: '投资策略',
  T1: '海豚交易法', T2: '海龟交易法', T3: '深度估值', T4: '波动率反转',
  K1: '单根K线', K2: 'K线组合', K3: '趋势形态', K4: '量价分析',
  P1: '下周涨跌预测', P2: '趋势转折预测', P3: '支撑压力预测',
}

function getLevelName(id: string) {
  return levelNames[id] || id
}

function formatDate(dateStr: string) {
  const d = new Date(dateStr)
  return `${d.getMonth()+1}-${d.getDate()} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
}

onLoad(async () => {
  if (userStore.userId) {
    const profile = await getUserProfile(userStore.userId)
    // 根据 created_at 降序排列
    sessions.value = [...profile.sessions].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }
})
</script>
