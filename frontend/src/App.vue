<template>
  <el-container class="app-container">
    <el-aside width="auto">
      <Sidebar />
    </el-aside>
    <el-container>
      <el-header>
        <Header />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import Sidebar from './components/layout/Sidebar.vue'
import Header from './components/layout/Header.vue'
</script>

<style>
.app-container {
  height: 100vh;
}

.el-aside {
  background-color: #001529;
}

.el-header {
  padding: 0;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
}

.el-main {
  padding: 20px;
  background-color: #f0f2f5;
}
</style>
