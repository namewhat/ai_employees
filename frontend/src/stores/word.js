import { defineStore } from 'pinia'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

export const useWordStore = defineStore('word', {
  state: () => ({
    wordList: [],
    pagination: {
      total: 0,
      currentPage: 1,
      perPage: 20,
      totalPages: 0
    },
    loading: false
  }),
  
  actions: {
    async fetchWordList(page = 1) {
      if (this.loading) return;
      
      this.loading = true
      try {
        const response = await request.get('/api/word/list', {
          params: {
            page,
            per_page: this.pagination.perPage
          }
        })
        
        if (response.data.success) {
          this.wordList = response.data.data
          this.pagination = response.data.pagination
        } else {
          ElMessage.error(response.data.message || '获取单词列表失败')
        }
      } catch (error) {
        console.error('获取单词列表失败:', error)
        ElMessage.error(error.response?.data?.message || '获取单词列表失败')
      } finally {
        this.loading = false
      }
    }
  }
}) 