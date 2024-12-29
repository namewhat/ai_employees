import request from './request'

export interface Quote {
  id: number
  content: string
  source: string
  created_at: string
}

export interface QuoteList {
  items: Quote[]
  total: number
}

// 获取语录列表
export const getQuotes = (params: { skip?: number; limit?: number }) => {
  return request.get<QuoteList>('/quotes', { params })
}

// 上传语录文件
export const uploadQuotes = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<Quote[]>('/quotes/upload', formData)
}

// 生成语录
export const generateQuotes = (prompt: string, count: number = 10) => {
  return request.post<Quote[]>('/quotes/generate', { prompt, count })
}

// 随机获取语录
export const getRandomQuotes = (count: number = 5) => {
  return request.get<Quote[]>('/quotes/random', { params: { count } })
} 