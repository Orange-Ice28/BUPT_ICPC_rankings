<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import logo from '@/assets/ICPC_logo.png'

const route = useRoute()

const navItems = [
  { path: '/', label: '首页' },
  { path: '/spring', label: '春季训练' },
  { path: '/summer', label: '暑期训练' },
  { path: '/online', label: '网络赛' },
  { path: '/overall', label: '总成绩' },
  { path: '/contests', label: '赛站信息' },
  { path: '/history', label: '历史战绩' },
]

const currentPath = computed(() => route.path)

function isActive(path: string): boolean {
  if (path === '/history') {
    return currentPath.value === '/history' || currentPath.value === '/history-team'
  }
  return currentPath.value === path
}
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <div class="header-brand">
        <img :src="logo" class="logo-img" alt="ICPC logo">
        <h1 class="header-title">北京邮电大学 ICPC 集训队排名</h1>
      </div>
      <nav class="header-nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
  <main class="app-main">
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
  color: #fff;
  box-shadow: var(--shadow-lg);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-img {
  height: 40px;
  width: auto;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.header-nav {
  display: flex;
  gap: 4px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  padding: 8px 18px;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
}

.nav-link.active {
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.app-main {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 24px;
}

@media (max-width: 768px) {
  .header-inner {
    flex-direction: column;
    height: auto;
    padding: 12px 16px;
    gap: 8px;
  }

  .header-title {
    font-size: 16px;
  }

  .header-nav {
    width: 100%;
    justify-content: center;
  }

  .nav-link {
    padding: 6px 12px;
    font-size: 13px;
  }

  .app-main {
    padding: 12px;
  }
}
</style>