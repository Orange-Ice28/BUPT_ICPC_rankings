<script setup lang="ts">
</script>

<template>
  <div class="placeholder-page">
    <div class="placeholder-card">
      <div class="placeholder-icon">🌐</div>
      <h2 class="placeholder-title">网络赛</h2>
      <p class="placeholder-desc">网络赛成绩暂未公布，敬请期待</p>
    </div>
  </div>
</template>

<style scoped>
.placeholder-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.placeholder-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 60px 80px;
  text-align: center;
  box-shadow: var(--shadow-md);
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.placeholder-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 12px;
}

.placeholder-desc {
  font-size: 16px;
  color: var(--text-secondary);
}
</style>