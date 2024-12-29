import { createRouter, createWebHistory } from 'vue-router'
import MaterialText from '../views/MaterialText.vue'
import MaterialImage from '../views/MaterialImage.vue'
import Publish from '../views/Publish.vue'
import DailyWord from '../components/DailyWord.vue'

const routes = [
  {
    path: '/',
    redirect: '/material-text'
  },
  {
    path: '/material-text',
    name: 'MaterialText',
    component: MaterialText
  },
  {
    path: '/material-image',
    name: 'MaterialImage',
    component: MaterialImage
  },
  {
    path: '/publish',
    name: 'Publish',
    component: Publish
  },
  {
    path: '/daily-word',
    name: 'DailyWord',
    component: DailyWord
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router