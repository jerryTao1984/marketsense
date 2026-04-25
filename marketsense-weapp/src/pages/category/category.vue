<style scoped>
.category-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.level-list {
  padding: 16px;
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

.locked {
  opacity: 0.5;
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

.level-status {
  font-size: 24px;
  flex-shrink: 0;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  color: #999;
  font-size: 16px;
}

.video-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 1000;
}

.video-close {
  position: absolute;
  top: 40px;
  right: 20px;
  color: white;
  font-size: 32px;
  z-index: 1001;
}

.video-player {
  width: 100%;
}
</style>

<template>
  <view class="category-page">
    <view v-if="loading" class="loading">加载中...</view>

    <view v-else class="level-list">
      <view
        v-for="(level, index) in category?.levels"
        :key="level.id"
        class="level-card"
        :class="{ locked: isLevelLocked(level.id) }"
        @click="startQuiz(level.id)"
      >
        <view
          class="level-num"
          :style="{ background: isLevelLocked(level.id) ? '#ccc' : categoryColor }"
        >
          {{ index + 1 }}
        </view>
        <view class="level-info">
          <view class="level-name">{{ level.name }}</view>
          <view class="level-desc">{{ level.description }}</view>
        </view>
        <button
          v-if="level.video_url && !isLevelLocked(level.id)"
          class="video-btn"
          @click.stop="openVideo(level.video_url)"
        >
          📹 视频
        </button>
        <view class="level-status">
          {{ isLevelLocked(level.id) ? '🔒' : '▶️' }}
        </view>
      </view>
    </view>

    <view class="video-mask" v-if="showVideo">
      <view class="video-close" @click="closeVideo">×</view>
      <video class="video-player" :src="currentVideoUrl" autoplay controls></video>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getCategories, type Category } from '../../api'

const userStore = useUserStore()
const category = ref<Category | null>(null)
const loading = ref(true)
const categoryId = ref('')

const showVideo = ref(false)
const currentVideoUrl = ref('')

function openVideo(url: string) {
  currentVideoUrl.value = url
  showVideo.value = true
}

function closeVideo() {
  showVideo.value = false
  currentVideoUrl.value = ''
}

const categoryColor = computed(() => {
  const map: Record<string, string> = { basics: '#4CAF50', trading: '#2196F3', kline: '#FF9800', predict: '#9C27B0' }
  return map[categoryId.value] || '#666'
})

function isLevelLocked(levelId: string) {
  return !userStore.isLevelUnlocked(categoryId.value, levelId)
}

function startQuiz(levelId: string) {
  if (isLevelLocked(levelId)) return
  uni.navigateTo({
    url: `/pages/quiz/quiz?categoryId=${categoryId.value}&levelId=${levelId}`
  })
}

onLoad(async (options: any) => {
  if (options.id) {
    categoryId.value = options.id
  }
  const cats = await getCategories()
  category.value = cats.find(c => c.id === categoryId.value) || null
  loading.value = false
  
  if (category.value) {
    uni.setNavigationBarTitle({ title: category.value.name })
  }
})
</script>
