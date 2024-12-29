import request from './request'

export interface QrCodeResponse {
  url: string
  key: string
}

export interface PublishItem {
  quote: string
  image: string
}

export interface PublishRequest {
  items: PublishItem[]
  textPosition: 'top' | 'middle' | 'bottom'
}

export interface PublishResponse {
  message: string
  articleUrl: string
}

// 获取登录二维码
export const getQrCode = () => {
  return request.get<QrCodeResponse>('/wechat/qrcode')
}

// 检查登录状态
export const checkWechatLogin = () => {
  return request.get<{ message: string }>('/wechat/status')
}

// 发布图文
export const publishArticle = (data: PublishRequest) => {
  return request.post<PublishResponse>('/wechat/publish', data)
}