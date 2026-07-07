<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeTab = ref<'schedule' | 'scores'>('schedule')

watch(
  () => route.name,
  (name) => {
    if (name === 'summer-scores') {
      activeTab.value = 'scores'
    } else {
      activeTab.value = 'schedule'
    }
  },
  { immediate: true },
)

function switchTab(tab: 'schedule' | 'scores') {
  activeTab.value = tab
  router.push({ name: tab === 'schedule' ? 'summer-schedule' : 'summer-scores' })
}
</script>

<template>
  <div class="summer-training">
    <div class="page-header">
      <h2 class="page-title">☀️ 暑期训练</h2>
      <div class="tab-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'schedule' }"
          @click="switchTab('schedule')"
        >
          训练安排
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'scores' }"
          @click="switchTab('scores')"
        >
          训练成绩
        </button>
      </div>
    </div>

    <router-view />
  </div>
</template>

<style scoped>
.summer-training {
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