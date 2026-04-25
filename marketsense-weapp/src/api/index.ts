// 小程序环境需要绝对路径，本地调试写死 http://127.0.0.1:8000/api/v1，上线时换成正式域名
const API_BASE = 'http://127.0.0.1:8000/api/v1'

export interface Option {
  label: string
  value: string
}

export interface Question {
  id: string
  type: 'text' | 'image' | 'predict'
  title: string
  image_url?: string
  options: Option[]
}

export interface LevelInfo {
  id: string
  name: string
  description: string
  sort_order: number
  video_url?: string
}

export interface Category {
  id: string
  name: string
  icon: string
  levels: LevelInfo[]
}

export interface AuthResponse {
  user_id: number
  hearts: number
  streak_days: number
  nickname?: string
  unlocked_levels: Record<string, string[]>
}

export interface CheckResponse {
  is_correct: boolean
  correct_answer: string
  explanation: string
  level_id: string
  category_id: string
}

export interface CompleteResponse {
  passed: boolean
  correct_count: number
  total_count: number
  next_unlocked: string | null
  hearts: number
  streak_days: number
}

export interface UserProfile {
  id: number
  phone: string | null
  nickname: string | null
  hearts: number
  streak_days: number
  created_at: string
  total_attempts: number
  total_correct: number
  overall_accuracy: number
  level_stats: { level_id: string; total: number; correct: number; accuracy: number }[]
  sessions: { level_id: string; correct_count: number; total_count: number; passed: number; created_at: string }[]
}

export interface WrongAnswerItem {
  record_id: number
  question_id: string
  level_id: string
  category_id: string
  user_answer: string
  correct_answer: string
  created_at: string
  title: string
  explanation: string
  options: Option[]
}

// 封装 uni.request
function request<T>(url: string, options: UniApp.RequestOptions = {}): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: API_BASE + url,
      method: options.method || 'GET',
      data: options.data,
      header: options.header || { 'Content-Type': 'application/json' },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T)
        } else {
          reject(new Error(`Request failed: ${res.statusCode}`))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

// ===== API 调用 =====
export async function authSync(deviceId: string): Promise<AuthResponse> {
  return request<AuthResponse>('/auth/sync', {
    method: 'POST',
    data: { device_id: deviceId },
  })
}

export async function getCategories(): Promise<Category[]> {
  return request<Category[]>('/categories')
}

export async function getLevelQuestions(levelId: string): Promise<Question[]> {
  const data = await request<{questions: Question[]}>(`/questions/${levelId}`)
  return data.questions
}

export async function checkAnswer(questionId: string, userAnswer: string, userId: number = 0): Promise<CheckResponse> {
  return request<CheckResponse>('/questions/check', {
    method: 'POST',
    data: { question_id: questionId, user_answer: userAnswer, user_id: userId },
  })
}

export async function phoneLogin(phone: string): Promise<AuthResponse> {
  return request<AuthResponse>('/auth/phone-login', {
    method: 'POST',
    data: { phone },
  })
}

export async function wxLogin(code: string): Promise<AuthResponse> {
  return request<AuthResponse>('/user/wx-login', {
    method: 'POST',
    data: { code },
  })
}

export async function getUserProfile(userId: number): Promise<UserProfile> {
  return request<UserProfile>(`/user/profile?user_id=${userId}`)
}

export async function getWrongAnswers(userId: number, levelId?: string): Promise<WrongAnswerItem[]> {
  const path = levelId
    ? `/user/wrong-answers?user_id=${userId}&level_id=${levelId}`
    : `/user/wrong-answers?user_id=${userId}`
  return request<WrongAnswerItem[]>(path)
}

export async function getDoneQuestions(userId: number, levelId?: string): Promise<string[]> {
  const path = levelId
    ? `/user/done-questions?user_id=${userId}&level_id=${levelId}`
    : `/user/done-questions?user_id=${userId}`
  return request<string[]>(path)
}

export async function getReviewQuestions(userId: number, levelId?: string): Promise<Question[]> {
  const path = levelId
    ? `/user/review-questions?user_id=${userId}&level_id=${levelId}`
    : `/user/review-questions?user_id=${userId}`
  return request<Question[]>(path)
}

export async function getAttemptedQuestions(userId: number, levelId?: string): Promise<string[]> {
  const path = levelId
    ? `/user/attempted-questions?user_id=${userId}&level_id=${levelId}`
    : `/user/attempted-questions?user_id=${userId}`
  return request<string[]>(path)
}

export async function completeLevel(
  userId: number,
  levelId: string,
  correctCount: number,
  totalCount: number
): Promise<CompleteResponse> {
  return request<CompleteResponse>('/progress/complete', {
    method: 'POST',
    data: {
      user_id: userId,
      level_id: levelId,
      correct_count: correctCount,
      total_count: totalCount,
    },
  })
}

export async function deductHeart(userId: number): Promise<{ hearts: number }> {
  return request<{ hearts: number }>(`/user/deduct-heart?user_id=${userId}`, {
    method: 'POST',
  })
}

export async function refillHearts(userId: number): Promise<{ hearts: number }> {
  return request<{ hearts: number }>(`/user/refill-hearts?user_id=${userId}`, {
    method: 'POST',
  })
}
