<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HistoryPersonal from './HistoryPersonal.vue'
import HistoryTeam from './HistoryTeam.vue'

const route = useRoute()
const router = useRouter()

const activeTab = ref<'personal' | 'team'>('personal')

watch(
  () => route.name,
  (name) => {
    if (name === 'history-team') {
      activeTab.value = 'team'
    } else {
      activeTab.value = 'personal'
    }
  },
  { immediate: true },
)

function switchTab(tab: 'personal' | 'team') {
  activeTab.value = tab
  router.push({ name: tab === 'personal' ? 'history' : 'history-team' })
}
</script>

<template>
  <div class="history">
    <div class="page-header">
      <h2 class="page-title">历史战绩</h2>
      <div class="tab-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'personal' }"
          @click="switchTab('personal')"
        >
          个人战绩
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'team' }"
          @click="switchTab('team')"
        >
          团队战绩
        </button>
      </div>
    </div>

    <HistoryPersonal v-if="activeTab === 'personal'" />
    <HistoryTeam v-else />
  </div>
</template>

<style scoped>
.history {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  color: var(--primary);
  background: var(--primary-bg);
  font-weight: 600;
}

@media (max-width: 768px) {
  .page-header {
    padding: 16px;
  }

  .page-title {
    font-size: 18px;
  }
}
</style>