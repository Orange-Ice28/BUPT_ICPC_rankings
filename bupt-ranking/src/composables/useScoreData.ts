import { ref } from 'vue'
import type { ScoreData } from '@/types'
import rawData from '@/data/score_data.json'
import summerRawData from '@/data/summer_score_data.json'

const scoreData = rawData as ScoreData
const summerScoreData = summerRawData as any

const data = ref<ScoreData | null>(null)
const summerData = ref<any>(null)
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

  async function fetchSummerData() {
    if (summerData.value) return summerData.value
    loading.value = true
    error.value = null
    try {
      summerData.value = summerScoreData
      return summerData.value
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  return { data, summerData, loading, error, fetchData, fetchSummerData }
}