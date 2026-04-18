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
  cursor: pointer;
  padding: 4px;
}

.progress-info {
  flex: 1;
  font-size: 14px;
  color: #666;
}

.question-area {
  flex: 1;
  padding: 20px 16px;
}

.question-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
  margin: 0 0 16px;
}

.question-image {
  width: 100%;
  max-width: 400px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  min-height: 120px;
}

.kline-img {
  width: 100%;
  max-width: 376px;
  height: auto;
  border-radius: 8px;
  display: block;
  flex-shrink: 0;
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
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.option-btn:active:not(.disabled) {
  transform: scale(0.98);
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
  cursor: default;
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
}

.next-btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 16px;
}

.next-btn:active {
  transform: scale(0.98);
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
  max-width: 320px;
}

.result-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.result-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px;
}

.result-score {
  font-size: 16px;
  color: #666;
  margin: 0 0 24px;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.result-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
}

.result-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.result-btn.secondary {
  background: #f0f0f0;
  color: #666;
}

/* No hearts overlay */
.no-hearts-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 101;
}

.no-hearts-card {
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  width: 80%;
  max-width: 300px;
}

.no-hearts-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.no-hearts-text {
  font-size: 16px;
  color: #333;
  margin: 0 0 20px;
}

.refill-btn {
  padding: 12px 32px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
}

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
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
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
  margin: 0 0 20px;
}

.no-questions-btn {
  padding: 10px 24px;
  border: 1px solid #667eea;
  border-radius: 20px;
  background: white;
  color: #667eea;
  font-size: 14px;
  cursor: pointer;
}

.tag-wrong {
  display: inline-block;
  background: #fee;
  color: #e53935;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  font-weight: normal;
}

.tag-done {
  display: inline-block;
  background: #e8f5e9;
  color: #43a047;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  font-weight: normal;
}
</style>

<template>
  <div class="quiz-page">
    <!-- Header -->
    <div class="quiz-header">
      <button class="back-btn" @click="goBack">←</button>
      <div class="progress-info">
        {{ currentIndex + 1 }} / {{ questions.length }}
      </div>
      <van-progress
        :percentage="progressPercent"
        :show-pivot="false"
        color="linear-gradient(135deg, #667eea, #764ba2)"
        style="width: 100px"
      />
    </div>

    <!-- Mode tabs -->
    <div class="mode-tabs">
      <div
        class="mode-tab"
        :class="{ active: mode === 'challenge' }"
        @click="switchMode('challenge')"
      >
        挑战模式
      </div>
      <div
        class="mode-tab"
        :class="{ active: mode === 'review' }"
        @click="switchMode('review')"
      >
        复习模式
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">加载题目中...</div>

    <!-- Question -->
    <div v-else-if="questions.length > 0" class="question-area">
      <p class="question-title">
        {{ currentQuestion?.title }}
        <span v-if="isWrongQuestion(currentQuestion?.id)" class="tag-wrong">曾做错</span>
        <span v-else-if="isDoneQuestion(currentQuestion?.id)" class="tag-done">做过</span>
      </p>

      <div v-if="currentQuestion?.image_url" class="question-image">
        <img :src="currentQuestion.image_url" :alt="currentQuestion.title" class="kline-img" />
      </div>

      <div class="options-list">
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
      </div>

      <!-- Feedback -->
      <div
        v-if="answered && feedbackText"
        class="feedback"
        :class="{ correct: isCorrect, wrong: !isCorrect }"
      >
        <div class="feedback-label">
          {{ isCorrect ? '✅ 回答正确！' : '❌ 回答错误' }}
          <span v-if="!isCorrect">正确答案：{{ correctAnswerText }}</span>
        </div>
        <div>{{ feedbackText }}</div>
        <button class="next-btn" @click="goNext">
          {{ isLast ? (mode === 'challenge' ? '查看结果' : '复习完毕') : '下一题' }}
        </button>
      </div>
    </div>

    <!-- No questions message -->
    <div v-else class="no-questions">
      <div class="no-questions-icon">🎉</div>
      <p class="no-questions-text">本关题目已全部答对！</p>
      <button class="no-questions-btn" @click="switchMode('review')">复习所有题目</button>
    </div>

    <!-- No hearts overlay -->
    <div v-if="showNoHearts" class="no-hearts-overlay">
      <div class="no-hearts-card">
        <div class="no-hearts-icon">💔</div>
        <p class="no-hearts-text">体力已耗尽！<br />恢复体力继续挑战</p>
        <button class="refill-btn" @click="refillHearts">❤️ 恢复体力</button>
      </div>
    </div>

    <!-- Result overlay -->
    <div v-if="showResult" class="result-overlay">
      <div class="result-card">
        <div class="result-icon">{{ resultData?.passed ? '🎉' : '💪' }}</div>
        <h2 class="result-title">{{ resultData?.passed ? '恭喜通关！' : '继续加油！' }}</h2>
        <p class="result-score">答对 {{ resultData?.correct_count }} / {{ questions.length }} 题</p>
        <div class="result-actions">
          <button class="result-btn secondary" @click="goBack">返回首页</button>
          <button
            v-if="resultData?.passed && resultData.next_unlocked"
            class="result-btn primary"
            @click="goNextLevel"
          >
            下一关
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getLevelQuestions, checkAnswer, completeLevel, getWrongAnswers, getDoneQuestions } from '../api'
import type { Question, CheckResponse, CompleteResponse } from '../api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const categoryId = computed(() => route.params.categoryId as string)
const levelId = computed(() => route.params.levelId as string)

const questions = ref<Question[]>([])
const loading = ref(true)
const mode = ref<'challenge' | 'review'>('challenge')

// 已做过的题目 ID
const doneQuestionIds = ref<Set<string>>(new Set())
// 曾经做错的题目 ID
const wrongQuestionIds = ref<Set<string>>(new Set())

const currentIndex = ref(0)
const selected = ref('')
const answered = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')
const feedbackText = ref('')
const correctCount = ref(0)
const showResult = ref(false)
const showNoHearts = ref(false)
const resultData = ref<CompleteResponse | null>(null)

const currentQuestion = computed(() => questions.value[currentIndex.value])

// 正确答案的文字（用于错误提示时显示）
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
  if (mode.value === 'challenge' && !userStore.hasHeart) {
    showNoHearts.value = true
    return
  }

  selected.value = value
  answered.value = true

  // Call backend to check answer
  const result: CheckResponse = await checkAnswer(currentQuestion.value.id, value, userStore.userId)
  isCorrect.value = result.is_correct
  correctAnswer.value = result.correct_answer
  feedbackText.value = result.explanation

  if (isCorrect.value) {
    correctCount.value++
  } else if (mode.value === 'challenge') {
    userStore.deductHeart()
  }
}

async function goNext() {
  if (isLast.value) {
    // 复习模式：不结算，直接返回
    if (mode.value === 'review') {
      showResult.value = true
      resultData.value = {
        passed: true,
        correct_count: correctCount.value,
        total_count: questions.value.length,
        next_unlocked: null,
        hearts: userStore.hearts,
        streak_days: userStore.streakDays,
      }
      return
    }
    // Finish quiz - call backend to complete level
    const result: CompleteResponse = await completeLevel(
      userStore.userId,
      levelId.value,
      correctCount.value,
      questions.value.length
    )
    resultData.value = result

    // Update local state
    userStore.hearts = result.hearts
    userStore.streakDays = result.streak_days
    if (result.passed && result.next_unlocked) {
      userStore.unlockLevel(categoryId.value, result.next_unlocked)
    }

    showResult.value = true
  } else {
    currentIndex.value++
    selected.value = ''
    answered.value = false
    isCorrect.value = false
    correctAnswer.value = ''
    feedbackText.value = ''
  }
}

function goBack() {
  router.push('/')
}

async function refillHearts() {
  await userStore.refillHearts()
  showNoHearts.value = false
}

function goNextLevel() {
  if (resultData.value?.next_unlocked) {
    router.push({
      path: `/quiz/${categoryId.value}/${resultData.value.next_unlocked}`,
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

// 加载题目逻辑抽成函数，支持路由变化时重新加载
async function loadQuestions() {
  // 重置状态
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

  const currentLevelId = route.params.levelId as string
  const currentCategoryId = route.params.categoryId as string

  let allQuestions = await getLevelQuestions(currentLevelId)

  if (userStore.userId) {
    const wrongs = await getWrongAnswers(userStore.userId, currentLevelId)
    for (const w of wrongs) {
      wrongQuestionIds.value.add(w.question_id)
      doneQuestionIds.value.add(w.question_id)
    }

    // 挑战模式：过滤已答对的题目；复习模式：显示全部
    if (mode.value === 'challenge') {
      const doneIds = await getDoneQuestions(userStore.userId, currentLevelId)
      allQuestions = allQuestions.filter(q => !doneIds.includes(q.id))
    }
  }

  if (allQuestions.length === 0) {
    if (mode.value === 'challenge' && userStore.userId) {
      const result: CompleteResponse = await completeLevel(
        userStore.userId,
        currentLevelId,
        0,
        0
      )
      userStore.hearts = result.hearts
      userStore.streakDays = result.streak_days
      if (result.passed && result.next_unlocked) {
        userStore.unlockLevel(currentCategoryId, result.next_unlocked)
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
    questions.value = allQuestions
    loading.value = false
  }
}

onMounted(loadQuestions)

// 路由变化时重新加载（支持"下一关"导航）
watch(() => route.params.levelId, () => {
  loadQuestions()
})
</script>
