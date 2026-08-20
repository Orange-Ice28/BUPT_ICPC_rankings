<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScoreData } from '@/composables/useScoreData'
import { recalcTeam } from '@/utils/summerAltScoring'

const route = useRoute()
const router = useRouter()

const { data, summerData, loading, error, fetchData, fetchSummerData } = useScoreData()

const isAltPage = computed(() => route.name === 'overall-alt')

function handleSunClick() {
  if (isAltPage.value) {
    router.push({ name: 'overall' })
  } else {
    router.push({ name: 'overall-alt' })
  }
}

onMounted(() => {
  fetchData()
  fetchSummerData()
})

interface OverallTeam {
  name_cn: string
  name_en: string
  members: string[]
  spring_score: number
  summer_score: number
  online_score: number
  overall_score: number
  rank: number
}

const overallTeams = computed(() => {
  const d = data.value
  const sd = summerData.value
  if (!d) return []

  // 构建暑期训练队伍成绩映射（使用备选评分规则）
  const summerTeamMap = new Map<string, number>()
  if (sd && sd.teams) {
    for (const team of sd.teams) {
      const recalculated = recalcTeam(team)
      summerTeamMap.set(team.name_cn, recalculated.team_total)
    }
  }

  const teams: OverallTeam[] = d.teams.map((t) => {
    const spring = t.team_total
    const summer = summerTeamMap.get(t.name_cn) || 0
    const online = 0
    const overall = spring * 0.1 + summer * 0.6 + online * 0.3
    return {
      name_cn: t.name_cn,
      name_en: t.name_en,
      members: t.members.map((m) => m.name),
      spring_score: spring,
      summer_score: summer,
      online_score: online,
      overall_score: Math.round(overall * 100) / 100,
      rank: 0,
    }
  })

  teams.sort((a, b) => b.overall_score - a.overall_score)

  // 计算并列排名
  let currentRank = 1
  let prevScore = -1
  teams.forEach((t, i) => {
    if (t.overall_score !== prevScore) {
      currentRank = i + 1
      prevScore = t.overall_score
    }
    t.rank = currentRank
  })

  return teams
})

const hasSummerData = computed(() => {
  const sd = summerData.value
  if (!sd || !sd.teams) return false
  return sd.teams.some((t: any) => t.team_total > 0)
})

function getRankClass(rank: number): string {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return ''
}

function getScoreClass(score: number): string {
  if (score >= 60) return 'score-excellent'
  if (score >= 40) return 'score-good'
  if (score >= 20) return 'score-medium'
  return 'score-low'
}
</script>

<template>
  <div class="overall-score">
    <div class="page-header">
      <h2 class="page-title">
        <span
          class="sun-icon"
          :class="{ 'sun-icon--alt': isAltPage }"
          @click="handleSunClick"
          :title="isAltPage ? '点击切换至默认评分规则' : '点击切换至备选评分规则'"
        >☀️</span>
        总成绩
      </h2>
      <p class="page-desc">
        总成绩 = 春季训练 × 10% + 暑期训练 × 60% + 网络赛 × 30%
      </p>
      <div class="formula-cards">
        <div class="formula-card formula-card--spring">
          <div class="formula-label">春季训练</div>
          <div class="formula-weight">× 10%</div>
        </div>
        <div class="formula-card formula-card--summer" :class="{ pending: !hasSummerData }">
          <div class="formula-label">暑期训练</div>
          <div class="formula-weight">× 60%</div>
        </div>
        <div class="formula-card pending">
          <div class="formula-label">网络赛</div>
          <div class="formula-weight">× 30%</div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">加载失败: {{ error }}</div>
    <template v-else-if="data">
      <div class="table-wrapper">
        <table class="overall-table">
          <thead>
            <tr>
              <th class="col-rank">排名</th>
              <th class="col-team-name">队名</th>
              <th class="col-members">队员</th>
              <th class="col-score">春季训练 (×10%)</th>
              <th class="col-score">暑期训练 (×60%)</th>
              <th class="col-score">网络赛 (×30%)</th>
              <th class="col-total">总成绩</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="team in overallTeams" :key="team.name_cn">
              <td class="col-rank" :class="getRankClass(team.rank)">{{ team.rank }}</td>
              <td class="col-team-name">
                <span class="team-cn">{{ team.name_cn }}</span>
                <span class="team-en">{{ team.name_en }}</span>
              </td>
              <td class="col-members">{{ team.members.join('、') }}</td>
              <td class="col-score">{{ team.spring_score.toFixed(2) }}</td>
              <td class="col-score" :class="{ 'pending-score': team.summer_score === 0 }">{{ team.summer_score.toFixed(2) }}</td>
              <td class="col-score pending-score">{{ team.online_score.toFixed(2) }}</td>
              <td class="col-total" :class="getScoreClass(team.overall_score)">
                {{ team.overall_score.toFixed(2) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<style scoped>
.overall-score {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid #ec4899;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 8px;
}

.sun-icon {
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease, filter 0.2s ease;
  user-select: none;
}

.sun-icon:hover {
  transform: scale(1.2);
  filter: brightness(1.3);
}

.sun-icon--alt {
  filter: drop-shadow(0 0 6px #f59e0b);
}

.page-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.8;
}

.formula-cards {
  display: flex;
  gap: 12px;
}

.formula-card {
  flex: 1;
  background: var(--primary-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  text-align: center;
}

.formula-card--spring {
  background: #ecfdf5;
  border-color: #10b981;
}

.formula-card--spring .formula-weight {
  color: #10b981;
}

.formula-card--summer {
  background: #fff7ed;
  border-color: #f59e0b;
}

.formula-card--summer .formula-weight {
  color: #f59e0b;
}

.formula-card.pending {
  background: var(--gray-bg);
  border-style: dashed;
}

.formula-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.formula-card.pending .formula-label {
  color: var(--text-muted);
}

.formula-weight {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
}

.formula-card.pending .formula-weight {
  color: var(--text-muted);
}

.table-wrapper {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.overall-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.overall-table th,
.overall-table td {
  padding: 8px 16px;
  text-align: center;
  border-bottom: 1px solid var(--border-light);
}

.overall-table thead th {
  font-size: 14px;
  padding: 10px 16px;
  border-bottom: 2px solid var(--border);
  background: var(--primary-bg);
  color: var(--primary-dark);
  font-weight: 600;
}

.col-rank {
  width: 70px;
  font-weight: 600;
}

.col-team-name {
  width: 180px;
  text-align: left !important;
}

.team-cn {
  display: block;
  font-weight: 700;
  font-size: 15px;
  color: var(--text-primary);
}

.team-en {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
  margin-top: 2px;
}

.col-members {
  width: 160px;
  font-size: 14px;
  text-align: left !important;
}

.col-score {
  width: 150px;
  font-variant-numeric: tabular-nums;
}

.col-total {
  width: 100px;
  font-weight: 700;
  font-size: 15px;
}

.pending-score {
  color: var(--text-muted);
  font-style: italic;
}

.rank-gold {
  color: #b45309;
  font-weight: 700;
}

.rank-gold::before {
  content: '🥇';
  margin-right: 2px;
}

.rank-silver {
  color: #6b7280;
  font-weight: 700;
}

.rank-silver::before {
  content: '🥈';
  margin-right: 2px;
}

.rank-bronze {
  color: #92400e;
  font-weight: 700;
}

.rank-bronze::before {
  content: '🥉';
  margin-right: 2px;
}

.overall-table tbody tr:nth-child(even) {
  background: #f8fafc;
}

.overall-table tbody tr:nth-child(even):hover {
  background: var(--primary-bg);
}

.overall-table tbody tr:hover {
  background: var(--primary-bg);
}

.overall-table tbody td {
  padding: 10px 16px;
  vertical-align: middle;
}

.col-total {
  font-variant-numeric: tabular-nums;
}

.score-excellent {
  color: var(--success);
  font-weight: 600;
}

.score-good {
  color: var(--primary);
  font-weight: 600;
}

.score-medium {
  color: var(--warning);
  font-weight: 600;
}

.score-low {
  color: var(--danger);
  font-weight: 600;
}

.loading,
.error {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: var(--text-secondary);
}

.error {
  color: var(--danger);
}
</style>
