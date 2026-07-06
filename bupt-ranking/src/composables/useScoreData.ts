import { ref } from 'vue'
import type { ScoreData } from '@/types'

const data = ref<ScoreData | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

export function useScoreData() {
  async function fetchData() {
    if (data.value) return data.value
    loading.value = true
    error.value = null
    try {
      const resp = await fetch(import.meta.env.BASE_URL + 'score_data.json')
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      data.value = await resp.json()
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