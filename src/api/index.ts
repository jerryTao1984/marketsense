const API_BASE = '/api/v1'

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

// ===== API 调用 =====
export async function authSync(deviceId: string): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/auth/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ device_id: deviceId }),
  })
  if (!res.ok) throw new Error(`Auth failed: ${res.status}`)
  return res.json()
}

export async function getCategories(): Promise<Category[]> {
  const res = await fetch(`${API_BASE}/categories`)
  if (!res.ok) throw new Error(`Categories failed: ${res.status}`)
  return res.json()
}

export async function getLevelQuestions(levelId: string): Promise<Question[]> {
  const res = await fetch(`${API_BASE}/questions/${levelId}`)
  if (!res.ok) throw new Error(`Questions failed: ${res.status}`)
  const data = await res.json()
  return data.questions
}

export async function checkAnswer(questionId: string, userAnswer: string, userId: number = 0): Promise<CheckResponse> {
  const res = await fetch(`${API_BASE}/questions/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question_id: questionId, user_answer: userAnswer, user_id: userId }),
  })
  if (!res.ok) throw new Error(`Check failed: ${res.status}`)
  return res.json()
}

export async function phoneLogin(phone: string): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/auth/phone-login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone }),
  })
  if (!res.ok) throw new Error(`Phone login failed: ${res.status}`)
  return res.json()
}

export async function getUserProfile(userId: number): Promise<UserProfile> {
  const res = await fetch(`${API_BASE}/user/profile?user_id=${userId}`)
  if (!res.ok) throw new Error(`Profile fetch failed: ${res.status}`)
  return res.json()
}

export async function getWrongAnswers(userId: number, levelId?: string): Promise<WrongAnswerItem[]> {
  const url = levelId
    ? `${API_BASE}/user/wrong-answers?user_id=${userId}&level_id=${levelId}`
    : `${API_BASE}/user/wrong-answers?user_id=${userId}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Wrong answers fetch failed: ${res.status}`)
  return res.json()
}

export async function getDoneQuestions(userId: number, levelId?: string): Promise<string[]> {
  const url = levelId
    ? `${API_BASE}/user/done-questions?user_id=${userId}&level_id=${levelId}`
    : `${API_BASE}/user/done-questions?user_id=${userId}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Done questions fetch failed: ${res.status}`)
  return res.json()
}

export async function getReviewQuestions(userId: number, levelId?: string): Promise<Question[]> {
  const url = levelId
    ? `${API_BASE}/user/review-questions?user_id=${userId}&level_id=${levelId}`
    : `${API_BASE}/user/review-questions?user_id=${userId}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Review questions fetch failed: ${res.status}`)
  return res.json()
}

export async function getAttemptedQuestions(userId: number, levelId?: string): Promise<string[]> {
  const url = levelId
    ? `${API_BASE}/user/attempted-questions?user_id=${userId}&level_id=${levelId}`
    : `${API_BASE}/user/attempted-questions?user_id=${userId}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Attempted questions fetch failed: ${res.status}`)
  return res.json()
}

export async function completeLevel(
  userId: number,
  levelId: string,
  correctCount: number,
  totalCount: number
): Promise<CompleteResponse> {
  const res = await fetch(`${API_BASE}/progress/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      level_id: levelId,
      correct_count: correctCount,
      total_count: totalCount,
    }),
  })
  if (!res.ok) throw new Error(`Complete failed: ${res.status}`)
  return res.json()
}

export async function deductHeart(userId: number): Promise<{ hearts: number }> {
  const res = await fetch(`${API_BASE}/user/deduct-heart?user_id=${userId}`, {
    method: 'POST',
  })
  if (!res.ok) throw new Error(`Deduct heart failed: ${res.status}`)
  return res.json()
}

export async function refillHearts(userId: number): Promise<{ hearts: number }> {
  const res = await fetch(`${API_BASE}/user/refill-hearts?user_id=${userId}`, {
    method: 'POST',
  })
  if (!res.ok) throw new Error(`Refill hearts failed: ${res.status}`)
  return res.json()
}
