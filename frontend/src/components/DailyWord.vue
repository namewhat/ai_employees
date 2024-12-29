<template>
  <div class="daily-word">
    <div class="phone-frame">
      <div class="content-area">
        <div class="message-box">
          知识正以一种奇怪的方式<br/>传输到你的脑子里<br/>请注意接收
        </div>
        <div class="text-box">
          <!-- 单词卡片将在这里动态生成 -->
        </div>
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-placeholder">故事的小黄花</div>
            <div class="progress-inner">
              <div class="progress-text-container">
                <span class="progress-text"></span>
              </div>
              <span class="progress-number">0%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="action-buttons">
      <el-select v-model="selectedType" placeholder="选择词库" @change="handleTypeChange">
        <el-option label="全部" value="" />
        <el-option
          v-for="type in wordTypes"
          :key="type"
          :label="type"
          :value="type"
        />
      </el-select>
      <el-button class="library-btn" @click="showLibrary">
        <el-icon><Files /></el-icon>
      </el-button>
      <button class="refresh-btn" @click="restart">
        <el-icon><Refresh /></el-icon>
      </button>
    </div>
    <WordLibrary ref="wordLibrary" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { WordCardAnimation } from '../utils/wordAnimation'
import WordLibrary from './WordLibrary.vue'
import '../styles/dailyWord.css'

const animation = ref(null)
const wordLibrary = ref(null)
const selectedType = ref('')
const wordTypes = ref([])

onMounted(async () => {
  animation.value = new WordCardAnimation()
  await loadWordTypes()
  restart()
})

const loadWordTypes = async () => {
  try {
    const response = await fetch('/api/word/types')
    if (response.ok) {
      wordTypes.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to load word types:', error)
  }
}

const handleTypeChange = () => {
  restart()
}

const restart = () => {
  animation.value?.restart(selectedType.value)
}

const showLibrary = () => {
  wordLibrary.value?.show()
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 16px;
  align-items: center;
}

.el-select {
  width: 120px;
}

.library-btn {
  width: 56px;
  height: 56px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.library-btn:hover {
  transform: scale(1.05);
  background: #fff;
}

.library-btn:active {
  transform: scale(0.95);
}
</style>