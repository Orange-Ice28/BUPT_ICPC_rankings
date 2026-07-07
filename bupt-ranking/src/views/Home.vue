<script setup lang="ts">
import { ref } from 'vue'
import volunteerPhoto from '@/assets/志愿者合照.jpg'
import wf1 from '@/assets/WF1.jpg'
import wf2 from '@/assets/WF2.jpg'
import wf3 from '@/assets/WF3.jpg'
import wf4 from '@/assets/WF4.jpg'

const wfPhotos = [wf1, wf2, wf3, wf4]
const isPaused = ref(false)

function pauseScroll() {
  isPaused.value = true
}

function resumeScroll() {
  isPaused.value = false
}

const extendedPhotos = [...wfPhotos, ...wfPhotos, ...wfPhotos, ...wfPhotos]
</script>

<template>
  <div class="home">
    <div class="home-background" :style="{ backgroundImage: `url(${volunteerPhoto})` }"></div>
    <div class="home-content">
      <h2 class="page-title">北京邮电大学 ICPC 集训队</h2>
      <p class="page-desc">欢迎查看集训队排名系统</p>
    </div>
  </div>

  <div class="wf-section">
    <h3 class="section-title">2025年 49th ICPC World Finals 参赛风采</h3>
    <div class="photo-carousel" @mouseenter="pauseScroll" @mouseleave="resumeScroll">
      <div class="carousel-track" :style="{ animationPlayState: isPaused ? 'paused' : 'running' }">
        <div v-for="(photo, index) in extendedPhotos" :key="index" class="carousel-item">
          <img :src="photo" alt="World Finals 2025" class="carousel-photo">
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 600px;
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.home-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
}

.home-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.home-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: #fff;
  padding: 40px;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding-top: 160px;
}

.page-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
}

.page-desc {
  font-size: 24px;
  line-height: 1.8;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
}

.wf-section {
  margin-top: 24px;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 16px;
  text-align: center;
}

.photo-carousel {
  width: 100%;
  overflow: hidden;
  border-radius: var(--radius);
}

.carousel-track {
  display: flex;
  gap: 16px;
  animation: scroll 30s linear infinite;
  width: fit-content;
}

.carousel-item {
  flex-shrink: 0;
}

.carousel-photo {
  height: 120px;
  width: auto;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  transition: transform 0.3s ease;
}

.carousel-photo:hover {
  transform: scale(1.05);
}

@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-25%);
  }
}

@media (max-width: 768px) {
  .home {
    min-height: 400px;
  }

  .home-content {
    min-height: 400px;
    padding: 24px;
  }

  .page-title {
    font-size: 32px;
  }

  .page-desc {
    font-size: 18px;
  }

  .carousel-photo {
    height: 80px;
  }

  .section-title {
    font-size: 18px;
  }
}
</style>