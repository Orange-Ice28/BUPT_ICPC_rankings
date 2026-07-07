import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
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
      redirect: '/summer/schedule',
      children: [
        {
          path: 'schedule',
          name: 'summer-schedule',
          component: () => import('../views/SummerTrainingSchedule.vue'),
        },
        {
          path: 'scores',
          name: 'summer-scores',
          component: () => import('../views/SummerTrainingScores.vue'),
        },
      ],
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
    {
      path: '/contests',
      name: 'contests',
      component: () => import('../views/ContestInfo.vue'),
    },
  ],
})

export default router