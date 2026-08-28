<script setup lang="ts">
import { ref, inject } from 'vue'
import icpcLogo from '@/assets/ICPC_logo.png'
import ccpcLogo from '@/assets/CCPC_logo.png'
import ccspLogo from '@/assets/CCSP_logo.png'
import caccLogo from '@/assets/CACC_logo.png'

const contests = inject<any[]>('contests', [])
const icpcContests = inject<any[]>('icpcContests', [])
const ccpcContests = inject<any[]>('ccpcContests', [])
const ccspContests = inject<any[]>('ccspContests', [])
const caccContests = inject<any[]>('caccContests', [])
const formatDate = inject<(dateStr: string) => string>('formatDate', () => '-')
const formatContestDate = inject<(dateStr: string) => string>('formatContestDate', () => '-')

const showCCPCSubtables = ref(false)

function toggleCCPCSubtables() {
  showCCPCSubtables.value = !showCCPCSubtables.value
}
</script>

<template>
  <div class="contest-table-view">
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
              <th class="col-problem-setter">命题学校</th>
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
              <td class="col-problem-setter">
                <span class="host-text">{{ item.problemSetter || '-' }}</span>
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
        <h3 class="section-title">ICPC 国际大学生程序设计竞赛</h3>
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
              <th class="col-teams">赛站规模</th>
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
      <div class="section-header ccpc-header" @click="toggleCCPCSubtables" title="点击展开/收起 CCSP 和 CACC 赛站信息">
        <img :src="ccpcLogo" class="section-logo ccpc-logo-clickable" alt="CCPC">
        <h3 class="section-title">CCPC 中国大学生程序设计竞赛</h3>
        <span class="expand-arrow" :class="{ expanded: showCCPCSubtables }">▶</span>
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
              <th class="col-teams">赛站规模</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in ccpcContests" :key="item.station">
              <td class="col-index">{{ i + 1 }}</td>
              <td class="col-station">
                <span class="contest-name">{{ item.station }}</span>
              </td>
              <td class="col-date">
                <span class="date-text">{{ item.date ? formatContestDate(item.date) : '-' }}</span>
              </td>
              <td class="col-host">
                <span class="host-text">{{ item.host || '-' }}</span>
              </td>
              <td class="col-problem-setter">
                <span class="problem-setter-text">{{ item.problemSetter || '-' }}</span>
              </td>
              <td class="col-teams">
                <span class="teams-text">{{ item.expectedTeams || '-' }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Transition name="section-fade">
      <div v-if="showCCPCSubtables" class="section">
        <div class="section-header">
          <img :src="ccspLogo" class="section-logo" alt="CCSP">
          <h3 class="section-title">CCSP  大学生计算机系统与程序设计竞赛</h3>
        </div>
        <div class="table-wrapper">
          <table class="contest-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-station">赛站</th>
                <th class="col-date">办赛日期</th>
                <th class="col-host">承办方</th>
                <th class="col-teams">赛站规模</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in ccspContests" :key="i">
                <td class="col-index">{{ i + 1 }}</td>
                <td class="col-station">
                  <span class="contest-name">{{ item.station || '-' }}</span>
                </td>
                <td class="col-date">
                  <span class="date-text">{{ item.date ? formatContestDate(item.date) : '-' }}</span>
                </td>
                <td class="col-host">
                  <span class="host-text">{{ item.host || '-' }}</span>
                </td>
                <td class="col-teams">
                  <span class="teams-text">{{ item.expectedTeams || '-' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Transition>

    <Transition name="section-fade">
      <div v-if="showCCPCSubtables" class="section">
        <div class="section-header">
          <img :src="caccLogo" class="section-logo" alt="CACC">
          <h3 class="section-title">CACC 算法能力大赛</h3>
        </div>
        <div class="table-wrapper">
          <table class="contest-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-station">赛站</th>
                <th class="col-date">办赛日期</th>
                <th class="col-host">承办方</th>
                <th class="col-teams">赛站规模</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in caccContests" :key="i">
                <td class="col-index">{{ i + 1 }}</td>
                <td class="col-station">
                  <span class="contest-name">{{ item.station || '-' }}</span>
                </td>
                <td class="col-date">
                  <span class="date-text">{{ item.date ? formatContestDate(item.date) : '-' }}</span>
                </td>
                <td class="col-host">
                  <span class="host-text">{{ item.host || '-' }}</span>
                </td>
                <td class="col-teams">
                  <span class="teams-text">{{ item.expectedTeams || '-' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.contest-table-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
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

.section-icon {
  font-size: 20px;
  flex-shrink: 0;
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
  font-size: 14px;
}

.contest-table tbody td {
  padding: 10px 20px;
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
  font-size: 15px;
}

.col-platform {
  min-width: 120px;
}

.platform-text {
  color: var(--text-muted);
  font-size: 14px;
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
  font-size: 14px;
}

.col-teams {
  min-width: 120px;
  text-align: left;
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

.ccpc-header {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.ccpc-header:hover {
  background: #e8ecf1;
}

.ccpc-logo-clickable {
  transition: transform 0.2s;
}

.ccpc-header:hover .ccpc-logo-clickable {
  transform: scale(1.08);
}

.expand-arrow {
  margin-left: auto;
  font-size: 12px;
  color: var(--text-muted);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.expand-arrow.expanded {
  transform: rotate(90deg);
}

.section-fade-enter-active {
  transition: all 0.4s ease;
}

.section-fade-leave-active {
  transition: all 0.3s ease;
}

.section-fade-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}

.section-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
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