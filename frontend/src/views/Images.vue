<template>
  <div class="images-page">
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span>图片管理</span>
          <div class="flex gap-2">
            <el-upload
              :accept="'.jpg,.jpeg,.png'"
              :show-file-list="false"
              :multiple="true"
              :before-upload="handleUpload"
            >
              <el-button type="primary" :loading="uploading">
                <el-icon class="mr-1"><Upload /></el-icon>
                导入图片
              </el-button>
            </el-upload>
            <el-button type="success" @click="showGenerateDialog">
              <el-icon class="mr-1"><Plus /></el-icon>
              AI生成
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 图片网格 -->
      <div v-loading="loading" class="grid grid-cols-4 gap-4">
        <el-card
          v-for="image in images"
          :key="image.id"
          class="image-card"
          shadow="hover"
        >
          <div class="aspect-square relative">
            <img
              :src="image.path"
              class="w-full h-full object-cover"
              @error="handleImageError"
            />
            <div class="image-info absolute bottom-0 left-0 right-0 bg-black/50 text-white p-2 opacity-0 hover:opacity-100 transition-opacity">
              <div class="text-sm truncate">{{ image.source }}</div>
              <div class="text-xs text-gray-300">{{ formatDate(image.created_at) }}</div>
            </div>
          </div>
        </el-card>
      </div>
      
      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[12, 24, 48, 96]"
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
      title="AI生成图片"
      width="500px"
    >
      <el-form :model="generateForm" label-width="80px">
        <el-form-item label="描述">
          <el-input
            v-model="generateForm.prompt"
            placeholder="请输入图片描述"
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
            :max="4"
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
      title="登录可灵AI"
      width="800px"
      :close-on-click-modal="false"
      :show-close="true"
      :before-close="handleLoginDialogClose"
      :destroy-on-close="true"
    >
      <div class="relative">
        <iframe
          v-if="loginDialog"
          :src="kelingUrl"
          class="w-full h-[600px]"
          @load="handleIframeLoad"
        />
        <!-- 添加遮罩层，用于检测点击事件 -->
        <div 
          v-if="loginDialog" 
          class="absolute inset-0" 
          @click="handleIframeClick"
        />
      </div>
      
      <template #footer>
        <div class="flex justify-between w-full">
          <el-button @click="handleLoginDialogClose">取消</el-button>
          <el-button type="primary" @click="checkLogin">检查登录</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Plus, Picture } from '@element-plus/icons-vue'
import { getImages, uploadImages, generateImages } from '@/api/images'
import * as authApi from '@/api/auth'
import type { Image } from '@/api/images'

// 数据列表
const images = ref<Image[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// AI生成相关
const generateDialog = ref(false)
const generating = ref(false)
const generateForm = ref({
  prompt: '',
  count: 1
})

// 上传状态
const uploading = ref(false)

// 登录对话框
const loginDialog = ref(false)
const kelingUrl = 'https://www.kelingai.com/'
let iframeWindow: Window | null = null

// 登录状态
const isLoggedIn = ref(false)

// 提示词建议
const promptSuggestions = [
  '风景',
  '人物',
  '动物',
  '建筑',
  '插画',
  '写实',
  '抽象',
  '科技',
  '自然',
  '城市'
]

// 选择提示词
const selectPrompt = (prompt: string) => {
  generateForm.value.prompt = generateForm.value.prompt
    ? `${generateForm.value.prompt}, ${prompt}`
    : prompt
}

// 加载图片列表
const loadImages = async () => {
  try {
    loading.value = true
    const skip = (currentPage.value - 1) * pageSize.value
    const data = await getImages({ skip, limit: pageSize.value })
    images.value = data.items
    total.value = data.total
  } catch (error) {
    ElMessage.error('加载图片失败')
  } finally {
    loading.value = false
  }
}

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/placeholder.png'  // 替换为默认图片
}

// 处理文件上传
const handleUpload = async (file: File) => {
  try {
    uploading.value = true
    await uploadImages([file])
    ElMessage.success('上传成功')
    loadImages()
  } catch (error) {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
  return false
}

// 显示生成对话框
const showGenerateDialog = () => {
  generateDialog.value = true
  generateForm.value = {
    prompt: '',
    count: 1
  }
}

// 处理AI生成
const handleGenerate = async () => {
  if (!generateForm.value.prompt) {
    ElMessage.warning('请输入图片描述')
    return
  }
  
  // 先检查登录状态
  if (!isLoggedIn.value) {
    const loggedIn = await checkLoginStatus()
    if (!loggedIn) {
      loginDialog.value = true
      return
    }
  }
  
  try {
    generating.value = true
    await generateImages(generateForm.value.prompt, generateForm.value.count)
    ElMessage.success('生成成功')
    generateDialog.value = false
    loadImages()
  } catch (error: any) {
    if (error.response?.status === 401) {
      // 登录过期，显示登录对话框
      isLoggedIn.value = false
      loginDialog.value = true
    } else {
      ElMessage.error('生成失败')
      generateDialog.value = false
    }
  } finally {
    generating.value = false
  }
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 处理分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadImages()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadImages()
}

// 记录iframe加载次数
const iframeLoadCount = ref(0)

// 处理iframe加载
const handleIframeLoad = () => {
  iframeLoadCount.value++
  
  // 第一次加载是初始页面
  // 第二次加载通常是登录后的跳转
  if (iframeLoadCount.value > 1) {
    handleLoginSuccess()
  }
}

// 处理iframe点击
const handleIframeClick = () => {
  // 用户点击iframe时，开始轮询检查登录状态
  startLoginCheck()
}

// 轮询检查登录状态
let loginCheckInterval: number | null = null
const startLoginCheck = () => {
  if (loginCheckInterval) {
    return
  }
  
  loginCheckInterval = window.setInterval(async () => {
    try {
      await authApi.checkKelingStatus()
      // 如果请求成功，说明已经登录
      clearInterval(loginCheckInterval!)
      loginCheckInterval = null
      handleLoginSuccess()
    } catch (error) {
      // 继续等待
    }
  }, 1000)
}

// 处理登录对话框关闭
const handleLoginDialogClose = () => {
  if (loginCheckInterval) {
    clearInterval(loginCheckInterval)
    loginCheckInterval = null
  }
  iframeLoadCount.value = 0
  loginDialog.value = false
}

// 处理登录成功
const handleLoginSuccess = async () => {
  try {
    ElMessage.success('登录成功')
    isLoggedIn.value = true
    handleLoginDialogClose()
    
    // 重试之前失败的操作
    if (generateDialog.value) {
      handleGenerate()
    }
  } catch (error) {
    ElMessage.error('保存登录状态失败')
  }
}

// 检查登录状态
const checkLogin = async () => {
  try {
    await authApi.checkKelingStatus()
    handleLoginSuccess()
  } catch (error) {
    ElMessage.warning('请先完成登录')
  }
}

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    await authApi.checkKelingStatus()
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

// 在组件挂载时加载数据
onMounted(() => {
  loadImages()
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
.image-card {
  transition: all 0.3s;
}

.image-card:hover {
  transform: scale(1.02);
}

.image-info {
  transition: opacity 0.3s;
}

.el-tag {
  transition: all 0.3s;
}

.el-tag:hover {
  transform: scale(1.05);
}

/* 遮罩层样式 */
.absolute {
  position: absolute;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style> 