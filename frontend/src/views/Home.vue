<template>
  <div class="home-page">
    <el-row :gutter="20">
      <!-- 数据统计卡片 -->
      <el-col :span="8">
        <el-card shadow="hover" class="mb-4">
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2"><Document /></el-icon>
              语录统计
            </div>
          </template>
          <div class="text-center">
            <div class="text-3xl font-bold mb-2">{{ stats.quotes }}</div>
            <div class="text-gray-500">总条数</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="mb-4">
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2"><Picture /></el-icon>
              图片统计
            </div>
          </template>
          <div class="text-center">
            <div class="text-3xl font-bold mb-2">{{ stats.images }}</div>
            <div class="text-gray-500">总数量</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="mb-4">
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2"><Share /></el-icon>
              发布统计
            </div>
          </template>
          <div class="text-center">
            <div class="text-3xl font-bold mb-2">{{ stats.published }}</div>
            <div class="text-gray-500">已发布</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最近操作记录 -->
    <el-card shadow="never">
      <template #header>
        <div class="flex items-center">
          <el-icon class="mr-2"><List /></el-icon>
          最近操作
        </div>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in recentActivities"
          :key="index"
          :timestamp="activity.created_at"
        >
          {{ activity.content }}
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Document, Picture, Share, List } from '@element-plus/icons-vue'
import { getStats, getRecentActivities } from '@/api/stats'

// 统计数据
const stats = ref({
  quotes: 0,
  images: 0,
  published: 0
})

// 最近活动
const recentActivities = ref([])

// 加载统计数据
const loadStats = async () => {
  try {
    const data = await getStats()
    stats.value = data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载最近活动
const loadActivities = async () => {
  try {
    const data = await getRecentActivities()
    recentActivities.value = data
  } catch (error) {
    console.error('加载最近活动失败:', error)
  }
}

onMounted(() => {
  loadStats()
  loadActivities()
})
</script> 