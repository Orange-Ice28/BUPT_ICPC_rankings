<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useScoreData } from '@/composables/useScoreData'

const { data, loading, error, fetchData } = useScoreData()

onMounted(fetchData)

// 暑期训练共20场（牛客10场 + 杭电10场），华为比赛不计入成绩
const CONTEST_LABELS = [
  '牛客1', '牛客2', '牛客3', '牛客4', '牛客5',
  '牛客6', '牛客7', '牛客8', '牛客9', '牛客10',
  '杭电1', '杭电2', '杭电3', '杭电4', '杭电5',
  '杭电6', '杭电7', '杭电8', '杭电9', '杭电10',
]

interface TeamWithRank {
  name_cn: string
  members: { name: string }[]
  team_total: number
  rank: number
}

const sortedTeams = computed<TeamWithRank[]>(() => {
  const d = data.value
  if (!d) return []
  return d.teams
    .filter((t) => t.team_total > 0)
    .sort((a, b) => b.team_total - a.team_total)
    .map((t, i) => ({
      name_cn: t.name_cn,
      members: t.members,
      team_total: t.team_total,
      rank: i + 1,
    }))
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

function getMemberNames(members: { name: string }[]): string {
  return members.map((m) => m.name).join('、')
}
</script>

<template>
  <div class="summer-scores">
    <div class="page-header">
      <h2 class="page-title">暑期训练成绩</h2>
      <p class="page-desc">
        得分 = 过题数 / baseline × (601 − 排名) / 600 × 100 | 
        取最好 16 场（80%）的平均成绩计入总成绩
      </p>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">加载失败: {{ error }}</div>
    <template v-else-if="data">
      <div class="table-wrapper">
        <div class="table-scroll">
          <table class="team-score-table">
            <thead>
              <tr class="orange-header">
                <th class="col-rank col-sticky" style="left: 0">排名</th>
                <th class="col-team col-sticky" style="left: 62px">队伍</th>
                <th class="col-team-total col-sticky" style="left: 262px">队伍总成绩</th>
                <th v-for="(label, i) in CONTEST_LABELS" :key="i" class="col-contest">
                  {{ label }}
                </th>
              </tr>
              <tr class="sub-header orange-sub-header">
                <th colspan="3" class="col-sticky-group" style="left: 0"></th>
                <th v-for="(_, i) in CONTEST_LABELS" :key="i" class="col-contest-sub">
                  <span class="sub-item">过题</span>
                  <span class="sub-item">排名</span>
                  <span class="sub-item">得分</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="team in sortedTeams" :key="team.name_cn">
                <td class="col-rank col-sticky" style="left: 0" :class="getRankClass(team.rank)">{{ team.rank }}</td>
                <td class="col-team col-sticky" style="left: 62px">
                  <div class="team-name">{{ team.name_cn }}</div>
                  <div class="team-members">{{ getMemberNames(team.members) }}</div>
                </td>
                <td class="col-team-total col-sticky" style="left: 262px">
                  -
                </td>
                <td
                  v-for="(_, ci) in CONTEST_LABELS"
                  :key="ci"
                  class="col-contest"
                >
                  <span class="sub-item">-</span>
                  <span class="sub-item">-</span>
                  <span class="sub-item">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="rules-section">
        <div class="rules-header">
          <h3 class="rules-title">暑期训练评分规则</h3>
          <span class="rules-badge">2026~2027赛季</span>
        </div>

        <div class="rules-grid">
          <div class="rule-card rule-card--general">
            <div class="rule-card__icon">📋</div>
            <h4 class="rule-card__title">总体规则</h4>
            <ul class="rule-list">
              <li>比赛数据来自 <strong>牛客、杭电</strong> 平台，各 <strong>10 场</strong>训练赛，总计 <strong>20 场</strong></li>
              <li>取所有场次中成绩最好的 <strong>80%</strong> 场次计入总成绩，即取最好 <strong>16 场</strong>的平均成绩</li>
              <li><strong>队伍总成绩</strong> = 成绩最好的 80% 场次成绩的平均值</li>
              <li>成绩保留到小数点后 <strong>2 位</strong></li>
            </ul>
          </div>

          <div class="rule-card rule-card--formula">
            <div class="rule-card__icon"></div>
            <h4 class="rule-card__title">单场得分公式</h4>
            <div class="formula-box">
              <div class="formula-text">得分 = 过题数 / baseline × (601 − 排名) / 600 × 100</div>
            </div>
            <ul class="rule-list rule-list--compact">
              <li>排名使用<strong>全场排名</strong></li>
              <li>若得分 &lt; 0 或未参赛，按 <strong>0 分</strong>计算</li>
              <li><strong>Baseline 题数</strong>：一般情况下指全场第 10 名队伍过题数，可能根据实际情况灵活调整</li>
              <li>不取第 1 名队伍的过题数原因在于往年存在个别极强队伍（甚至有些不属于 Asia EC 赛区）过题数明显领先，导致大家的成绩被过度压缩，区分度不明显</li>
              <li>排名基数为 <strong>600</strong>，理论上平均每场位于集训队内最后 10% 左右的队伍，得分 = 0 分</li>
              <li>存在疑似违规现象的队伍，其当场成绩作废，得分按 <strong>0 分</strong>计算。如有需要，可在赛季训练群内申诉</li>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.summer-scores {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid #f59e0b;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 8px;
}

.page-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.8;
}

.table-wrapper {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.table-scroll {
  overflow-x: auto;
}

.team-score-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
  white-space: nowrap;
}

.team-score-table th,
.team-score-table td {
  padding: 10px 12px;
  text-align: center;
  border-bottom: 1px solid var(--border-light);
}

.col-sticky {
  position: sticky;
  z-index: 2;
  background: var(--bg-card);
}

.col-sticky-group {
  position: sticky;
  z-index: 2;
  background: #fef3c7;
}

.team-score-table thead .col-sticky {
  background: var(--primary-bg);
  z-index: 4;
}

.orange-header th {
  background: var(--primary-bg) !important;
  color: var(--primary-dark) !important;
}

.orange-header th.col-sticky {
  background: var(--primary-bg) !important;
}

.orange-sub-header th {
  background: #dbeafe !important;
}

.orange-sub-header th.col-sticky-group {
  background: #dbeafe !important;
}

.team-score-table thead th {
  background: var(--primary-bg);
  color: var(--primary-dark);
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 1;
}

.team-score-table .sub-header th {
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  background: #fef3c7;
}

.col-contest-sub .sub-item {
  display: inline-block;
  width: 42px;
  text-align: center;
}

.col-rank {
  width: 62px;
  min-width: 62px;
  font-weight: 600;
}

.col-team {
  width: 200px;
  min-width: 200px;
  text-align: left !important;
}

.team-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.team-members {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
}

.col-team-total {
  width: 100px;
  min-width: 100px;
  font-weight: 700;
}

.col-contest {
  min-width: 130px;
}

.col-contest .sub-item {
  display: inline-block;
  width: 42px;
  text-align: center;
  color: var(--text-muted);
}

.team-score-table tbody tr:hover {
  background: var(--primary-bg);
}

.team-score-table tbody tr:hover .col-sticky:not(.orange-header th) {
  background: var(--primary-bg);
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

.rules-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rules-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: linear-gradient(135deg, #d97706, #f59e0b);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.rules-title {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.rules-badge {
  display: inline-block;
  padding: 4px 14px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.rules-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.rule-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--primary);
  transition: box-shadow 0.2s ease;
}

.rule-card:hover {
  box-shadow: var(--shadow-md);
}

.rule-card--general {
  border-left-color: var(--success);
}

.rule-card--formula {
  border-left-color: var(--accent);
}

.rule-card--team {
  border-left-color: var(--primary-light);
}

.rule-card__icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.rule-card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

.rule-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rule-list--compact {
  gap: 8px;
}

.rule-list li {
  position: relative;
  padding-left: 20px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.rule-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 9px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
}

.rule-card--general .rule-list li::before {
  background: var(--success);
}

.rule-card--formula .rule-list li::before {
  background: var(--accent);
}

.rule-list li strong {
  color: var(--text-primary);
  font-weight: 600;
}

.formula-box {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 2px solid #fcd34d;
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 18px;
  text-align: center;
}

.formula-box--small {
  padding: 14px 20px;
}

.formula-text {
  font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
  font-size: 15px;
  font-weight: 700;
  color: #92400e;
  letter-spacing: 0.5px;
  word-break: break-all;
}

.formula-box--small .formula-text {
  font-size: 14px;
}

@media (max-width: 768px) {
  .rules-grid {
    grid-template-columns: 1fr;
  }

  .rules-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .formula-text {
    font-size: 13px;
  }
}
</style>