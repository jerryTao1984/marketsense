<style scoped>
.category-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.nav-bar {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.back-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
}

.cat-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.level-list {
  padding: 0 16px;
}

.level-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
}

.level-card.locked {
  opacity: 0.5;
}

.level-card:not(.locked):active {
  transform: scale(0.98);
}

.level-num {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.level-info {
  flex: 1;
}

.level-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0 0 4px;
}

.level-desc {
  font-size: 13px;
  color: #999;
  margin: 0;
}

.level-status {
  font-size: 24px;
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
  <div class="category-page">
    <div class="nav-bar">
      <button class="back-btn" @click="$router.back()">←</button>
      <span class="cat-title">{{ category?.name || '加载中...' }}</span>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else class="level-list">
      <div
        v-for="(level, index) in category?.levels"
        :key="level.id"
        class="level-card"
        :class="{ locked: isLevelLocked(level.id) }"
        @click="startQuiz(level.id)"
      >
        <div
          class="level-num"
          :style="{ background: isLevelLocked(level.id) ? '#ccc' : categoryColor }"
        >
          {{ index + 1 }}
        </div>
        <div class="level-info">
          <p class="level-name">{{ level.name }}</p>
          <p class="level-desc">{{ level.description }}</p>
        </div>
        <div class="level-status">
          {{ isLevelLocked(level.id) ? '🔒' : '▶️' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getCategories, type Category, type LevelInfo } from '../api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const category = ref<Category | null>(null)
const loading = ref(true)

const categoryColor = computed(() => {
  const map: Record<string, string> = { basics: '#4CAF50', trading: '#2196F3', kline: '#FF9800', predict: '#9C27B0' }
  return map[route.params.categoryId as string] || '#666'
})

function isLevelLocked(levelId: string) {
  return !userStore.isLevelUnlocked(route.params.categoryId as string, levelId)
}

function startQuiz(levelId: string) {
  if (isLevelLocked(levelId)) return
  router.push({
    path: `/quiz/${route.params.categoryId}/${levelId}`,
  })
}

onMounted(async () => {
  const cats = await getCategories()
  category.value = cats.find(c => c.id === route.params.categoryId) || null
  loading.value = false
})
</script>
