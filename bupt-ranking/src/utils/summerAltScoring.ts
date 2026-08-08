// 暑期训练备选评分规则的共享逻辑
// 用于 SummerTrainingScoresAlt.vue 和 OverallScoreAlt.vue

// 暑期训练共20场（牛客10场 + 杭电10场），索引 0-19
export const CONTEST_LABELS = [
  '牛客1', '牛客2', '牛客3', '牛客4', '牛客5',
  '牛客6', '牛客7', '牛客8', '牛客9', '牛客10',
  '杭电1', '杭电2', '杭电3', '杭电4', '杭电5',
  '杭电6', '杭电7', '杭电8', '杭电9', '杭电10',
]

// 违规记录：队伍名 → 违规场次索引列表
// 索引 2=牛客3, 3=牛客4, 12=杭电3, 13=杭电4
export const VIOLATION_MAP: Record<string, number[]> = {
  '三只企鹅': [2, 3, 12, 13],
}

export interface TeamWithRank {
  name_cn: string
  members: { name: string; total_score: number }[]
  team_total: number
  rank: number
  contests: any[]
  imputedScore: number | null // 因公出差场次的估算分
}

/**
 * 对每个队伍重新计算：因公出差场次用"其余正常场次最高5场平均分"估算
 * 其余规则与原页面完全一致：取 ceil(有效场次 × 80%) 场最好成绩
 */
export function recalcTeam(team: any): TeamWithRank {
  const contests = team.contests || []

  // Step 0: 处理违规场次 — 强制 0 分，不视为因公出差
  const violations = VIOLATION_MAP[team.name_cn] || []
  const preprocessed = contests.map((c: any, i: number) => {
    if (violations.includes(i)) {
      return { ...c, score: 0, excused: false, _violation: true }
    }
    return { ...c }
  })

  // Step 1: 收集非 excused、非违规场次的有效分数（用于估算因公出差得分）
  const normalScores: number[] = []
  for (const c of preprocessed) {
    if (!c.excused && !c._violation) {
      const s = c.score ?? 0
      normalScores.push(s)
    }
  }

  // 取最高 5 场的平均分作为估算分
  normalScores.sort((a: number, b: number) => b - a)
  const top5 = normalScores.slice(0, 5)
  const imputedScore = top5.length > 0
    ? top5.reduce((sum, s) => sum + s, 0) / top5.length
    : 0

  // Step 2: 为 excused 场次填充估算分
  const filledContests = preprocessed.map((c: any) => {
    if (c.excused) {
      return { ...c, score: imputedScore, _imputed: true }
    }
    return { ...c, _imputed: false }
  })

  // Step 3: 按原规则计算有效场次和 best_n
  function isEffective(c: any): boolean {
    if (c.excused) {
      return c.score > 0 || c._imputed === true
    }
    if (c.absent) {
      return true
    }
    return (c.solved > 0 || c.score > 0)
  }

  const effectiveCount = filledContests.filter(isEffective).length

  let bestN: number
  if (effectiveCount === 0) {
    bestN = 0
  } else if (effectiveCount === 1) {
    bestN = 1
  } else {
    bestN = Math.max(1, Math.ceil(effectiveCount * 0.8))
  }

  // Step 4: 取 bestN 场最好成绩
  const effectivePairs: { score: number; origIndex: number }[] = []
  for (let i = 0; i < filledContests.length; i++) {
    if (isEffective(filledContests[i])) {
      effectivePairs.push({ score: filledContests[i].score ?? 0, origIndex: i })
    }
  }
  effectivePairs.sort((a, b) => b.score - a.score)

  const bestPairs = effectivePairs.slice(0, bestN)
  const isBestFlags = new Array(20).fill(false)
  let sum = 0
  for (const item of bestPairs) {
    isBestFlags[item.origIndex] = true
    sum += item.score
  }

  const finalContests = filledContests.map((c: any, i: number) => ({
    ...c,
    isBest: isBestFlags[i],
  }))

  const teamTotal = bestN > 0 ? Math.round((sum / bestN) * 100) / 100 : 0

  return {
    name_cn: team.name_cn,
    members: team.members,
    team_total: teamTotal,
    rank: 0,
    contests: finalContests,
    imputedScore: imputedScore,
  }
}
