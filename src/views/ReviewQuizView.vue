<template>
  <div class="review-page">
    <div class="review-header">
      <van-icon name="arrow-left" size="20" @click="$router.back()" />
      <span>题目复习 - {{ getLevelName(levelId) }}</span>
    </div>

    <div v-if="questions.length > 0 && !showResult" class="quiz-content">
      <div class="progress-bar">
        <van-progress :percentage="Math.round((currentIndex / questions.length) * 100)" :show-pivot="false" />
        <span class="progress-text">{{ currentIndex + 1 }} / {{ questions.length }}</span>
      </div>

      <div class="question-card">
        <p class="question-title">{{ questions[currentIndex].title }}</p>
        <div v-if="questions[currentIndex].image_url" class="question-image">
          <img :src="questions[currentIndex].image_url" alt="K线图" />
        </div>
      </div>

      <div class="options-list">
        <van-button
          v-for="opt in questions[currentIndex].options"
          :key="opt.value"
          :class="['option-btn', {
            selected: selectedAnswer === opt.value,
            correct: showFeedback && opt.value === questions[currentIndex]._correct,
            wrong: showFeedback && selectedAnswer === opt.value && opt.value !== questions[currentIndex]._correct,
          }]"
          block
          round
          @click="!showFeedback && selectAnswer(opt.value)"
        >
          {{ opt.label }}
        </van-button>
      </div>

      <div v-if="showFeedback" class="feedback">
        <van-notice-bar :text="feedbackText" :color="isCorrect ? '#07c160' : '#ee0a24'" />
        <p class="explanation">{{ questions[currentIndex].explanation }}</p>
        <van-button type="primary" block round @click="nextQuestion">
          {{ currentIndex < questions.length - 1 ? '下一题' : '查看结果' }}
        </van-button>
      </div>
    </div>

    <div v-if="showResult" class="result-overlay">
      <div class="result-card">
        <div class="result-icon">{{ passRate >= 60 ? '🎉' : '💪' }}</div>
        <h2>{{ passRate >= 60 ? '复习完成！' : '继续加油' }}</h2>
        <div class="result-stats">
          <p>正确 {{ correctCount }} / {{ questions.length }}</p>
          <p>正确率 {{ passRate }}%</p>
        </div>
        <van-button type="primary" block round @click="$router.push('/wrong-answers')">
          返回错题本
        </van-button>
      </div>
    </div>

    <van-empty v-if="questions.length === 0 && !loading" description="该关卡暂无做题记录" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getReviewQuestions, type Question } from '../api'

const route = useRoute()
const userStore = useUserStore()
const levelId = route.params.levelId as string

const questions = ref<(Question & { _correct?: string; explanation?: string })[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showFeedback = ref(false)
const showResult = ref(false)
const correctCount = ref(0)
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

const feedbackText = computed(() => {
  if (!showFeedback.value) return ''
  return isCorrect.value ? '回答正确！' : `回答错误，正确答案是 ${questions.value[currentIndex.value]._correct}`
})

const isCorrect = computed(() => {
  return selectedAnswer.value === questions.value[currentIndex.value]._correct
})

const passRate = computed(() => {
  return Math.round((correctCount.value / questions.value.length) * 100)
})

async function selectAnswer(value: string) {
  selectedAnswer.value = value
  showFeedback.value = true
  if (value === questions.value[currentIndex.value]._correct) {
    correctCount.value++
  }
}

function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    selectedAnswer.value = ''
    showFeedback.value = false
  } else {
    showResult.value = true
  }
}

onMounted(async () => {
  const done = await getReviewQuestions(userStore.userId, levelId)
  if (done.length > 0) {
    questions.value = done.map(q => ({
      id: q.id,
      type: q.type,
      title: q.title,
      image_url: q.image_url,
      options: q.options,
      _correct: q.answer,
      explanation: q.explanation,
    }))
    questions.value.sort(() => Math.random() - 0.5)
  }
  loading.value = false
})
</script>

<style scoped>
.review-page {
  min-height: 100vh;
  background: #f5f5f5;
}
.review-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 500;
}
.progress-bar {
  padding: 12px 16px 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.progress-text {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
}
.question-card {
  background: #fff;
  margin: 12px;
  border-radius: 12px;
  padding: 20px;
}
.question-title {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  margin: 0 0 12px;
}
.question-image {
  text-align: center;
  margin-top: 12px;
}
.question-image img {
  max-width: 100%;
  border-radius: 8px;
}
.options-list {
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.option-btn {
  height: 44px;
  font-size: 14px;
  text-align: left;
  justify-content: flex-start;
  padding: 0 16px;
  border: 1px solid #eee;
  color: #333;
  background: #fff;
}
.option-btn.selected {
  border-color: #667eea;
  background: #f0f0ff;
}
.option-btn.correct {
  border-color: #07c160;
  background: #e8f8ef;
  color: #07c160;
}
.option-btn.wrong {
  border-color: #ee0a24;
  background: #fff0f0;
  color: #ee0a24;
}
.feedback {
  padding: 12px;
}
.explanation {
  font-size: 13px;
  color: #666;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
  margin: 12px 0;
  line-height: 1.6;
}
.result-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.result-card {
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  width: 80%;
  max-width: 320px;
}
.result-icon {
  font-size: 48px;
  margin-bottom: 12px;
}
.result-card h2 {
  margin: 0 0 16px;
  font-size: 20px;
}
.result-stats {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}
.result-stats p {
  margin: 4px 0;
}
</style>
