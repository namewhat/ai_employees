<template>
  <div class="header">
    <div class="left">
      <el-button
        type="text"
        @click="toggleSidebar"
      >
        <el-icon>
          <component :is="layoutStore.isCollapse ? 'Expand' : 'Fold'" />
        </el-icon>
      </el-button>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right">
      <el-dropdown>
        <span class="user-info">
          <el-avatar :size="32" icon="UserFilled" />
          <span class="username">管理员</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>个人设置</el-dropdown-item>
            <el-dropdown-item divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { layoutStore } from '../../stores/layout'
import { Expand, Fold, UserFilled } from '@element-plus/icons-vue'

const route = useRoute()

const currentRoute = computed(() => {
  const routeMap = {
    '/material-text': '语录素材',
    '/material-image': '图片素材',
    '/publish': '公众号发布',
    '/daily-word': '每日单词'
  }
  return routeMap[route.path] || '首页'
})

const toggleSidebar = () => {
  layoutStore.toggleCollapse()
}
</script>

<style scoped>
.header {
  height: 100%;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #333;
}
</style> 