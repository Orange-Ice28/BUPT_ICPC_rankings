<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useScoreData } from '@/composables/useScoreData'
import type { PersonalResult } from '@/types'

const { data, loading, error, fetchData } = useScoreData()

const activeTab = ref<'personal' | 'team'>('personal')

onMounted(fetchData)

const CONTEST_LABELS = [
  '第1场', '第2场', '第3场', '第4场', '第5场',
  '第6场', '第7场', '第8场', '第9场', '第10场',
]

const teamMembers = computed(() => {
  const d = data.value
  if (!d) return []
  const members = d.personal
    .filter((p) => p.in_team)
    .sort((a, b) => b.total_score - a.total_score)
  members.forEach((p, i) => (p.rank = i + 1))
  return members
})

function isBest(person: PersonalResult, contestIndex: number): boolean {
  return person.best_indices.includes(contestIndex)
}

function formatScore(score: number): string {
  if (score === 0 && score !== 0) return '0'
  return score.toFixed(2)
}

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

function getMemberName(members: { name: string }[], index: number): string {
  return members[index]?.name ?? '-'
}

function getMemberScore(members: { total_score: number }[], index: number): string {
  return members[index]?.total_score.toFixed(2) ?? '-'
}
</script>

<template>
  <div class="spring-training">
    <div class="page-header">
      <h2 class="page-title">春季训练成绩</h2>
      <p class="page-desc">
        得分 = 过题数 / baseline × (801 − 排名) / 800 × 100 | 
        team编号 ≤ team1791 取最佳7场，> team1791 取最佳5场 | 
        灰色底 = 未计入成绩的场次
      </p>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">加载失败: {{ error }}</div>
    <template v-else-if="data">
      <div class="tab-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'personal' }"
          @click="activeTab = 'personal'"
        >
          个人成绩
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'team' }"
          @click="activeTab = 'team'"
        >
          队伍成绩
        </button>
      </div>

      <div v-if="activeTab === 'personal'" class="table-wrapper">
        <div class="table-scroll">
          <table class="score-table">
            <thead>
              <tr>
                <th class="col-rank col-sticky" style="left: 0">排名</th>
                <th class="col-team-id col-sticky" style="left: 62px">队伍编号</th>
                <th class="col-name col-sticky" style="left: 172px">姓名</th>
                <th class="col-total col-sticky" style="left: 248px">总成绩</th>
                <th v-for="(label, i) in CONTEST_LABELS" :key="i" class="col-contest">
                  {{ label }}
                </th>
              </tr>
              <tr class="sub-header">
                <th colspan="4" class="col-sticky-group" style="left: 0"></th>
                <th v-for="(_, i) in CONTEST_LABELS" :key="i" class="col-contest-sub">
                  <span class="sub-item">过题</span>
                  <span class="sub-item">排名</span>
                  <span class="sub-item">得分</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="person in teamMembers" :key="person.team_id">
                <td class="col-rank col-sticky" style="left: 0" :class="getRankClass(person.rank)">{{ person.rank }}</td>
                <td class="col-team-id col-sticky" style="left: 62px">{{ person.team_id }}</td>
                <td class="col-name col-sticky" style="left: 172px">{{ person.name }}</td>
                <td class="col-total col-sticky" style="left: 248px" :class="getScoreClass(person.total_score)">
                  {{ person.total_score.toFixed(2) }}
                </td>
                <td
                  v-for="(contest, ci) in person.contests"
                  :key="ci"
                  class="col-contest"
                  :class="{ 'not-best': !isBest(person, ci) }"
                >
                  <span class="sub-item">{{ contest.solved }}</span>
                  <span class="sub-item">{{ contest.rank || '-' }}</span>
                  <span class="sub-item" :class="getScoreClass(contest.score)">
                    {{ contest.score.toFixed(2) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else class="table-wrapper">
        <table class="team-table">
          <thead>
            <tr>
              <th class="col-rank">排名</th>
              <th class="col-team-name">中文队名</th>
              <th class="col-team-en">英文队名</th>
              <th>队员1</th>
              <th>成绩</th>
              <th>队员2</th>
              <th>成绩</th>
              <th>队员3</th>
              <th>成绩</th>
              <th class="col-team-total">队伍总成绩</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="team in data.teams" :key="team.name_cn">
              <td class="col-rank" :class="getRankClass(team.rank)">{{ team.rank }}</td>
              <td class="col-team-name">{{ team.name_cn }}</td>
              <td class="col-team-en">{{ team.name_en }}</td>
              <template v-for="i in 3" :key="i">
                <td>{{ getMemberName(team.members, i - 1) }}</td>
                <td class="member-score">{{ getMemberScore(team.members, i - 1) }}</td>
              </template>
              <td class="col-team-total" :class="getScoreClass(team.team_total)">
                {{ team.team_total.toFixed(2) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    <div class="rules-section">
        <div class="rules-header">
          <h3 class="rules-title">春季训练评分规则</h3>
          <span class="rules-badge">2026~2027赛季</span>
        </div>

        <div class="rules-grid">
          <div class="rule-card rule-card--general">
            <div class="rule-card__icon">📋</div>
            <h4 class="rule-card__title">总体规则</h4>
            <ul class="rule-list">
              <li>比赛数据来自 <strong>HDU 平台</strong>，共 <strong>10 场</strong>个人训练赛</li>
              <li>由于春季没有集中时间进行组队训练，因此组队训练不计入成绩</li>
              <li>考虑到存在新生军训的情况，取所有场次中成绩最好的 <strong>70%</strong> 场次计入总成绩</li>
              <li>新生赛前参与训练的队员，取最好 <strong>7 场</strong>的平均成绩</li>
              <li>新生赛后参与训练的队员，取最好 <strong>5 场</strong>的平均成绩</li>
              <li>成绩保留到小数点后 <strong>2 位</strong></li>
            </ul>
          </div>

          <div class="rule-card rule-card--formula">
            <div class="rule-card__icon">🧮</div>
            <h4 class="rule-card__title">单场得分公式</h4>
            <div class="formula-box">
              <div class="formula-text">得分 = 过题数 / baseline × (801 − 排名) / 800 × 100</div>
            </div>
            <ul class="rule-list rule-list--compact">
              <li>排名使用 HDU 平台<strong>全场排名</strong></li>
              <li>若得分 &lt; 0 或未参赛，按 <strong>0 分</strong>计算</li>
              <li><strong>Baseline 题数</strong>：全场最高过题数（University 组中除特邀嘉宾外的最高过题数）</li>
              <li>排名基数为 <strong>800</strong>，理论上平均每场位于集训队内最后 10% 左右的选手，得分 = 0 分</li>
              <li>存在疑似违规现象的选手，其当场成绩作废，得分按 <strong>0 分</strong>计算</li>
            </ul>
          </div>

          <div class="rule-card rule-card--team">
            <div class="rule-card__icon">👥</div>
            <h4 class="rule-card__title">团队总成绩</h4>
            <div class="formula-box formula-box--small">
              <div class="formula-text">队伍总成绩 = 队伍所有成员个人总成绩的平均值</div>
            </div>
          </div>
        </div>

        <div class="rule-card rule-card--baseline">
          <div class="rule-card__icon">📊</div>
          <h4 class="rule-card__title">各场题数 Baseline</h4>
          <table class="baseline-table">
            <thead>
              <tr>
                <th v-for="n in 10" :key="n">第{{ n }}场</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>10</td>
                <td>10</td>
                <td>9</td>
                <td>10</td>
                <td>10</td>
                <td>9</td>
                <td>11</td>
                <td>8</td>
                <td>8</td>
                <td>10</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.spring-training {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
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

.tab-bar {
  display: flex;
  gap: 4px;
  background: var(--bg-card);
  padding: 4px;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  width: fit-content;
}

.tab-btn {
  padding: 8px 24px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: var(--primary);
  background: var(--primary-bg);
}

.tab-btn.active {
  background: var(--primary);
  color: #fff;
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

.score-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
  white-space: nowrap;
}

.team-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  white-space: nowrap;
}

.score-table th,
.score-table td {
  padding: 10px 12px;
  text-align: center;
  border-bottom: 1px solid var(--border-light);
}

.team-table th,
.team-table td {
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
  background: #e8f0fe;
  width: 328px;
}

.score-table thead .col-sticky {
  background: var(--primary-bg);
  z-index: 4;
}

.score-table .sub-header .col-sticky-group {
  background: #e8f0fe;
  z-index: 4;
}

.score-table tbody tr:hover .col-sticky {
  background: var(--primary-bg);
}

.score-table thead th,
.team-table thead th {
  background: var(--primary-bg);
  color: var(--primary-dark);
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 1;
}

.score-table .sub-header th {
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  background: #e8f0fe;
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

.col-team-id {
  width: 110px;
  min-width: 110px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: var(--text-secondary);
}

.col-name {
  width: 76px;
  min-width: 76px;
  font-weight: 500;
  text-align: left !important;
}

.col-total {
  width: 80px;
  min-width: 80px;
  font-weight: 700;
}

.col-contest {
  min-width: 130px;
}

.col-contest .sub-item {
  display: inline-block;
  width: 42px;
  text-align: center;
}

.col-team-name {
  min-width: 120px;
  text-align: left !important;
  font-weight: 500;
}

.col-team-en {
  min-width: 140px;
  font-size: 12px;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
}

.col-team-total {
  font-weight: 700;
}

.member-score {
  font-weight: 500;
}

.not-best {
  background: var(--gray-bg) !important;
}

.score-table tbody tr:hover,
.team-table tbody tr:hover {
  background: var(--primary-bg);
}

.section-divider .divider-cell {
  padding: 8px 16px;
  background: var(--gray-bg);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  text-align: left;
  letter-spacing: 1px;
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
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
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

.rules-grid .rule-card--team {
  grid-column: 1 / -1;
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

.rule-card--baseline {
  border-left-color: var(--danger);
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

.baseline-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
}

.baseline-table thead th {
  background: #fef2f2;
  color: #991b1b;
  font-weight: 600;
  padding: 12px 10px;
  text-align: center;
  font-size: 13px;
  border-bottom: 2px solid #fecaca;
}

.baseline-table tbody td {
  padding: 12px 10px;
  text-align: center;
  font-weight: 700;
  font-size: 18px;
  font-family: 'Courier New', 'Consolas', monospace;
  color: var(--text-primary);
  background: #fff;
  border-bottom: 1px solid var(--border-light);
}

.baseline-table tbody tr:last-child td {
  border-bottom: none;
}

.baseline-table tbody tr:hover td {
  background: var(--primary-bg);
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

  .baseline-table {
    font-size: 12px;
  }

  .baseline-table tbody td {
    font-size: 15px;
    padding: 8px 6px;
  }
}
</style>