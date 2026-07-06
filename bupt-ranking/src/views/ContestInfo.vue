<script setup lang="ts">
import icpcLogo from '@/assets/ICPC_logo.png'
import ccpcLogo from '@/assets/CCPC_logo.png'

const contests = [
  { name: 'ICPC 网络赛 第1场', date: '2026-09-06', weekday: '周日', platform: '' },
  { name: 'ICPC 网络赛 第2场', date: '2026-09-12', weekday: '周六', platform: '' },
  { name: 'CCPC 网络赛', date: '', weekday: '', platform: '' },
]

function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  const parts = dateStr.split('-')
  return `${parseInt(parts[1])}月${parseInt(parts[2])}日`
}
</script>

<template>
  <div class="contest-info">
    <div class="page-header">
      <h2 class="page-title">赛站信息</h2>
      <p class="page-desc">2026~2027赛季 ICPC / CCPC 各赛站日程安排</p>
    </div>

    <div class="section">
      <div class="section-header">
        <span class="section-icon">🌐</span>
        <h3 class="section-title">网络赛</h3>
      </div>
      <div class="table-wrapper">
        <table class="contest-table">
          <thead>
            <tr>
              <th class="col-index">序号</th>
              <th class="col-name">比赛名称</th>
              <th class="col-date">日期</th>
              <th class="col-platform">平台</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in contests" :key="item.name">
              <td class="col-index">{{ i + 1 }}</td>
              <td class="col-name">
                <span class="contest-name">{{ item.name }}</span>
              </td>
              <td class="col-date">
                <template v-if="item.date">
                  <span class="date-text">{{ formatDate(item.date) }}</span>
                  <span
                    class="weekday-badge"
                    :class="item.weekday === '周日' ? 'weekday-sun' : 'weekday-sat'"
                  >{{ item.weekday }}</span>
                </template>
                <span v-else class="date-text date-empty">-</span>
              </td>
              <td class="col-platform">
                <span class="platform-text">{{ item.platform || '-' }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <img :src="icpcLogo" class="section-logo" alt="ICPC">
        <h3 class="section-title">ICPC</h3>
      </div>
      <div class="placeholder-box">
        <p class="placeholder-text">待公布</p>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <img :src="ccpcLogo" class="section-logo" alt="CCPC">
        <h3 class="section-title">CCPC</h3>
      </div>
      <div class="placeholder-box">
        <p class="placeholder-text">待公布</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.contest-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--primary);
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 6px;
}

.page-desc {
  font-size: 14px;
  color: var(--text-secondary);
}

.section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 24px;
  background: var(--primary-bg);
  border-bottom: 1px solid var(--border);
}

.section-logo {
  height: 28px;
  width: auto;
  flex-shrink: 0;
}

.section-title {
  font-size: 19px;
  font-weight: 700;
  color: var(--primary-dark);
}

.table-wrapper {
  overflow: hidden;
}

.contest-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.contest-table thead th {
  background: #f8fafc;
  color: var(--text-secondary);
  font-weight: 600;
  padding: 12px 20px;
  text-align: left;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
  font-size: 13px;
}

.contest-table tbody td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  vertical-align: middle;
}

.contest-table tbody tr:last-child td {
  border-bottom: none;
}

.contest-table tbody tr:hover {
  background: var(--primary-bg);
}

.contest-table tbody tr:last-child {
  background: #fafafa;
}

.contest-table tbody tr:last-child:hover {
  background: #f5f5f5;
}

.col-index {
  width: 60px;
  color: var(--text-muted);
  text-align: center;
  font-weight: 500;
}

.col-name {
  min-width: 200px;
}

.contest-name {
  font-weight: 600;
  color: var(--text-primary);
}

.contest-table tbody tr:last-child .contest-name {
  color: var(--text-muted);
  font-style: italic;
}

.col-platform {
  min-width: 120px;
}

.platform-text {
  color: var(--text-muted);
  font-size: 13px;
}

.col-date {
  min-width: 180px;
}

.date-text {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 15px;
  margin-right: 10px;
}

.date-empty {
  color: var(--text-muted);
}

.weekday-badge {
  display: inline-block;
  padding: 3px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 10px;
  vertical-align: middle;
}

.weekday-sun {
  background: #fff7ed;
  color: #ea580c;
}

.weekday-sat {
  background: #fdf2f8;
  color: #db2777;
}

.placeholder-box {
  padding: 40px 24px;
  text-align: center;
}

.placeholder-text {
  font-size: 15px;
  color: var(--text-muted);
}

@media (max-width: 600px) {
  .section-header {
    padding: 12px 16px;
  }

  .contest-table thead th,
  .contest-table tbody td {
    padding: 12px 12px;
  }

  .col-date {
    min-width: 100px;
  }

  .col-name {
    min-width: 140px;
  }

  .col-platform {
    min-width: 80px;
  }
}
</style>