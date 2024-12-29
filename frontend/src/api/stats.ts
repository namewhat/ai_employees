import request from './request'

export interface Stats {
  quotes: number
  images: number
  published: number
}

export interface Activity {
  id: number
  type: string
  content: string
  created_at: string
}

// 获取统计数据
export const getStats = () => {
  return request.get<Stats>('/stats')
}

// 获取最近活动
export const getRecentActivities = (limit: number = 10) => {
  return request.get<Activity[]>('/stats/activities', { params: { limit } })
} 