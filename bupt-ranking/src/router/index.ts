import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/spring',
    },
    {
      path: '/spring',
      name: 'spring',
      component: () => import('../views/SpringTraining.vue'),
    },
    {
      path: '/summer',
      name: 'summer',
      component: () => import('../views/SummerTraining.vue'),
    },
    {
      path: '/online',
      name: 'online',
      component: () => import('../views/OnlineContest.vue'),
    },
    {
      path: '/overall',
      name: 'overall',
      component: () => import('../views/OverallScore.vue'),
    },
  ],
})

export default router