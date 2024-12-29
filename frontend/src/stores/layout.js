import { defineStore } from 'pinia'
import { ref } from 'vue'
import { pinia } from './index'

export const useLayoutStore = defineStore('layout', () => {
  const isCollapse = ref(false)

  function toggleCollapse() {
    isCollapse.value = !isCollapse.value
  }

  return {
    isCollapse,
    toggleCollapse
  }
})

// 导出一个实例，以便在组件外使用
export const layoutStore = useLayoutStore(pinia) 