<style scoped>
.quiz-page {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.quiz-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  gap: 12px;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.back-btn {
  background: none;
  border: none;
  font-size: 18px;
  padding: 4px;
}
.back-btn::after {
  border: none;
}

.progress-info {
  flex: 1;
  font-size: 14px;
  color: #666;
}

.question-area {
  flex: 1;
  padding: 20px 16px;
  padding-bottom: 40px;
}

.question-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
  margin-bottom: 16px;
  display: block;
}

.question-image {
  width: 100%;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  box-sizing: border-box;
}

.kline-img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 16px;
}

.option-btn {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  font-size: 16px;
  color: #333;
  text-align: left;
  line-height: 1.4;
}
.option-btn::after {
  border: none;
}
.option-btn.correct {
  border-color: #4CAF50;
  background: #e8f5e9;
  color: #2e7d32;
}
.option-btn.wrong {
  border-color: #f44336;
  background: #ffebee;
  color: #c62828;
}
.option-btn.disabled {
  opacity: 0.7;
}

.feedback {
  margin-top: 16px;
  padding: 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
}
.feedback.correct {
  background: #e8f5e9;
  color: #2e7d32;
  border-left: 4px solid #4CAF50;
}
.feedback.wrong {
  background: #fff3e0;
  color: #e65100;
  border-left: 4px solid #FF9800;
}

.feedback-label {
  font-weight: bold;
  margin-bottom: 6px;
  display: block;
}

.next-btn {
  width: 100%;
  padding: 10px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-top: 16px;
}

/* Result overlay */
.result-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.result-card {
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  width: 85%;
}

.result-icon {
  font-size: 64px;
  margin-bottom: 16px;
  display: block;
}

.result-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  display: block;
}

.result-score {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
  display: block;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.result-btn {
  flex: 1;
  padding: 10px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
.result-btn::after {
  border: none;
}
.result-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
.result-btn.secondary {
  background: #f0f0f0;
  color: #666;
}

/* Loading */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  color: #999;
  font-size: 16px;
}

.mode-tabs {
  display: flex;
  background: white;
  padding: 0 16px;
  border-bottom: 1px solid #eee;
}

.mode-tab {
  flex: 1;
  text-align: center;
  padding: 12px 0;
  font-size: 14px;
  color: #999;
  border-bottom: 2px solid transparent;
}

.mode-tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
  font-weight: bold;
}

.no-questions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: #999;
}

.no-questions-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.no-questions-text {
  font-size: 16px;
  margin-bottom: 20px;
}

.no-questions-btn {
  padding: 8px 24px;
  border: 1px solid #667eea;
  border-radius: 20px;
  background: white;
  color: #667eea;
  font-size: 14px;
}
.no-questions-btn::after {
  border: none;
}

.tag-wrong {
  display: inline-block;
  background: #fee;
  color: #e53935;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  vertical-align: middle;
}

.tag-done {
  display: inline-block;
  background: #e8f5e9;
  color: #43a047;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  vertical-align: middle;
}

.hearts-info {
  font-size: 14px;
  font-weight: bold;
  color: #e53935;
  margin-right: 8px;
}

.custom-progress {
  width: 100px;
  height: 4px;
  background: #eee;
  border-radius: 2px;
  overflow: hidden;
}
.custom-progress-inner {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  transition: width 0.3s;
}
</style>

<template>
  <view class="quiz-page">
    <!-- Header -->
    <view class="quiz-header">
      <button class="back-btn" @click="goBack">←</button>
      <text class="progress-info">
        {{ currentIndex + 1 }} / {{ questions.length }}
      </text>
      <text class="hearts-info" v-if="mode === 'challenge'">
        ❤️ {{ userStore.hearts }}
      </text>
      <view class="custom-progress">
        <view class="custom-progress-inner" :style="{ width: progressPercent + '%' }"></view>
      </view>
    </view>

    <!-- Mode tabs -->
    <view class="mode-tabs">
      <view
        class="mode-tab"
        :class="{ active: mode === 'challenge' }"
        @click="switchMode('challenge')"
      >
        挑战模式
      </view>
      <view
        class="mode-tab"
        :class="{ active: mode === 'review' }"
        @click="switchMode('review')"
      >
        复习模式
      </view>
    </view>

    <!-- Loading -->
    <view v-if="loading" class="loading">加载题目中...</view>

    <!-- Question -->
    <scroll-view v-else-if="questions.length > 0" class="question-area" scroll-y>
      <text class="question-title">
        {{ currentQuestion?.title }}
        <text v-if="isWrongQuestion(currentQuestion?.id)" class="tag-wrong">曾做错</text>
        <text v-else-if="isDoneQuestion(currentQuestion?.id)" class="tag-done">做过</text>
      </text>

      <view v-if="currentQuestion?.image_url" class="question-image">
        <image :src="currentQuestion.image_url" mode="widthFix" class="kline-img" />
      </view>

      <view class="options-list">
        <button
          v-for="opt in currentQuestion?.options"
          :key="opt.value"
          class="option-btn"
          :class="{
            correct: answered && opt.value === correctAnswer,
            wrong: answered && selected === opt.value && opt.value !== correctAnswer,
            disabled: answered,
          }"
          @click="selectAnswer(opt.value)"
        >
          {{ opt.label }}
        </button>
      </view>

      <!-- Feedback -->
      <view
        v-if="answered && feedbackText"
        class="feedback"
        :class="{ correct: isCorrect, wrong: !isCorrect }"
      >
        <text class="feedback-label">
          {{ isCorrect ? '✅ 回答正确！' : '❌ 回答错误' }}
          <text v-if="!isCorrect">正确答案：{{ correctAnswerText }}</text>
        </text>
        <text>{{ feedbackText }}</text>
        <button class="next-btn" @click="goNext">
          {{ isLast ? (mode === 'challenge' ? '查看结果' : '复习完毕') : '下一题' }}
        </button>
      </view>
    </scroll-view>

    <!-- No questions message -->
    <view v-else class="no-questions">
      <text class="no-questions-icon">{{ mode === 'review' ? '📚' : '🎉' }}</text>
      <text class="no-questions-text">
        {{ mode === 'review' ? '还没有做过的题目' : '本关题目已全部答对！' }}
      </text>
      <button class="no-questions-btn" @click="mode === 'review' ? switchMode('challenge') : switchMode('review')">
        {{ mode === 'review' ? '去挑战' : '复习所有题目' }}
      </button>
    </view>

    <!-- Result overlay -->
    <view v-if="showResult" class="result-overlay">
      <view class="result-card">
        <text class="result-icon">{{ resultData?.passed ? '🎉' : '💪' }}</text>
        <text class="result-title">{{ resultData?.passed ? '恭喜通关！' : '继续加油！' }}</text>
        <text class="result-score">答对 {{ resultData?.correct_count }} / {{ questions.length }} 题</text>
        <view class="result-actions">
          <button class="result-btn secondary" @click="goBack">返回首页</button>
          <button
            v-if="resultData?.passed && resultData.next_unlocked"
            class="result-btn primary"
            @click="goNextLevel"
          >
            下一关
          </button>
        </view>
      </view>
    </view>

    <!-- No Hearts overlay -->
    <view v-if="mode === 'challenge' && userStore.hearts <= 0" class="result-overlay no-hearts-overlay">
      <view class="result-card no-hearts-card">
        <text class="result-icon">💔</text>
        <text class="result-title">体力耗尽</text>
        <text class="result-score">休息一下或者恢复体力继续挑战吧</text>
        <view class="result-actions">
          <button class="result-btn secondary" @click="goBack">返回首页</button>
          <button class="result-btn primary" @click="handleRefillHearts">满血复活</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad, onShareAppMessage } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getLevelQuestions, checkAnswer, completeLevel, getWrongAnswers, getDoneQuestions, getAttemptedQuestions, deductHeart as apiDeductHeart } from '../../api'
import type { Question, CheckResponse, CompleteResponse } from '../../api'

const userStore = useUserStore()

const categoryId = ref('')
const levelId = ref('')

const questions = ref<Question[]>([])
const allLevelQuestions = ref<Question[]>([])
const loading = ref(true)
const mode = ref<'challenge' | 'review'>('challenge')

const doneQuestionIds = ref<Set<string>>(new Set())
const wrongQuestionIds = ref<Set<string>>(new Set())

const currentIndex = ref(0)
const selected = ref('')
const answered = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')
const feedbackText = ref('')
const correctCount = ref(0)
const showResult = ref(false)
const resultData = ref<CompleteResponse | null>(null)

const currentQuestion = computed(() => questions.value[currentIndex.value])

const correctAnswerText = computed(() => {
  if (!correctAnswer.value || !currentQuestion.value) return correctAnswer.value
  const opt = currentQuestion.value.options.find(o => o.value === correctAnswer.value)
  return opt ? opt.label : correctAnswer.value
})

const progressPercent = computed(() =>
  questions.value.length > 0 ? Math.round(((currentIndex.value + 1) / questions.value.length) * 100) : 0
)

const isLast = computed(() => currentIndex.value >= questions.value.length - 1)

async function selectAnswer(value: string) {
  if (answered.value) return

  selected.value = value
  answered.value = true

  uni.showLoading({ title: '判断中...', mask: true })
  try {
    const result: CheckResponse = await checkAnswer(currentQuestion.value.id, value, userStore.userId)
    isCorrect.value = result.is_correct
    correctAnswer.value = result.correct_answer
    feedbackText.value = result.explanation

    if (isCorrect.value) {
      correctCount.value++
    } else if (mode.value === 'challenge') {
      if (userStore.userId) {
        const { hearts } = await apiDeductHeart(userStore.userId)
        userStore.hearts = hearts
      } else {
        userStore.deductHeart()
      }
    }
  } catch (e) {
    uni.showToast({ title: '网络异常', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}

async function handleRefillHearts() {
  uni.showLoading({ title: '恢复中...' })
  try {
    await userStore.refillHearts()
  } finally {
    uni.hideLoading()
  }
}

async function goNext() {
  if (isLast.value) {
    if (mode.value === 'review') {
      uni.navigateBack()
      return
    }
    
    uni.showLoading({ title: '结算中...', mask: true })
    try {
      const result: CompleteResponse = await completeLevel(
        userStore.userId,
        levelId.value,
        correctCount.value,
        questions.value.length
      )
      resultData.value = result

      userStore.hearts = result.hearts
      userStore.streakDays = result.streak_days
      if (result.passed && result.next_unlocked) {
        userStore.unlockLevel(categoryId.value, result.next_unlocked)
      }

      showResult.value = true
    } catch (e) {
      uni.showToast({ title: '结算失败', icon: 'none' })
    } finally {
      uni.hideLoading()
    }
  } else {
    selected.value = ''
    answered.value = false
    isCorrect.value = false
    correctAnswer.value = ''
    feedbackText.value = ''
    currentIndex.value++
  }
}

function goBack() {
  uni.navigateBack()
}

function goNextLevel() {
  if (resultData.value?.next_unlocked) {
    uni.redirectTo({
      url: `/pages/quiz/quiz?categoryId=${categoryId.value}&levelId=${resultData.value.next_unlocked}`
    })
  }
}

function switchMode(newMode: 'challenge' | 'review') {
  mode.value = newMode
  loadQuestions()
}

function isWrongQuestion(id: string | undefined) {
  return id && wrongQuestionIds.value.has(id)
}

function isDoneQuestion(id: string | undefined) {
  return id && doneQuestionIds.value.has(id)
}

let loadingTask: Promise<void> | null = null

async function loadQuestions() {
  if (loadingTask) {
    await loadingTask
    return
  }

  currentIndex.value = 0
  selected.value = ''
  answered.value = false
  isCorrect.value = false
  correctAnswer.value = ''
  feedbackText.value = ''
  correctCount.value = 0
  showResult.value = false
  resultData.value = null
  wrongQuestionIds.value.clear()
  doneQuestionIds.value.clear()
  loading.value = true

  try {
    if (allLevelQuestions.value.length === 0) {
      allLevelQuestions.value = await getLevelQuestions(levelId.value)
    }

    let filtered = [...allLevelQuestions.value]

    if (userStore.userId) {
      const [wrongs, doneResult, attemptedResult] = await Promise.all([
        getWrongAnswers(userStore.userId, levelId.value),
        getDoneQuestions(userStore.userId, levelId.value),
        getAttemptedQuestions(userStore.userId, levelId.value),
      ])

      wrongQuestionIds.value = new Set(wrongs.map(w => w.question_id))
      doneQuestionIds.value = new Set(doneResult)

      if (mode.value === 'challenge') {
        filtered = filtered.filter(q => !doneResult.includes(q.id))
      } else {
        filtered = filtered.filter(q => attemptedResult.includes(q.id))
      }
    }

    if (filtered.length === 0) {
      if (mode.value === 'challenge' && userStore.userId) {
        const result: CompleteResponse = await completeLevel(
          userStore.userId,
          levelId.value,
          0,
          0
        )
        userStore.hearts = result.hearts
        userStore.streakDays = result.streak_days
        if (result.passed && result.next_unlocked) {
          userStore.unlockLevel(categoryId.value, result.next_unlocked)
        }
        resultData.value = {
          passed: result.passed,
          correct_count: result.correct_count,
          total_count: result.total_count,
          next_unlocked: result.next_unlocked,
          hearts: result.hearts,
          streak_days: result.streak_days,
        }
      } else {
        resultData.value = {
          passed: true,
          correct_count: 0,
          total_count: 0,
          next_unlocked: null,
          hearts: userStore.hearts,
          streak_days: userStore.streakDays,
        }
      }
      loading.value = false
      showResult.value = true
    } else {
      questions.value = filtered
      loading.value = false
    }
  } catch (e) {
    uni.showToast({ title: '加载题目失败', icon: 'none' })
    loading.value = false
  }
  loadingTask = null
}

onLoad((options: any) => {
  if (options.categoryId) categoryId.value = options.categoryId
  if (options.levelId) levelId.value = options.levelId
  
  loadQuestions()
})

onShareAppMessage(() => {
  return {
    title: `我在识盘鸭挑战了 ${categoryId.value} 关卡，快来一起学股票！`,
    path: `/pages/quiz/quiz?categoryId=${categoryId.value}&levelId=${levelId.value}`
  }
})
</script>
