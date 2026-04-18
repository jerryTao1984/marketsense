<template>
  <div class="history-page">
    <div class="history-header">
      <van-icon name="arrow-left" size="20" @click="$router.back()" />
      <span>做题记录</span>
    </div>

    <van-empty v-if="!loading && groups.length === 0" description="暂无做题记录" />

    <div v-if="groups.length > 0" class="history-list">
      <van-collapse v-model="activeCollapse" accordion>
        <van-collapse-item
          v-for="group in groups"
          :key="group.levelId"
          :title="group.levelName"
          :name="group.levelId"
        >
          <div class="group-stats">
            <span class="stat-correct">正确 {{ group.correct }}</span>
            <span class="stat-wrong">错误 {{ group.wrong }}</span>
            <span class="stat-accuracy">正确率 {{ group.accuracy }}%</span>
          </div>
          <div class="question-list">
            <div
              v-for="item in group.items"
              :key="item.record_id"
              class="question-item"
              :class="{ correct: item.is_correct, wrong: !item.is_correct }"
            >
              <div class="q-status">
                {{ item.is_correct ? '✓' : '✗' }}
              </div>
              <div class="q-content">
                <div class="q-title">{{ truncate(item.title, 50) }}</div>
                <div class="q-detail">
                  你的答案: {{ item.user_answer }} | 正确: {{ item.correct_answer }}
                </div>
              </div>
              <div class="q-time">{{ formatTime(item.created_at) }}</div>
            </div>
          </div>
        </van-collapse-item>
      </van-collapse>
    </div>

    <div v-if="loading" class="loading">
      <van-loading size="24px" vertical>加载中...</van-loading>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const loading = ref(true)
const activeCollapse = ref<string | null>(null)

interface HistoryItem {
  record_id: number
  question_id: string
  level_id: string
  category_id: string
  user_answer: string
  correct_answer: string
  is_correct: number
  title: string
  created_at: string
}

interface HistoryGroup {
  levelId: string
  levelName: string
  correct: number
  wrong: number
  accuracy: number
  items: HistoryItem[]
}

const groups = ref<HistoryGroup[]>([])

const levelNames: Record<string, string> = {
  L1: '市场基础', L2: '财务报表', L3: '技术指标', L4: '投资策略',
  T1: '海豚交易法', T2: '海龟交易法', T3: '深度估值', T4: '波动率反转',
  K1: '单根K线', K2: 'K线组合', K3: '趋势形态', K4: '量价分析',
  P1: '下周涨跌预测', P2: '趋势转折预测', P3: '支撑压力预测',
}

function truncate(s: string, n: number) {
  return s.length > n ? s.slice(0, n) + '...' : s
}

function formatTime(d: string) {
  if (!d) return ''
  const parts = d.split(' ')
  if (parts.length >= 2) return parts[1].slice(0, 5)
  return d.slice(0, 10)
}

onMounted(async () => {
  if (userStore.userId) {
    const res = await fetch(`/api/v1/user/history?user_id=${userStore.userId}`)
    const allItems: HistoryItem[] = await res.json()

    // Group by level
    const map = new Map<string, HistoryGroup>()
    for (const item of allItems) {
      if (!map.has(item.level_id)) {
        map.set(item.level_id, {
          levelId: item.level_id,
          levelName: levelNames[item.level_id] || item.level_id,
          correct: 0,
          wrong: 0,
          accuracy: 0,
          items: [],
        })
      }
      const g = map.get(item.level_id)!
      g.items.push(item)
      if (item.is_correct) g.correct++
      else g.wrong++
    }

    // Calculate accuracy
    for (const g of map.values()) {
      const total = g.correct + g.wrong
      g.accuracy = total > 0 ? Math.round((g.correct / total) * 100) : 0
    }

    groups.value = Array.from(map.values())
  }
  loading.value = false
})
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: #f5f5f5;
}
.history-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 17px;
  font-weight: 500;
}
.history-list {
  padding: 12px;
}
.group-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  margin-bottom: 8px;
}
.stat-correct {
  color: #07c160;
}
.stat-wrong {
  color: #ee0a24;
}
.stat-accuracy {
  color: #999;
}
.question-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.question-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 13px;
}
.question-item.correct {
  background: #f0faf3;
}
.question-item.wrong {
  background: #fff5f5;
}
.q-status {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
}
.correct .q-status {
  background: #07c160;
  color: #fff;
}
.wrong .q-status {
  background: #ee0a24;
  color: #fff;
}
.q-content {
  flex: 1;
  min-width: 0;
}
.q-title {
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.q-detail {
  color: #999;
  font-size: 11px;
  margin-top: 2px;
}
.q-time {
  color: #bbb;
  font-size: 11px;
  flex-shrink: 0;
}
.loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}
</style>
