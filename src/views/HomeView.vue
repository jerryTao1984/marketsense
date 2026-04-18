<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-bottom: 32px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px 16px 20px;
  border-radius: 0 0 20px 20px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 12px;
}

.stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  padding: 20px 16px 12px;
  color: #333;
}

.category-card {
  margin: 0 16px 12px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.category-inner {
  padding: 16px;
  cursor: pointer;
}

.category-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.category-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 4px;
}

.category-desc {
  font-size: 13px;
  color: #999;
  margin: 0 0 8px;
}

.category-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #666;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  color: #999;
  font-size: 16px;
}
</style>

<template>
  <div class="home">
    <div class="header">
      <div class="header-top">
        <h1 class="app-title">🦆 识盘鸭</h1>
        <div class="stats">
          <div class="stat-item" @click="$router.push('/profile')">
            <span>👤</span>
            <span>{{ userStore.nickname || '我的' }}</span>
          </div>
          <div class="stat-item">
            <span>❤️</span>
            <span>{{ userStore.hearts }}/{{ userStore.maxHearts }}</span>
          </div>
          <div class="stat-item">
            <span>🔥</span>
            <span>{{ userStore.streakDays }} 天</span>
          </div>
          <div class="stat-item" @click="$router.push('/wrong-answers')">
            <span>📝</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <template v-else>
      <div class="section-title">选择学习模块</div>

      <div
        v-for="cat in categories"
        :key="cat.id"
        class="category-card"
        @click="goToCategory(cat.id)"
      >
        <div class="category-inner">
          <div class="category-icon">{{ cat.icon }}</div>
          <p class="category-name">{{ cat.name }}</p>
          <p class="category-desc">{{ cat.levels.length }} 个关卡</p>
          <div class="category-progress">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getProgress(cat) + '%', background: getCategoryColor(cat.id) }"
              ></div>
            </div>
            <span>{{ getProgress(cat) }}% 通关</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getCategories, type Category } from '../api'

const router = useRouter()
const userStore = useUserStore()
const categories = ref<Category[]>([])
const loading = ref(true)

const colorMap: Record<string, string> = {
  basics: '#4CAF50',
  trading: '#2196F3',
  kline: '#FF9800',
  predict: '#9C27B0',
}

function getCategoryColor(id: string) {
  return colorMap[id] || '#666'
}

function getProgress(cat: Category) {
  const total = cat.levels.length
  const unlocked = cat.levels.filter(l => userStore.isLevelUnlocked(cat.id, l.id)).length
  return total > 0 ? Math.round((unlocked / total) * 100) : 0
}

function goToCategory(id: string) {
  router.push({ path: `/category/${id}` })
}

onMounted(async () => {
  // 恢复登录态（路由守卫已同步恢复，这里重新从服务端同步数据）
  await userStore.refreshUserData()

  // 如果未登录，跳转
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }

  const cats = await getCategories()
  categories.value = cats
  loading.value = false
})
</script>
