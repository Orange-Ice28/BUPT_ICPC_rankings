<script setup lang="ts">
import { ref, provide, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const contests = [
  { name: 'ICPC 网络赛 第1场', date: '2026-09-06', weekday: '周日', platform: 'PTA', problemSetter: '北京大学' },
  { name: 'ICPC 网络赛 第2场', date: '2026-09-12', weekday: '周六', platform: 'PTA', problemSetter: '杭州师范大学、浙江大学' },
  { name: 'CCPC 网络赛', date: '2026-09-19', weekday: '周六', platform: '', problemSetter: '' },
]

const icpcContests = [
  { station: '西安', date: '2026.10.17-18', host: '西北工业大学', expectedTeams: 380, problemSetter: '' },
  { station: '成都', date: '2026.10.24-25', host: '电子科技大学', expectedTeams: 320, problemSetter: '' },
  { station: '武汉', date: '2026.10.31-11.01', host: '武汉大学', expectedTeams: 300, problemSetter: '' },
  { station: '南京', date: '2026.11.07-08', host: '南京航空航天大学', expectedTeams: 360, problemSetter: '' },
  { station: '沈阳', date: '2026.11.14-15', host: '东北大学', expectedTeams: 400, problemSetter: '' },
  { station: '上海', date: '2026.12.05-06', host: '上海大学', expectedTeams: '336（正式）+48（打星）', problemSetter: '' },
  { station: '南昌', date: '2026.12.19-20', host: '江西师范大学', expectedTeams: 360, problemSetter: '' },
  { station: '香港', date: '2027.01.09-10', host: '香港大学', expectedTeams: 120, problemSetter: '' },
  { station: '杭州（EC Final）', date: '2027.01.26-28', host: '杭州师范大学、浙江大学', expectedTeams: 300, problemSetter: '' },
]

const ccpcContests = [
  { station: '长春', date: '2026.10.17-18', host: '东北师范大学', expectedTeams: '300', problemSetter: '' },
  { station: '荆州', date: '2026.11.07-08', host: '长江大学', expectedTeams: '300', problemSetter: '' },
  { station: '乐山', date: '2026.11.14-15', host: '乐山师范学院', expectedTeams: '300', problemSetter: '' },
  { station: '厦门', date: '2026.11.21-22', host: '厦门大学', expectedTeams: '300', problemSetter: '' },
  { station: '总决赛', date: '', host: '', expectedTeams: '', problemSetter: '' },
]

const ccspContests = [
  { station: '成都', date: '2026.10.21-22', host: '', expectedTeams: '500' },
]

const caccContests = [
  { station: '北京（区域赛）', date: '2026年12月', host: '北京邮电大学', expectedTeams: '' },
  { station: '宁波（总决赛）', date: '2027年4月', host: '宁波海曙区委党校', expectedTeams: '500' },
]

function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  const parts = dateStr.split('-')
  return `${parseInt(parts[1]!)}月${parseInt(parts[2]!)}日`
}

function formatContestDate(dateStr: string): string {
  if (!dateStr) return '-'
  const match = dateStr.match(/^(\d{4})\.(\d{2})\.(\d{2})-(\d{2})\.(\d{2})$/)
  if (match) {
    const year = match[1]!
    const month = parseInt(match[2]!)
    const day1 = parseInt(match[3]!)
    const month2 = parseInt(match[4]!)
    const day2 = parseInt(match[5]!)
    if (month === month2) {
      return `${year}年${month}月${day1}日~${day2}日`
    } else {
      return `${year}年${month}月${day1}日~${month2}月${day2}日`
    }
  }
  const match2 = dateStr.match(/^(\d{4})\.(\d{2})\.(\d{2})-(\d{2})$/)
  if (match2) {
    const year = match2[1]!
    const month = parseInt(match2[2]!)
    const day1 = parseInt(match2[3]!)
    const day2 = parseInt(match2[4]!)
    return `${year}年${month}月${day1}日~${day2}日`
  }
  return dateStr
}

function parseContestDate(dateStr: string): { start: Date; end: Date } | null {
  if (!dateStr) return null
  const match = dateStr.match(/^(\d{4})\.(\d{2})\.(\d{2})-(\d{2})\.(\d{2})$/)
  if (match) {
    const year = parseInt(match[1]!)
    const month1 = parseInt(match[2]!)
    const day1 = parseInt(match[3]!)
    const month2 = parseInt(match[4]!)
    const day2 = parseInt(match[5]!)
    return {
      start: new Date(year, month1 - 1, day1),
      end: new Date(year, month2 - 1, day2),
    }
  }
  const match2 = dateStr.match(/^(\d{4})\.(\d{2})\.(\d{2})-(\d{2})$/)
  if (match2) {
    const year = parseInt(match2[1]!)
    const month = parseInt(match2[2]!)
    const day1 = parseInt(match2[3]!)
    const day2 = parseInt(match2[4]!)
    return {
      start: new Date(year, month - 1, day1),
      end: new Date(year, month - 1, day2),
    }
  }
  return null
}

// 共享数据通过 provide 传递给子组件
provide('contests', contests)
provide('icpcContests', icpcContests)
provide('ccpcContests', ccpcContests)
provide('ccspContests', ccspContests)
provide('caccContests', caccContests)
provide('formatDate', formatDate)
provide('formatContestDate', formatContestDate)
provide('parseContestDate', parseContestDate)

// Tab 切换
const activeTab = ref<'calendar' | 'table'>('calendar')

function switchTab(tab: 'calendar' | 'table') {
  activeTab.value = tab
  router.push({ name: tab === 'calendar' ? 'contest-calendar' : 'contest-table' })
}

// 根据路由同步 tab
watch(
  () => route.name,
  (name) => {
    if (name === 'contest-table') {
      activeTab.value = 'table'
    } else {
      activeTab.value = 'calendar'
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="contest-info">
    <div class="page-header">
      <h2 class="page-title">赛站信息</h2>
      <p class="page-desc">2026~2027赛季 ICPC / CCPC 各赛站日程安排</p>
      <div class="tab-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'calendar' }"
          @click="switchTab('calendar')"
        >
          赛季日历
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'table' }"
          @click="switchTab('table')"
        >
          详细信息
        </button>
      </div>
    </div>

    <router-view />
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
  margin-bottom: 16px;
}

.tab-bar {
  display: flex;
  gap: 4px;
  background: var(--bg);
  padding: 4px;
  border-radius: var(--radius);
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
</style>