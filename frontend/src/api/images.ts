import request from './request'

export interface Image {
  id: number
  path: string
  source: string
  prompt?: string
  created_at: string
}

export interface ImageList {
  items: Image[]
  total: number
}

// 获取图片列表
export const getImages = (params: { skip?: number; limit?: number }) => {
  return request.get<ImageList>('/images', { params })
}

// 上传图片文件
export const uploadImages = (files: File[]) => {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })
  return request.post<Image[]>('/images/upload', formData)
}

// 生成图片
export const generateImages = (prompt: string, count: number = 1) => {
  return request.post<Image[]>('/images/generate', { prompt, count })
}

// 随机获取图片
export const getRandomImages = (count: number = 5) => {
  return request.get<Image[]>('/images/random', { params: { count } })
} 