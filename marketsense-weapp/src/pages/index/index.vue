<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-bottom: 32px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 48px 16px 20px; /* 小程序没有原生导航栏时，顶部留出状态栏高度 */
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
  background-color: #ffffff;
}

.category-inner {
  padding: 16px;
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
  <view class="home">
    <view class="header">
      <view class="header-top">
        <text class="app-title">🦆 识盘鸭</text>
        <view class="stats">
          <view class="stat-item" @click="goTo('/pages/profile/profile')">
            <text>👤</text>
            <text>{{ userStore.nickname || '我的' }}</text>
          </view>
          <view class="stat-item">
            <text>🔥</text>
            <text>{{ userStore.streakDays }} 天</text>
          </view>
          <view class="stat-item" @click="goTo('/pages/wrong/wrong')">
            <text>📝</text>
          </view>
        </view>
      </view>
    </view>

    <view v-if="loading" class="loading">加载中...</view>

    <template v-else>
      <view class="section-title">选择学习模块</view>

      <view
        v-for="cat in categories"
        :key="cat.id"
        class="category-card"
        @click="goToCategory(cat.id)"
      >
        <view class="category-inner">
          <view class="category-icon">{{ cat.icon }}</view>
          <view class="category-name">{{ cat.name }}</view>
          <view class="category-desc">{{ cat.levels.length }} 个关卡</view>
          <view class="category-progress">
            <view class="progress-bar">
              <view
                class="progress-fill"
                :style="{ width: getProgress(cat) + '%', background: getCategoryColor(cat.id) }"
              ></view>
            </view>
            <text>{{ getProgress(cat) }}% 通关</text>
          </view>
        </view>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getCategories, type Category } from '../../api'

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

function goTo(url: string) {
  uni.navigateTo({ url })
}

function goToCategory(id: string) {
  uni.navigateTo({ url: `/pages/category/category?id=${id}` })
}

onShow(async () => {
  // 从本地缓存恢复状态
  userStore.restoreLogin()

  // 如果未登录，跳转登录页
  if (!userStore.isLoggedIn) {
    uni.reLaunch({ url: '/pages/login/login' })
    return
  }
  
  // 刷新最新数据
  await userStore.refreshUserData()
})

onLoad(async () => {
  if (userStore.isLoggedIn) {
    const cats = await getCategories()
    categories.value = cats
    loading.value = false
  }
})
</script>
