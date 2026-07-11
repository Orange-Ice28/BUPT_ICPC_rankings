<script setup lang="ts">
import { computed } from 'vue'
import teamData from '@/data/history_team_data.json'

interface TeamRecord {
  name_cn: string
  name_en: string
  members: string[]
  gold: number
  silver: number
  bronze: number
}

interface RankedTeam extends TeamRecord {
  rank: number
}

const teams = computed(() => {
  const data = teamData as TeamRecord[]
  const sorted = [...data].sort((a, b) => {
    if (b.gold !== a.gold) return b.gold - a.gold
    if (b.silver !== a.silver) return b.silver - a.silver
    return b.bronze - a.bronze
  })

  const ranked: RankedTeam[] = []
  let currentRank = 1
  for (let i = 0; i < sorted.length; i++) {
    if (i > 0) {
      const prev = sorted[i - 1]
      const curr = sorted[i]
      if (
        prev.gold !== curr.gold ||
        prev.silver !== curr.silver ||
        prev.bronze !== curr.bronze
      ) {
        currentRank = i + 1
      }
    }
    ranked.push({ ...sorted[i], rank: currentRank })
  }
  return ranked
})

function getMedalClass(count: number): string {
  if (count > 0) return 'has-medal'
  return 'no-medal'
}

function getRankDisplay(rank: number): string {
  if (rank === 1) return '🥇'
  if (rank === 2) return '🥈'
  if (rank === 3) return '🥉'
  return String(rank)
}

function getRankClass(rank: number): string {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return ''
}
</script>

<template>
  <div class="history-team">
    <div class="table-wrapper">
      <table class="history-table">
        <thead>
          <tr>
            <th class="col-rank">排名</th>
            <th class="col-team-name">中文队名</th>
            <th class="col-team-en">英文队名</th>
            <th class="col-members">队员</th>
            <th class="col-medal">🥇 金牌</th>
            <th class="col-medal">🥈 银牌</th>
            <th class="col-medal">🥉 铜牌</th>
            <th class="col-total">总计</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="team in teams" :key="team.name_cn">
            <td class="col-rank" :class="getRankClass(team.rank)">{{ getRankDisplay(team.rank) }}</td>
            <td class="col-team-name">{{ team.name_cn }}</td>
            <td class="col-team-en">{{ team.name_en }}</td>
            <td class="col-members">{{ team.members.join('、') }}</td>
            <td class="col-medal" :class="getMedalClass(team.gold)">{{ team.gold }}</td>
            <td class="col-medal" :class="getMedalClass(team.silver)">{{ team.silver }}</td>
            <td class="col-medal" :class="getMedalClass(team.bronze)">{{ team.bronze }}</td>
            <td class="col-total">{{ team.gold + team.silver + team.bronze }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.history-team {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.table-wrapper {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
}

.history-table thead th {
  background: #f8fafc;
  color: var(--text-secondary);
  font-weight: 600;
  padding: 14px 20px;
  text-align: center;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
  font-size: 15px;
}

.history-table thead th.col-team-name,
.history-table thead th.col-members {
  text-align: left;
}

.history-table tbody td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  text-align: center;
  vertical-align: middle;
}

.history-table tbody td.col-team-name,
.history-table tbody td.col-members {
  text-align: left;
}

.history-table tbody tr:last-child td {
  border-bottom: none;
}

.history-table tbody tr:hover {
  background: var(--primary-bg);
}

.col-rank {
  width: 60px;
  font-weight: 700;
  font-size: 18px;
}

.col-team-name {
  min-width: 120px;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 16px;
}

.col-team-en {
  min-width: 100px;
  color: var(--text-secondary);
  font-size: 14px;
}

.col-members {
  min-width: 150px;
  color: var(--text-primary);
  font-size: 15px;
}

.col-medal {
  width: 70px;
  font-weight: 600;
  font-size: 16px;
}

.col-medal.has-medal {
  color: var(--text-primary);
}

.col-medal.no-medal {
  color: var(--text-muted);
}

.col-total {
  width: 60px;
  font-weight: 700;
  color: var(--primary);
  font-size: 18px;
}

.rank-gold {
  color: #f59e0b;
}

.rank-silver {
  color: #94a3b8;
}

.rank-bronze {
  color: #d97706;
}

@media (max-width: 768px) {
  .history-table {
    font-size: 12px;
  }

  .history-table thead th,
  .history-table tbody td {
    padding: 10px 12px;
  }

  .col-team-en {
    display: none;
  }
}
</style>