<template>
  <el-menu
    :default-active="activeIndex"
    class="sidebar-menu"
    :collapse="layoutStore.isCollapse"
    background-color="#001529"
    text-color="#fff"
    active-text-color="#409EFF"
    router>
    
    <el-menu-item index="/material-text">
      <el-icon><Document /></el-icon>
      <span>语录素材</span>
    </el-menu-item>
    
    <el-menu-item index="/material-image">
      <el-icon><Picture /></el-icon>
      <span>图片素材</span>
    </el-menu-item>
    
    <el-menu-item index="/publish">
      <el-icon><Share /></el-icon>
      <span>公众号发布</span>
    </el-menu-item>

    <el-menu-item index="/daily-word">
      <el-icon><Reading /></el-icon>
      <span>每日单词</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { layoutStore } from '../../stores/layout'
import { Document, Picture, Share, Reading } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = computed(() => route.path)
</script>

<style scoped>
.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
}
</style> 