const API_BASE = import.meta.env.VITE_STOCKPILLAR_API_URL || 'https://layercake.com.cn/stockpillar/api/skill/v1'

function getHeaders() {
  return {
    Authorization: `Bearer ${import.meta.env.VITE_STOCKPILLAR_API_KEY}`,
    'Content-Type': 'application/json',
  }
}

export async function getKline(tsCode: string, startDate: string, endDate: string) {
  const url = `${API_BASE}/prices/kline?ts_code=${tsCode}&start_date=${startDate}&end_date=${endDate}`
  const res = await fetch(url, { headers: getHeaders() })
  if (!res.ok) throw new Error(`Kline API error: ${res.status}`)
  return res.json()
}

export async function getIndicators(tsCode: string, startDate: string, endDate: string, indicators: string) {
  const url = `${API_BASE}/technical/indicators?ts_code=${tsCode}&start_date=${startDate}&end_date=${endDate}&indicators=${indicators}`
  const res = await fetch(url, { headers: getHeaders() })
  if (!res.ok) throw new Error(`Indicators API error: ${res.status}`)
  return res.json()
}

export async function getRealtime(tsCodes: string) {
  const url = `${API_BASE}/prices/realtime?ts_codes=${tsCodes}`
  const res = await fetch(url, { headers: getHeaders() })
  if (!res.ok) throw new Error(`Realtime API error: ${res.status}`)
  return res.json()
}
