import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Quotes from '@/views/Quotes.vue'
import Images from '@/views/Images.vue'
import Publish from '@/views/Publish.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        title: '首页'
      }
    },
    {
      path: '/quotes',
      name: 'quotes',
      component: Quotes,
      meta: {
        title: '语录管理'
      }
    },
    {
      path: '/images',
      name: 'images',
      component: Images,
      meta: {
        title: '图片管理'
      }
    },
    {
      path: '/publish',
      name: 'publish',
      component: Publish,
      meta: {
        title: '公众号发布'
      }
    }
  ]
})

// 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - AI员工`
  next()
})

export default router 