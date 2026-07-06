import { ref } from 'vue'
import type { ScoreData } from '@/types'
import rawData from '@/data/score_data.json'

const scoreData = rawData as ScoreData

const data = ref<ScoreData | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

export function useScoreData() {
  async function fetchData() {
    if (data.value) return data.value
    loading.value = true
    error.value = null
    try {
      data.value = scoreData
      return data.value
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}