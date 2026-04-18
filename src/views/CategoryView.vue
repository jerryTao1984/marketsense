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
  gap: 12px;
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
  min-width: 0;
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

.video-btn {
  background: #fff3e0;
  border: 1px solid #ffb74d;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  color: #e65100;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}

.video-btn:active {
  background: #ffe0b2;
}

.level-status {
  font-size: 24px;
  flex-shrink: 0;
}

.video-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  padding: 8px;
  box-sizing: border-box;
}

.video-container video {
  width: 100%;
  max-height: 100%;
  border-radius: 8px;
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
        <button
          v-if="level.video_url && !isLevelLocked(level.id)"
          class="video-btn"
          @click.stop="openVideo(level.video_url)"
        >
          📹 视频
        </button>
        <div class="level-status">
          {{ isLevelLocked(level.id) ? '🔒' : '▶️' }}
        </div>
      </div>
    </div>

    <van-popup v-model:show="showVideo" position="bottom" round :style="{ height: '80%' }">
      <div class="video-header">
        <van-icon name="cross" @click="closeVideo" size="20" />
      </div>
      <div class="video-container">
        <video ref="videoPlayer" controls autoplay :src="currentVideoUrl" />
      </div>
    </van-popup>
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

const showVideo = ref(false)
const currentVideoUrl = ref('')
const videoPlayer = ref<HTMLVideoElement | null>(null)

function openVideo(url: string) {
  currentVideoUrl.value = url
  showVideo.value = true
}

function closeVideo() {
  showVideo.value = false
  if (videoPlayer.value) {
    videoPlayer.value.pause()
    videoPlayer.value.currentTime = 0
  }
  currentVideoUrl.value = ''
}

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
