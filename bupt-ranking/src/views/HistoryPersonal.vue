<script setup lang="ts">
import { computed } from 'vue'
import historyData from '@/data/history_data.json'

interface HistoryRecord {
  name: string
  gold: number
  silver: number
  bronze: number
  best: string
}

interface RankedRecord extends HistoryRecord {
  rank: number
}

const records = computed(() => {
  const data = historyData as HistoryRecord[]
  const sorted = [...data].sort((a, b) => {
    if (b.gold !== a.gold) return b.gold - a.gold
    if (b.silver !== a.silver) return b.silver - a.silver
    return b.bronze - a.bronze
  })

  const ranked: RankedRecord[] = []
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
  <div class="history-personal">
    <div class="table-wrapper">
      <table class="history-table">
        <thead>
          <tr>
            <th class="col-rank">排名</th>
            <th class="col-name">姓名</th>
            <th class="col-medal">🥇 金牌</th>
            <th class="col-medal">🥈 银牌</th>
            <th class="col-medal">🥉 铜牌</th>
            <th class="col-total">总计</th>
            <th class="col-best">最佳成绩</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.name">
            <td class="col-rank" :class="getRankClass(record.rank)">{{ getRankDisplay(record.rank) }}</td>
            <td class="col-name">{{ record.name }}</td>
            <td class="col-medal" :class="getMedalClass(record.gold)">{{ record.gold }}</td>
            <td class="col-medal" :class="getMedalClass(record.silver)">{{ record.silver }}</td>
            <td class="col-medal" :class="getMedalClass(record.bronze)">{{ record.bronze }}</td>
            <td class="col-total">{{ record.gold + record.silver + record.bronze }}</td>
            <td class="col-best">{{ record.best || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.history-personal {
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

.history-table thead th.col-name,
.history-table thead th.col-best {
  text-align: left;
}

.history-table tbody td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  text-align: center;
  vertical-align: middle;
}

.history-table tbody td.col-name,
.history-table tbody td.col-best {
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

.col-name {
  min-width: 80px;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 16px;
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

.col-best {
  min-width: 200px;
  color: var(--text-secondary);
  font-size: 15px;
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

  .col-best {
    display: none;
  }
}
</style>