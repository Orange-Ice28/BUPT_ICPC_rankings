export interface ContestDetail {
  solved: number
  rank: number
  score: number
}

export interface PersonalResult {
  team_id: string
  name: string
  total_score: number
  contests: ContestDetail[]
  best_indices: number[]
  in_team: boolean
  rank: number
}

export interface TeamMember {
  name: string
  total_score: number
}

export interface TeamResult {
  name_cn: string
  name_en: string
  members: TeamMember[]
  team_total: number
  rank: number
  contests?: ContestDetail[]
}

export interface ScoreData {
  baselines: number[]
  personal: PersonalResult[]
  teams: TeamResult[]
}