<script setup lang="ts">
import icpcLogo from '@/assets/ICPC_logo.png'
import ccpcLogo from '@/assets/CCPC_logo.png'

const contests = [
  { name: 'ICPC 网络赛 第1场', date: '2026-09-06', weekday: '周日', platform: '' },
  { name: 'ICPC 网络赛 第2场', date: '2026-09-12', weekday: '周六', platform: '' },
  { name: 'CCPC 网络赛', date: '', weekday: '', platform: '' },
]

const icpcContests = [
  { station: '西安', date: '2026.10.10-11', host: '西北工业大学', expectedTeams: 350, problemSetter: '' },
  { station: '沈阳', date: '2026.10.17-18', host: '东北大学', expectedTeams: 400, problemSetter: '' },
  { station: '成都', date: '2026.10.24-25', host: '电子科技大学', expectedTeams: 320, problemSetter: '' },
  { station: '武汉', date: '2026.10.31-11.01', host: '武汉大学', expectedTeams: 300, problemSetter: '' },
  { station: '南京', date: '2026.11.07-08', host: '南京航空航天大学', expectedTeams: 360, problemSetter: '' },
  { station: '南昌', date: '2026.11.28-29', host: '江西师范大学', expectedTeams: 360, problemSetter: '' },
  { station: '上海', date: '2026.12.06-07', host: '上海大学', expectedTeams: 360, problemSetter: '' },
  { station: '香港', date: '2027.01.09-10', host: '香港大学', expectedTeams: 120, problemSetter: '' },
  { station: '杭州（EC Final）', date: '2027.01.26-28', host: '杭州师范大学、浙江大学', expectedTeams: 300, problemSetter: '' },
]

function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  const parts = dateStr.split('-')
  return `${parseInt(parts[1])}月${parseInt(parts[2])}日`
}

function formatContestDate(dateStr: string): string {
  if (!dateStr) return '-'
  return dateStr
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
      <div class="table-wrapper">
        <table class="contest-table">
          <thead>
            <tr>
              <th class="col-index">序号</th>
              <th class="col-station">赛站</th>
              <th class="col-date">办赛日期</th>
              <th class="col-host">主办学校</th>
              <th class="col-problem-setter">命题学校</th>
              <th class="col-teams">预期队伍数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in icpcContests" :key="item.station">
              <td class="col-index">{{ i + 1 }}</td>
              <td class="col-station">
                <span class="contest-name">{{ item.station }}</span>
              </td>
              <td class="col-date">
                <span class="date-text">{{ formatContestDate(item.date) }}</span>
              </td>
              <td class="col-host">
                <span class="host-text">{{ item.host }}</span>
              </td>
              <td class="col-problem-setter">
                <span class="problem-setter-text">{{ item.problemSetter || '-' }}</span>
              </td>
              <td class="col-teams">
                <span class="teams-text">{{ item.expectedTeams }}</span>
              </td>
            </tr>
          </tbody>
        </table>
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

.col-platform {
  min-width: 120px;
}

.platform-text {
  color: var(--text-muted);
  font-size: 13px;
}

.col-station {
  min-width: 120px;
}

.col-host {
  min-width: 180px;
}

.host-text {
  color: var(--text-primary);
  font-weight: 500;
}

.col-problem-setter {
  min-width: 140px;
}

.problem-setter-text {
  color: var(--text-muted);
  font-size: 13px;
}

.col-teams {
  min-width: 120px;
  text-align: center;
}

.teams-text {
  color: var(--text-primary);
  font-weight: 500;
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