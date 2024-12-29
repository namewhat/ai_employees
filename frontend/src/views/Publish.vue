<template>
  <div class="publish">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>公众号发布</span>
          <el-button type="primary" @click="handlePublish">发布</el-button>
        </div>
      </template>
      
      <el-form :model="form" label-width="120px">
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        
        <el-form-item label="选择语录">
          <el-select v-model="form.quotes" multiple placeholder="请选择语录">
            <el-option
              v-for="item in quoteOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="选择图片">
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
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const form = ref({
  title: '',
  quotes: [],
  images: []
})

const quoteOptions = ref([])

const handlePublish = () => {
  // 发布逻辑
}

const handleChange = (file) => {
  // 处理文件变化的逻辑
}
</script>

<style scoped>
.publish {
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