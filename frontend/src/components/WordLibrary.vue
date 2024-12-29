<template>
  <el-dialog
    title="词库管理"
    v-model="dialogVisible"
    width="70%">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="CET4" name="CET4">
        <el-table :data="cet4Words" height="400">
          <el-table-column prop="word" label="单词" width="150" />
          <el-table-column prop="phonetic" label="音标" width="150" />
          <el-table-column prop="meaning" label="释义" />
          <el-table-column label="学习次数" width="100">
            <template #default="scope">
              {{ getProgress(scope.row.id)?.study_count || 0 }}
            </template>
          </el-table-column>
          <el-table-column label="最后学习" width="180">
            <template #default="scope">
              {{ formatDate(getProgress(scope.row.id)?.last_study) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button size="small" type="danger" @click="deleteWord(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="CET6" name="CET6">
        <el-table :data="cet6Words" height="400">
          <el-table-column prop="word" label="单词" width="180" />
          <el-table-column prop="phonetic" label="音标" width="180" />
          <el-table-column prop="meaning" label="释义" />
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button size="small" type="danger" @click="deleteWord(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="importWords">导入词库</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { wordApi } from '../api/wordApi'
import { ElMessage } from 'element-plus'

const dialogVisible = ref(false)
const activeTab = ref('CET4')
const cet4Words = ref([])
const cet6Words = ref([])

const progressMap = ref(new Map())

const show = async () => {
  dialogVisible.value = true
  await loadWords()
}

const loadWords = async () => {
  try {
    const response = await wordApi.getWords()
    cet4Words.value = response.filter(word => word.type === 'CET4')
    cet6Words.value = response.filter(word => word.type === 'CET6')
    await loadProgress([...cet4Words.value, ...cet6Words.value])
  } catch (error) {
    ElMessage.error('加载词库失败')
  }
}

const loadProgress = async (words) => {
  for (const word of words) {
    try {
      const progress = await wordApi.getWordProgress(word.id)
      progressMap.value.set(word.id, progress)
    } catch (error) {
      console.error('Failed to load progress for word:', word.id)
    }
  }
}

const getProgress = (wordId) => {
  return progressMap.value.get(wordId)
}

const formatDate = (date) => {
  if (!date) return '未学习'
  return new Date(date).toLocaleString()
}

const deleteWord = async (word) => {
  try {
    await wordApi.deleteWord(word.id)
    await loadWords()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const importWords = () => {
  // 触发文件选择
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (file) {
      try {
        const reader = new FileReader()
        reader.onload = async (e) => {
          const words = JSON.parse(e.target.result)
          await wordApi.importWords(words)
          await loadWords()
          ElMessage.success('导入成功')
        }
        reader.readAsText(file)
      } catch (error) {
        ElMessage.error('导入失败')
      }
    }
  }
  input.click()
}

defineExpose({
  show
})
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.el-table {
  margin-top: 10px;
}
</style> 