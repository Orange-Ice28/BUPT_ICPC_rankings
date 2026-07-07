<script setup lang="ts">
import { ref } from 'vue'

const WEEK_DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

interface CalendarDay {
  date: number
  month: number
  type: 'none' | 'nowcoder' | 'hdu' | 'huawei' | 'rest' | 'start'
  label: string
}

const calendarWeeks = ref<CalendarDay[][]>([
  // 第1周: 7月13日 - 7月19日
  [
    { date: 13, month: 7, type: 'none', label: '' },
    { date: 14, month: 7, type: 'none', label: '' },
    { date: 15, month: 7, type: 'none', label: '' },
    { date: 16, month: 7, type: 'none', label: '' },
    { date: 17, month: 7, type: 'nowcoder', label: '牛客' },
    { date: 18, month: 7, type: 'none', label: '' },
    { date: 19, month: 7, type: 'huawei', label: '华为' },
  ],
  // 第2周: 7月20日 - 7月26日
  [
    { date: 20, month: 7, type: 'none', label: '' },
    { date: 21, month: 7, type: 'hdu', label: '杭电' },
    { date: 22, month: 7, type: 'nowcoder', label: '牛客' },
    { date: 23, month: 7, type: 'hdu', label: '杭电' },
    { date: 24, month: 7, type: 'nowcoder', label: '牛客' },
    { date: 25, month: 7, type: 'none', label: '' },
    { date: 26, month: 7, type: 'huawei', label: '华为' },
  ],
  // 第3周: 7月27日 - 8月2日
  [
    { date: 27, month: 7, type: 'none', label: '' },
    { date: 28, month: 7, type: 'hdu', label: '杭电' },
    { date: 29, month: 7, type: 'nowcoder', label: '牛客' },
    { date: 30, month: 7, type: 'hdu', label: '杭电' },
    { date: 31, month: 7, type: 'nowcoder', label: '牛客' },
    { date: 1, month: 8, type: 'none', label: '' },
    { date: 2, month: 8, type: 'huawei', label: '华为' },
  ],
  // 第4周: 8月3日 - 8月9日
  [
    { date: 3, month: 8, type: 'none', label: '' },
    { date: 4, month: 8, type: 'hdu', label: '杭电' },
    { date: 5, month: 8, type: 'nowcoder', label: '牛客' },
    { date: 6, month: 8, type: 'hdu', label: '杭电' },
    { date: 7, month: 8, type: 'nowcoder', label: '牛客' },
    { date: 8, month: 8, type: 'none', label: '' },
    { date: 9, month: 8, type: 'huawei', label: '华为' },
  ],
  // 第5周: 8月10日 - 8月16日
  [
    { date: 10, month: 8, type: 'none', label: '' },
    { date: 11, month: 8, type: 'hdu', label: '杭电' },
    { date: 12, month: 8, type: 'nowcoder', label: '牛客' },
    { date: 13, month: 8, type: 'hdu', label: '杭电' },
    { date: 14, month: 8, type: 'nowcoder', label: '牛客' },
    { date: 15, month: 8, type: 'none', label: '' },
    { date: 16, month: 8, type: 'none', label: '' },
  ],
  // 第6周: 8月17日 - 8月23日
  [
    { date: 17, month: 8, type: 'none', label: '' },
    { date: 18, month: 8, type: 'hdu', label: '杭电' },
    { date: 19, month: 8, type: 'nowcoder', label: '牛客' },
    { date: 20, month: 8, type: 'hdu', label: '杭电' },
    { date: 21, month: 8, type: 'rest', label: '' },
    { date: 22, month: 8, type: 'rest', label: '' },
    { date: 23, month: 8, type: 'rest', label: '' },
  ],
  // 第7周: 8月24日 - 8月30日
  [
    { date: 24, month: 8, type: 'rest', label: '' },
    { date: 25, month: 8, type: 'rest', label: '' },
    { date: 26, month: 8, type: 'rest', label: '' },
    { date: 27, month: 8, type: 'rest', label: '' },
    { date: 28, month: 8, type: 'rest', label: '' },
    { date: 29, month: 8, type: 'rest', label: '' },
    { date: 30, month: 8, type: 'start', label: '开学' },
  ],
])

function getDayClass(day: CalendarDay): string {
  switch (day.type) {
    case 'nowcoder':
      return 'day-nowcoder'
    case 'hdu':
      return 'day-hdu'
    case 'huawei':
      return 'day-huawei'
    case 'rest':
      return 'day-rest'
    case 'start':
      return 'day-start'
    default:
      return 'day-none'
  }
}
</script>

<template>
  <div class="summer-schedule">
    <div class="page-header">
      <h2 class="page-title">☀️ 暑期训练安排</h2>
      <p class="page-desc">2026年7月13日 — 8月20日 | 共6周训练计划</p>
    </div>

    <div class="calendar-container">
      <div class="calendar-card">
        <div class="calendar-header">
          <div v-for="day in WEEK_DAYS" :key="day" class="weekday-header">
            {{ day }}
          </div>
        </div>

        <div class="calendar-body">
          <div v-for="(week, wi) in calendarWeeks" :key="wi" class="calendar-week">
            <div
              v-for="(day, di) in week"
              :key="di"
              class="calendar-day"
              :class="getDayClass(day)"
            >
              <div class="day-date">
                <span class="day-month">{{ day.month }}月</span>
                <span class="day-number">{{ day.date }}</span>
              </div>
              <div v-if="day.label" class="day-label">
                {{ day.label }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="legend-section">
      <h3 class="legend-title">图例说明</h3>
      <div class="legend-grid">
        <div class="legend-item">
          <div class="legend-color legend-nowcoder"></div>
          <span>牛客训练赛</span>
        </div>
        <div class="legend-item">
          <div class="legend-color legend-hdu"></div>
          <span>杭电训练赛</span>
        </div>
        <div class="legend-item">
          <div class="legend-color legend-huawei"></div>
          <span>华为算子开发</span>
        </div>
        <div class="legend-item">
          <div class="legend-color legend-rest"></div>
          <span>休息/自由训练</span>
        </div>
        <div class="legend-item">
          <div class="legend-color legend-start"></div>
          <span>开学</span>
        </div>
      </div>
    </div>

    <div class="schedule-summary">
      <h3 class="summary-title">训练统计</h3>
      <div class="summary-grid">
        <div class="summary-card">
          <div class="summary-number">10</div>
          <div class="summary-label">牛客训练赛</div>
        </div>
        <div class="summary-card">
          <div class="summary-number">10</div>
          <div class="summary-label">杭电训练赛</div>
        </div>
        <div class="summary-card">
          <div class="summary-number">4</div>
          <div class="summary-label">华为算子开发</div>
        </div>
        <div class="summary-card">
          <div class="summary-number">20</div>
          <div class="summary-label">计入成绩场次</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.summer-schedule {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 8px;
}

.page-desc {
  font-size: 16px;
  color: var(--text-secondary);
}

.calendar-container {
  margin-bottom: 30px;
}

.calendar-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: var(--primary-dark);
  color: white;
}

.weekday-header {
  padding: 14px 8px;
  text-align: center;
  font-weight: 600;
  font-size: 15px;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.weekday-header:last-child {
  border-right: none;
}

.calendar-body {
  padding: 10px;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
  margin-bottom: 6px;
}

.calendar-week:last-child {
  margin-bottom: 0;
}

.calendar-day {
  aspect-ratio: 1;
  border-radius: var(--radius);
  padding: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.calendar-day:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.day-date {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.day-month {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}

.day-number {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
}

.day-label {
  font-size: 13px;
  font-weight: 600;
  text-align: center;
  padding: 4px 8px;
  border-radius: 4px;
  margin-top: 4px;
}

/* 牛客 - 绿色 */
.day-nowcoder {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.day-nowcoder .day-month {
  color: rgba(255, 255, 255, 0.8);
}

.day-nowcoder .day-label {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* 杭电 - 橙黄色 */
.day-hdu {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.day-hdu .day-month {
  color: rgba(255, 255, 255, 0.8);
}

.day-hdu .day-label {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* 华为 - 黄色 */
.day-huawei {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #1e293b;
}

.day-huawei .day-month {
  color: rgba(30, 41, 59, 0.6);
}

.day-huawei .day-label {
  background: rgba(30, 41, 59, 0.1);
  color: #1e293b;
}

/* 休息 - 浅蓝色 */
.day-rest {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  color: var(--text-secondary);
}

.day-rest .day-month {
  color: var(--text-muted);
}

/* 开学 - 棕色 */
.day-start {
  background: linear-gradient(135deg, #92400e 0%, #78350f 100%);
  color: white;
}

.day-start .day-month {
  color: rgba(255, 255, 255, 0.8);
}

.day-start .day-label {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 700;
}

/* 无安排 - 白色 */
.day-none {
  background: var(--gray-bg);
  color: var(--text-muted);
  border: 1px dashed var(--border);
}

.day-none .day-month {
  color: var(--text-muted);
}

/* 图例 */
.legend-section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}

.legend-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-dark);
  margin-bottom: 16px;
  text-align: center;
}

.legend-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.legend-color {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}

.legend-nowcoder {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.legend-hdu {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.legend-huawei {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.legend-rest {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
}

.legend-start {
  background: linear-gradient(135deg, #92400e 0%, #78350f 100%);
}

/* 统计 */
.schedule-summary {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.summary-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-dark);
  margin-bottom: 16px;
  text-align: center;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.summary-card {
  text-align: center;
  padding: 20px;
  background: var(--primary-bg);
  border-radius: var(--radius);
  transition: transform 0.2s;
}

.summary-card:hover {
  transform: translateY(-2px);
}

.summary-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
  margin-bottom: 8px;
}

.summary-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 768px) {
  .summer-schedule {
    padding: 10px;
  }

  .page-title {
    font-size: 24px;
  }

  .calendar-day {
    aspect-ratio: 1;
    padding: 4px;
  }

  .day-month {
    font-size: 9px;
  }

  .day-number {
    font-size: 16px;
  }

  .day-label {
    font-size: 10px;
    padding: 2px 4px;
  }

  .weekday-header {
    padding: 10px 4px;
    font-size: 12px;
  }

  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .legend-grid {
    gap: 12px;
  }
}
</style>