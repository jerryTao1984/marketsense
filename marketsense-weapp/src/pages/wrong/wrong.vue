<style scoped>
.wrong-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}
.list-container {
  padding: 12px;
}
.wrong-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}
.level-tag {
  background: #f0f2f5;
  color: #666;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.time {
  font-size: 12px;
  color: #999;
}
.title {
  font-size: 15px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
  display: block;
  line-height: 1.5;
}
.answer-box {
  background: #fafafa;
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 12px;
}
.wrong-ans {
  color: #f44336;
  margin-bottom: 4px;
  display: block;
}
.correct-ans {
  color: #4CAF50;
  display: block;
}
.explanation {
  font-size: 13px;
  color: #666;
  background: #fff8e1;
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid #ffc107;
}
.empty {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 14px;
}
</style>

<template>
  <view class="wrong-page">
    <view class="list-container" v-if="wrongs.length">
      <view class="wrong-card" v-for="item in wrongs" :key="item.record_id">
        <view class="card-header">
          <text class="level-tag">{{ getLevelName(item.level_id) }}</text>
          <text class="time">{{ formatDate(item.created_at) }}</text>
        </view>
        <text class="title">{{ item.title }}</text>
        <view class="answer-box">
          <text class="wrong-ans">我的答案：{{ getOptionLabel(item, item.user_answer) }}</text>
          <text class="correct-ans">正确答案：{{ getOptionLabel(item, item.correct_answer) }}</text>
        </view>
        <view class="explanation">
          <text>解析：{{ item.explanation }}</text>
        </view>
      </view>
    </view>
    <view class="empty" v-else>
      太棒了，目前没有错题记录！
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/user'
import { getWrongAnswers, type WrongAnswerItem } from '../../api'

const userStore = useUserStore()
const wrongs = ref<WrongAnswerItem[]>([])

const levelNames: Record<string, string> = {
  L1: '市场基础', L2: '财务报表', L3: '技术指标', L4: '投资策略',
  T1: '海豚交易法', T2: '海龟交易法', T3: '深度估值', T4: '波动率反转',
  K1: '单根K线', K2: 'K线组合', K3: '趋势形态', K4: '量价分析',
  P1: '下周涨跌预测', P2: '趋势转折预测', P3: '支撑压力预测',
}

function getLevelName(id: string) {
  return levelNames[id] || id
}

function getOptionLabel(item: WrongAnswerItem, val: string) {
  const opt = item.options.find(o => o.value === val)
  return opt ? opt.label : val
}

function formatDate(dateStr: string) {
  const d = new Date(dateStr)
  return `${d.getMonth()+1}-${d.getDate()} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
}

onLoad(async () => {
  if (userStore.userId) {
    const data = await getWrongAnswers(userStore.userId)
    wrongs.value = [...data].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }
})
</script>
