<template>
  <div class="quotes-page">
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span>语录管理</span>
          <div class="flex gap-2">
            <el-upload
              :accept="'.txt'"
              :show-file-list="false"
              :before-upload="handleUpload"
              :multiple="false"
            >
              <el-button type="primary" :loading="uploading">
                <el-icon class="mr-1"><Upload /></el-icon>
                导入文件
              </el-button>
            </el-upload>
            <el-button type="success" @click="showGenerateDialog">
              <el-icon class="mr-1"><Plus /></el-icon>
              AI生成
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 语录列表 -->
      <el-table
        v-loading="loading"
        :data="quotes"
        style="width: 100%"
      >
        <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="source" label="来源" width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          :background="true"
          layout="sizes, prev, pager, next, total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- AI生成对话框 -->
    <el-dialog
      v-model="generateDialog"
      title="AI生成语录"
      width="500px"
    >
      <el-form :model="generateForm" label-width="80px">
        <el-form-item label="主题">
          <el-input
            v-model="generateForm.prompt"
            placeholder="请输入生成主题"
            type="textarea"
            :rows="3"
          />
          <!-- 添加提示词建议 -->
          <div class="mt-2 flex flex-wrap gap-2">
            <el-tag
              v-for="prompt in promptSuggestions"
              :key="prompt"
              class="cursor-pointer hover:bg-blue-100"
              @click="selectPrompt(prompt)"
            >
              {{ prompt }}
            </el-tag>
          </div>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number
            v-model="generateForm.count"
            :min="1"
            :max="20"
            controls-position="right"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="generateDialog = false">取消</el-button>
        <el-button
          type="primary"
          :loading="generating"
          @click="handleGenerate"
        >
          生成
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 登录对话框 -->
    <el-dialog
      v-model="loginDialog"
      title="请先登录"
      width="400px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="text-center">
        <div class="mb-4">请使用浏览器打开以下地址完成登录：</div>
        <div class="text-blue-500 mb-4">
          <a :href="settings.KIMI_URL" target="_blank">{{ settings.KIMI_URL }}</a>
        </div>
        <div class="text-gray-500 text-sm">登录成功后会自动关闭此窗口</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Plus } from '@element-plus/icons-vue'
import * as quotesApi from '@/api/quotes'
import * as authApi from '@/api/auth'
import { settings } from '@/config'

// 数据加载状态
const loading = ref(false)
const uploading = ref(false)
const generating = ref(false)

// 语录列表数据
const quotes = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 生成对话框
const generateDialog = ref(false)
const generateForm = ref({
  prompt: '',
  count: 10
})

// 提示词建议
const promptSuggestions = settings.PROMPT_SUGGESTIONS.QUOTES

// 登录相关
const loginDialog = ref(false)
const isLoggedIn = ref(false)
let loginCheckInterval: number | null = null

// 加载语录列表
const loadQuotes = async () => {
  try {
    loading.value = true
    const data = await quotesApi.getQuotes({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    quotes.value = data.items
    total.value = data.total
  } catch (error) {
    ElMessage.error('加载语录失败')
  } finally {
    loading.value = false
  }
}

// 处理分页
const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadQuotes()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadQuotes()
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 选择���示词
const selectPrompt = (prompt: string) => {
  generateForm.value.prompt = prompt
}

// 显示生成对话框
const showGenerateDialog = async () => {
  if (await checkLoginStatus()) {
    generateDialog.value = true
  }
}

// 处理文件上传
const handleUpload = async (file: File) => {
  try {
    uploading.value = true
    await quotesApi.uploadQuotes(file)
    ElMessage.success('上传成功')
    loadQuotes()
    return false
  } catch (error) {
    ElMessage.error('上传失败')
    return false
  } finally {
    uploading.value = false
  }
}

// 处理生成
const handleGenerate = async () => {
  if (!generateForm.value.prompt) {
    ElMessage.warning('请输入生成主题')
    return
  }
  
  try {
    generating.value = true
    await quotesApi.generateQuotes(generateForm.value)
    ElMessage.success('生成成功')
    generateDialog.value = false
    loadQuotes()
  } catch (error: any) {
    if (error.response?.status === 401) {
      showLoginDialog()
    } else {
      ElMessage.error('生成失败')
    }
  } finally {
    generating.value = false
  }
}

// 开始检查登录状态
const startLoginCheck = () => {
  if (loginCheckInterval) {
    return
  }
  
  // 立即检查一次
  checkLoginStatus()
  
  loginCheckInterval = window.setInterval(async () => {
    const success = await checkLoginStatus()
    if (success) {
      // 登录成功，清理定时器并关闭对话框
      if (loginCheckInterval) {
        clearInterval(loginCheckInterval)
        loginCheckInterval = null
      }
      loginDialog.value = false
      handleLoginSuccess()
    }
  }, 2000)  // 每2秒检查一次
}

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    await authApi.checkKimiStatus()
    isLoggedIn.value = true
    return true
  } catch (error: any) {
    // 只有在非401错误时才显示错误消息
    if (error.response?.status !== 401) {
      ElMessage.error('检查登录状态失败')
    }
    isLoggedIn.value = false
    return false
  }
}

// 显示登录对话框
const showLoginDialog = () => {
  loginDialog.value = true
  startLoginCheck()
}

// 处理登录成功
const handleLoginSuccess = async () => {
  ElMessage.success('登录成功')
  isLoggedIn.value = true
  
  // 重试之前失败的操作
  if (generateDialog.value) {
    await handleGenerate()
  }
}

// 在组件挂载时加载数据
onMounted(() => {
  loadQuotes()
  checkLoginStatus()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (loginCheckInterval) {
    clearInterval(loginCheckInterval)
    loginCheckInterval = null
  }
})
</script>

<style scoped>
.el-tag {
  transition: all 0.3s;
}

.el-tag:hover {
  transform: scale(1.05);
}
</style> 