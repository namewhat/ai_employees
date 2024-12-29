<template>
  <div class="material-image">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>图片素材管理</span>
          <el-button type="primary" @click="handleUpload">上传图片</el-button>
        </div>
      </template>
      
      <el-upload
        class="upload-demo"
        action=""
        :auto-upload="false"
        :on-change="handleChange"
        multiple
        list-type="picture-card">
        <template #default>
          <el-icon><Plus /></el-icon>
        </template>
      </el-upload>
    </el-card>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'

const handleUpload = () => {
  // 上传图片的逻辑
}

const handleChange = (file) => {
  // 处理文件变化的逻辑
}
</script>

<style scoped>
.material-image {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  width: 100%;
}
</style> 