<script setup lang="ts">
import { ref, computed, inject } from 'vue'

interface ContestEvent {
  label: string
  type: 'icpc' | 'ccpc' | 'online'
  startDate: Date
  endDate: Date
}

interface CalendarDay {
  date: Date
  day: number
  month: number
  isCurrentMonth: boolean
  contests: ContestEvent[]
}

const contests = inject<any[]>('contests', [])
const icpcContests = inject<any[]>('icpcContests', [])
const ccpcContests = inject<any[]>('ccpcContests', [])
const parseContestDate = inject<(dateStr: string) => { start: Date; end: Date } | null>('parseContestDate', () => null)

const WEEK_DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

const currentYear = ref(2026)
const currentMonth = ref(9)

const allEvents = computed<ContestEvent[]>(() => {
  const events: ContestEvent[] = []

  for (const c of contests) {
    if (c.date) {
      const parts = c.date.split('-')
      const y = parseInt(parts[0]!), m = parseInt(parts[1]!), d = parseInt(parts[2]!)
      const start = new Date(y, m - 1, d)
      events.push({ label: c.name, type: 'online', startDate: start, endDate: start })
    }
  }

  for (const c of icpcContests) {
    const parsed = parseContestDate(c.date)
    if (parsed) {
      events.push({ label: `ICPC ${c.station}`, type: 'icpc', startDate: parsed.start, endDate: parsed.end })
    }
  }

  for (const c of ccpcContests) {
    const parsed = parseContestDate(c.date)
    if (parsed) {
      events.push({ label: `CCPC ${c.station}`, type: 'ccpc', startDate: parsed.start, endDate: parsed.end })
    }
  }

  return events
})

const monthCalendar = computed<CalendarDay[][]>(() => {
  const year = currentYear.value
  const month = currentMonth.value

  const firstDay = new Date(year, month - 1, 1)
  const lastDay = new Date(year, month, 0)

  const startDay = new Date(firstDay)
  const dow = startDay.getDay()
  const offset = dow === 0 ? -6 : 1 - dow
  startDay.setDate(startDay.getDate() + offset)

  const endDay = new Date(lastDay)
  const endDow = endDay.getDay()
  const endOffset = endDow === 0 ? 0 : 7 - endDow
  endDay.setDate(endDay.getDate() + endOffset)

  const weeks: CalendarDay[][] = []
  const cursor = new Date(startDay)

  while (cursor <= endDay) {
    const week: CalendarDay[] = []
    for (let i = 0; i < 7; i++) {
      const d = new Date(cursor)
      const dayContests = allEvents.value.filter(e => d >= e.startDate && d <= e.endDate)
      week.push({
        date: new Date(d),
        day: d.getDate(),
        month: d.getMonth() + 1,
        isCurrentMonth: d.getMonth() + 1 === month,
        contests: dayContests,
      })
      cursor.setDate(cursor.getDate() + 1)
    }
    weeks.push(week)
  }

  return weeks
})

function prevMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function goToToday() {
  const now = new Date()
  currentYear.value = now.getFullYear()
  currentMonth.value = now.getMonth() + 1
}

const monthLabel = computed(() => `${currentYear.value}年${currentMonth.value}月`)

const monthHasEvents = computed(() =>
  monthCalendar.value.some(week => week.some(day => day.contests.length > 0))
)
</script>

<template>
  <div class="contest-calendar">
    <div class="section">
      <div class="section-header">
        <span class="section-icon">📅</span>
        <h3 class="section-title">赛季日历</h3>
        <span class="section-subtitle">ICPC / CCPC 正式赛 & 网络赛</span>
      </div>
      <div class="calendar-container">
        <div class="calendar-nav">
          <button class="nav-btn" @click="prevMonth" title="上个月">◀</button>
          <span class="nav-label">{{ monthLabel }}</span>
          <button class="nav-btn" @click="nextMonth" title="下个月">▶</button>
          <button class="nav-btn nav-today" @click="goToToday">今天</button>
        </div>
        <div class="calendar-card">
          <div class="calendar-header">
            <div v-for="day in WEEK_DAYS" :key="day" class="weekday-header">
              {{ day }}
            </div>
          </div>
          <div class="calendar-body">
            <div v-for="(week, wi) in monthCalendar" :key="wi" class="calendar-week">
              <div
                v-for="day in week"
                :key="day.date.toISOString()"
                class="calendar-day"
                :class="{
                  'is-current-month': day.isCurrentMonth,
                  'is-other-month': !day.isCurrentMonth,
                  'has-contest': day.contests.length > 0,
                  'has-icpc': day.contests.some(c => c.type === 'icpc'),
                  'has-ccpc': day.contests.some(c => c.type === 'ccpc'),
                  'has-online': day.contests.some(c => c.type === 'online'),
                  'has-both': day.contests.filter(c => c.type === 'icpc' || c.type === 'ccpc').length >= 2
                    || (day.contests.some(c => c.type === 'icpc') && day.contests.some(c => c.type === 'ccpc')),
                }"
              >
                <div class="day-date">
                  <span class="day-number">{{ day.day }}</span>
                </div>
                <div v-if="day.contests.length > 0" class="day-contests">
                  <div
                    v-for="c in day.contests"
                    :key="c.type + c.label"
                    class="contest-tag"
                    :class="{
                      'tag-icpc': c.type === 'icpc',
                      'tag-ccpc': c.type === 'ccpc',
                      'tag-online': c.type === 'online',
                    }"
                  >
                    {{ c.label.length > 20 ? c.label.slice(0, 20) + '…' : c.label }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!monthHasEvents" class="calendar-empty-hint">
          本月暂无比赛安排
        </div>
      </div>
      <div class="calendar-legend">
        <div class="legend-item">
          <div class="legend-swatch legend-icpc-swatch"></div>
          <span>ICPC 赛站</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch legend-ccpc-swatch"></div>
          <span>CCPC 赛站</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch legend-online-swatch"></div>
          <span>网络赛</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch legend-both-swatch"></div>
          <span>同日多项比赛</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.contest-calendar {
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

.section-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.section-title {
  font-size: 19px;
  font-weight: 700;
  color: var(--primary-dark);
}

.section-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin-left: 4px;
}

.calendar-container {
  padding: 16px;
}

.calendar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.nav-btn {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 6px 14px;
  font-size: 14px;
  cursor: pointer;
  color: var(--text-primary);
  transition: background 0.15s, border-color 0.15s;
}

.nav-btn:hover {
  background: var(--primary-bg);
  border-color: var(--primary);
}

.nav-today {
  font-size: 12px;
  padding: 4px 10px;
}

.nav-label {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-dark);
  min-width: 110px;
  text-align: center;
}

.calendar-card {
  overflow-x: auto;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: var(--primary-dark);
  color: white;
  border-radius: var(--radius) var(--radius) 0 0;
}

.weekday-header {
  padding: 12px 8px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.weekday-header:last-child {
  border-right: none;
}

.calendar-body {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  border-radius: var(--radius);
  padding: 8px 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 80px;
  transition: transform 0.15s, box-shadow 0.15s;
  border: 1px solid var(--border-light);
  background: var(--bg-card);
  overflow: hidden;
}

.calendar-day:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.calendar-day.is-other-month {
  opacity: 0.35;
}

.calendar-day.is-other-month .day-number {
  color: var(--text-muted);
}

.calendar-day.has-icpc:not(.has-both):not(.has-online) {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-color: #93c5fd;
}

.calendar-day.has-ccpc:not(.has-both):not(.has-online) {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  border-color: #f9a8d4;
}

.calendar-day.has-online:not(.has-icpc):not(.has-ccpc) {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-color: #6ee7b7;
}

.calendar-day.has-both,
.calendar-day.has-icpc.has-ccpc,
.calendar-day.has-icpc.has-online,
.calendar-day.has-ccpc.has-online {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border-color: #fdba74;
}

.calendar-day .day-date {
  display: flex;
  justify-content: center;
}

.calendar-day .day-number {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.calendar-day.is-other-month .day-number {
  font-weight: 500;
}

.day-contests {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.contest-tag {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 3px;
  text-align: center;
  line-height: 1.4;
  white-space: nowrap;
}

.tag-icpc {
  background: #2563eb;
  color: white;
}

.tag-ccpc {
  background: #db2777;
  color: white;
}

.tag-online {
  background: #059669;
  color: white;
}

.calendar-empty-hint {
  text-align: center;
  padding: 12px;
  font-size: 13px;
  color: var(--text-muted);
}

.calendar-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 12px 24px 16px;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.legend-swatch {
  width: 22px;
  height: 22px;
  border-radius: 4px;
}

.legend-icpc-swatch {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 2px solid #93c5fd;
}

.legend-ccpc-swatch {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  border: 2px solid #f9a8d4;
}

.legend-online-swatch {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border: 2px solid #6ee7b7;
}

.legend-both-swatch {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border: 2px solid #fdba74;
}

@media (max-width: 768px) {
  .calendar-day {
    padding: 4px 3px;
    min-height: 60px;
  }

  .calendar-day .day-number {
    font-size: 14px;
  }

  .contest-tag {
    font-size: 9px;
    padding: 1px 3px;
  }

  .weekday-header {
    padding: 8px 2px;
    font-size: 11px;
  }

  .nav-label {
    font-size: 15px;
    min-width: 90px;
  }
}
</style>