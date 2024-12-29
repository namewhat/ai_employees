<template>
  <div class="material-text">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>语录素材管理</span>
          <el-button type="primary" @click="showAddDialog">添加语录</el-button>
        </div>
      </template>
      
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="content" label="语录内容" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([])

const showAddDialog = () => {
  // 添加语录的逻辑
}

const handleEdit = (row) => {
  // 编辑语录的逻辑
}

const handleDelete = (row) => {
  // 删除语录的逻辑
}
</script>

<style scoped>
.material-text {
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