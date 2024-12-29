import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 60000
})

request.interceptors.response.use(
  response => response.data,
  error => {
    // 如果是401错误，不显示错误消息
    if (error.response?.status !== 401) {
      const message = error.response?.data?.detail || error.message || '请求失败'
      ElMessage.error(message)
    }
    return Promise.reject(error)
  }
)

export default request 