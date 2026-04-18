import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authSync, phoneLogin, refillHearts as apiRefillHearts, getUserProfile } from '../api'

const LS_PHONE = 'user_phone'
const LS_USER_ID = 'user_id'
const LS_LEVELS = 'unlocked_levels'

export const useUserStore = defineStore('user', () => {
  const userId = ref(0)
  const hearts = ref(5)
  const maxHearts = 5
  const streakDays = ref(0)
  const unlockedLevels = ref<Record<string, string[]>>({})
  const phone = ref<string | null>(null)
  const nickname = ref<string | null>(null)
  const isLoggedIn = ref(false)

  const hasHeart = computed(() => hearts.value > 0)

  function saveUnlockedLevels() {
    localStorage.setItem(LS_LEVELS, JSON.stringify(unlockedLevels.value))
  }

  function loadUnlockedLevels(): Record<string, string[]> | null {
    const raw = localStorage.getItem(LS_LEVELS)
    return raw ? JSON.parse(raw) : null
  }

  async function sync(deviceId: string) {
    const data = await authSync(deviceId)
    userId.value = data.user_id
    hearts.value = data.hearts
    streakDays.value = data.streak_days
    unlockedLevels.value = data.unlocked_levels
    isLoggedIn.value = true
    localStorage.setItem(LS_USER_ID, String(data.user_id))
    saveUnlockedLevels()
  }

  async function loginWithPhone(phoneNumber: string) {
    const data = await phoneLogin(phoneNumber)
    userId.value = data.user_id
    hearts.value = data.hearts
    streakDays.value = data.streak_days
    unlockedLevels.value = data.unlocked_levels
    phone.value = phoneNumber
    nickname.value = data.nickname || `用户${phoneNumber.slice(-4)}`
    isLoggedIn.value = true
    localStorage.setItem(LS_PHONE, phoneNumber)
    localStorage.setItem(LS_USER_ID, String(data.user_id))
    saveUnlockedLevels()
  }

  // 从 localStorage 恢复登录态（同步，用于路由守卫和页面刷新）
  function restoreLogin() {
    const storedPhone = localStorage.getItem(LS_PHONE)
    const storedId = localStorage.getItem(LS_USER_ID)
    if (storedPhone) {
      phone.value = storedPhone
      nickname.value = `用户${storedPhone.slice(-4)}`
      isLoggedIn.value = true
      if (storedId) {
        userId.value = parseInt(storedId, 10)
      }
      // 恢复关卡解锁状态
      const levels = loadUnlockedLevels()
      if (levels) {
        unlockedLevels.value = levels
      }
    }
  }

  // 刷新时同步服务端数据
  async function refreshUserData() {
    if (userId.value && phone.value) {
      try {
        const profile = await getUserProfile(userId.value)
        hearts.value = profile.hearts
        streakDays.value = profile.streak_days
        nickname.value = profile.nickname || nickname.value
        // 重新登录获取最新关卡解锁状态
        await loginWithPhone(phone.value)
      } catch {
        // 静默失败，不影响登录态
      }
    }
  }

  function logout() {
    userId.value = 0
    hearts.value = 5
    streakDays.value = 0
    unlockedLevels.value = {}
    phone.value = null
    nickname.value = null
    isLoggedIn.value = false
    localStorage.removeItem(LS_PHONE)
    localStorage.removeItem(LS_USER_ID)
    localStorage.removeItem(LS_LEVELS)
  }

  function deductHeart() {
    if (hearts.value > 0) {
      hearts.value--
    }
  }

  async function refillHearts() {
    if (userId.value) {
      const data = await apiRefillHearts(userId.value)
      hearts.value = data.hearts
    }
  }

  function resetHearts() {
    hearts.value = maxHearts
  }

  function addStreak() {
    streakDays.value++
  }

  function unlockLevel(categoryId: string, levelId: string) {
    if (!unlockedLevels.value[categoryId]) {
      unlockedLevels.value[categoryId] = []
    }
    if (!unlockedLevels.value[categoryId].includes(levelId)) {
      unlockedLevels.value[categoryId].push(levelId)
      saveUnlockedLevels()
    }
  }

  function isLevelUnlocked(categoryId: string, levelId: string) {
    return unlockedLevels.value[categoryId]?.includes(levelId) ?? false
  }

  return {
    userId, hearts, maxHearts, streakDays, unlockedLevels,
    phone, nickname, isLoggedIn,
    hasHeart, sync, loginWithPhone, restoreLogin, refreshUserData, logout,
    deductHeart, refillHearts, resetHearts,
    addStreak, unlockLevel, isLevelUnlocked,
  }
})
