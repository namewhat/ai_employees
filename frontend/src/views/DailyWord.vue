<template>
  <div class="daily-word">
    <div v-loading="wordStore.loading" class="word-list">
      <div v-for="word in wordStore.wordList" :key="word.id" class="word-item">
        <span>{{ word.word }}</span>
        <span>{{ word.translation }}</span>
      </div>
    </div>
    
    <el-pagination
      v-if="wordStore.pagination.total > 0"
      v-model:current-page="currentPage"
      :page-size="wordStore.pagination.perPage"
      :total="wordStore.pagination.total"
      @current-change="handlePageChange"
      layout="prev, pager, next"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useWordStore } from '@/stores/word'

const wordStore = useWordStore()
const currentPage = ref(1)

const handlePageChange = (page) => {
  wordStore.fetchWordList(page)
}

onMounted(async () => {
  await wordStore.fetchWordList()
})
</script>

<style scoped>
.daily-word {
  padding: 20px;
}

.word-list {
  min-height: 400px;
}

.word-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}
</style> 