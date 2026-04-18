<template>
  <div class="wrong-page">
    <div class="wrong-header">
      <van-icon name="arrow-left" size="20" @click="$router.back()" />
      <span>错题本</span>
    </div>

    <van-empty v-if="!loading && wrongAnswers.length === 0" description="暂无错题，继续加油！" />

    <div v-if="wrongAnswers.length > 0" class="wrong-list">
      <van-cell-group inset>
        <van-cell
          v-for="item in wrongAnswers"
          :key="item.record_id"
          :title="truncate(item.title, 40)"
          :label="`${getLevelName(item.level_id)} | 你的答案: ${item.user_answer} | 正确: ${item.correct_answer}`"
          is-link
          @click="goReview(item.level_id)"
        />
      </van-cell-group>
      <div class="wrong-count">共 {{ wrongAnswers.length }} 道错题</div>
    </div>

    <div v-if="loading" class="loading">
      <van-loading size="24px" vertical>加载中...</van-loading>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getWrongAnswers, type WrongAnswerItem } from '../api'

const router = useRouter()
const userStore = useUserStore()
const wrongAnswers = ref<WrongAnswerItem[]>([])
const loading = ref(true)

const levelNames: Record<string, string> = {
  L1: '市场基础', L2: '财务报表', L3: '技术指标', L4: '投资策略',
  T1: '海豚交易法', T2: '海龟交易法', T3: '深度估值', T4: '波动率反转',
  K1: '单根K线', K2: 'K线组合', K3: '趋势形态', K4: '量价分析',
  P1: '下周涨跌预测', P2: '趋势转折预测', P3: '支撑压力预测',
}

function getLevelName(id: string) {
  return levelNames[id] || id
}

function truncate(s: string, n: number) {
  return s.length > n ? s.slice(0, n) + '...' : s
}

function goReview(levelId: string) {
  router.push(`/review/${levelId}`)
}

onMounted(async () => {
  if (userStore.userId) {
    wrongAnswers.value = await getWrongAnswers(userStore.userId)
  }
  loading.value = false
})
</script>

<style scoped>
.wrong-page {
  min-height: 100vh;
  background: #f5f5f5;
}
.wrong-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 17px;
  font-weight: 500;
}
.wrong-list {
  padding: 12px;
}
.wrong-count {
  text-align: center;
  color: #999;
  font-size: 12px;
  padding: 12px;
}
.loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}
</style>
