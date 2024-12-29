import request from './request'

// 检查 Kimi 登录状态
export const checkKimiStatus = () => {
  return request.get('/auth/kimi/status')
}

// 检查可灵登录状态
export const checkKelingStatus = () => {
  return request.get('/auth/keling/status')
}

// 保存 Kimi Cookies
export const saveKimiCookies = (cookies: string) => {
  return request.post('/auth/kimi/cookies', { cookies })
}

// 保存可灵 Cookies
export const saveKelingCookies = (cookies: string) => {
  return request.post('/auth/keling/cookies', { cookies })
} 