<template>
  <div class="word-input-container">
    <el-form :inline="true" class="word-form">
      <el-form-item>
        <el-input
          v-model="wordInput"
          placeholder="输入英文单词"
          clearable
          @keyup.enter="handleSearch"
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="chineseInput"
          placeholder="输入中文释义"
          clearable
          @keyup.enter="handleSearch"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">查询</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useWordStore } from '../stores/word'

const wordStore = useWordStore()
const wordInput = ref('')
const chineseInput = ref('')

const handleSearch = async () => {
  try {
    await wordStore.fetchDailyWord({
      word: wordInput.value,
      chinese: chineseInput.value
    })
    // 清空输入
    wordInput.value = ''
    chineseInput.value = ''
  } catch (error) {
    console.error('查询单词失败:', error)
  }
}
</script>

<style scoped>
.word-input-container {
  margin-bottom: 20px;
}

.word-form {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style> 