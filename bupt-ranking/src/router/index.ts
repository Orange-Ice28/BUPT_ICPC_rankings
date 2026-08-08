import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
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
        {
          path: 'scores-alt',
          name: 'summer-scores-alt',
          component: () => import('../views/SummerTrainingScoresAlt.vue'),
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
      path: '/overall-alt',
      name: 'overall-alt',
      component: () => import('../views/OverallScoreAlt.vue'),
    },
    {
      path: '/contests',
      name: 'contests',
      component: () => import('../views/ContestInfo.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/History.vue'),
    },
    {
      path: '/history-team',
      name: 'history-team',
      component: () => import('../views/History.vue'),
    },
  ],
})

export default router