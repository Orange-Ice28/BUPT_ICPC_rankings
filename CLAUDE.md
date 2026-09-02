# CLAUDE.md

## 项目概述

北京邮电大学 ICPC 集训队实时排名网站，当前赛季：2026~2027 赛季。
线上地址：https://orange-ice28.github.io/BUPT_ICPC_rankings/

## 技术栈

- **前端**: Vue 3.5 + TypeScript 6.0 + Vite 8.0 + Vue Router 5.1
- **后端/数据处理**: Python 3，脚本位于 `scripts/` 目录
- **数据源**: Excel 文件（`data/*.xlsx`），处理后导出为 JSON 供前端消费
- **部署**: GitHub Pages（`bupt-ranking/dist/`）

## 项目结构

```
bupt_icpc_rankings/
├── bupt-ranking/          # Vue 3 前端项目
│   └── src/
│       ├── App.vue        # 根组件（导航栏 + RouterView）
│       ├── main.ts        # 入口
│       ├── types.ts       # TypeScript 类型定义
│       ├── router/index.ts # 路由配置
│       ├── views/         # 页面组件
│       ├── composables/   # 可复用逻辑（useScoreData）
│       ├── utils/         # 工具函数（summerAltScoring）
│       ├── data/          # JSON 数据文件（与 data/ 目录同步）
│       └── assets/        # 图片、CSS、Logo
├── data/                  # Excel 数据源 + JSON 输出
├── scripts/               # Python 数据处理脚本
└── website/               # （空目录）
```

## 路由表

| 路径 | 名称 | 组件 | 说明 |
|------|------|------|------|
| `/` | home | Home.vue | 首页 |
| `/spring` | spring | SpringTraining.vue | 春季训练成绩 |
| `/summer` | summer | SummerTraining.vue | 暑期训练（重定向到 /summer/schedule） |
| `/summer/schedule` | summer-schedule | SummerTrainingSchedule.vue | 暑期训练安排 |
| `/summer/scores` | summer-scores | SummerTrainingScoresAlt.vue | 暑期训练成绩（**默认规则**） |
| `/summer/scores-alt` | summer-scores-alt | SummerTrainingScores.vue | 暑期训练成绩（**备选方案**） |
| `/online` | online | OnlineContest.vue | 网络赛（占位） |
| `/overall` | overall | OverallScoreAlt.vue | 总成绩（**默认规则**） |
| `/overall-alt` | overall-alt | OverallScore.vue | 总成绩（**备选方案**） |
| `/contests` | contests | ContestInfo.vue | 赛站信息（重定向到 calendar） |
| `/contests/calendar` | contest-calendar | ContestCalendar.vue | 赛季日历 |
| `/contests/table` | contest-table | ContestTable.vue | 赛站详细信息 |
| `/history` | history | History.vue | 历史战绩-个人 |
| `/history-team` | history-team | History.vue | 历史战绩-团队 |

## 评分规则

### 总成绩公式
```
总成绩 = 春季训练 × 10% + 暑期训练 × 60% + 网络赛 × 30%
```

### 春季训练（HDU 平台，10 场个人赛）
- 得分 = 过题数 / baseline × (801 − 排名) / 800 × 100
- 取最好 70% 场次：team编号 ≤ 1791 取 7 场，> 1791 取 5 场
- 队伍总成绩 = 队员个人总成绩的平均值

### 暑期训练（牛客 10 场 + 杭电 10 场，共 20 场，团队赛）
- 牛客：过题数 / baseline × (751 − 排名) / 750 × 100
- 杭电：过题数 / baseline × (501 − 排名) / 500 × 100
- 取最好 80% 场次（16 场）的平均值
- 因公出差：用其余正常场次最高 5 场平均分估算，或减少计入场次

### 两种评分规则的区别
- **默认规则** (SummerTrainingScoresAlt / OverallScoreAlt)：使用 `recalcTeam()` 处理因公出差估算分、违规作废等逻辑
- **备选方案** (SummerTrainingScores / OverallScore)：使用原始数据，因公出差场次不计入有效场次，减少 best_n

## 数据流

1. Excel 数据源（`data/*.xlsx`）→ Python 脚本处理 → 生成 `data/score_data.json` 和 `data/summer_score_data.json`
2. JSON 文件需同步到 `bupt-ranking/src/data/` 和 `bupt-ranking/public/`
3. 前端 `useScoreData` composable 直接 import JSON 文件作为静态数据

## 关键 Python 脚本

- **`scripts/update_summer.py`** — 更新暑期训练成绩。用法：`python scripts/update_summer.py nc 3` 或 `python scripts/update_summer.py hdu 1`
- **`scripts/calc_score.py`** — 计算春季训练成绩
- **`scripts/export_json.py`** — 导出春季训练数据为 JSON
- **`scripts/recalc_nc_formula.py`** — 一次性脚本，将牛客公式从 (601−rank)/600 更新为 (751−rank)/750

## 重要注意事项

- 前端导航栏中"暑期训练"和"总成绩"的切换按钮（🌸/☀️ 图标点击）已被注释掉禁用，不再支持用户在前端切换评分规则
- 路由命名有历史遗留：`/summer/scores` 指向 SummerTrainingScoresAlt（默认规则），`/summer/scores-alt` 指向 SummerTrainingScores（备选方案）。同理 `/overall` 指向 OverallScoreAlt（默认规则），`/overall-alt` 指向 OverallScore（备选方案）
- 导航栏 `isActive` 对 `/summer` 和 `/history` 做了前缀匹配
- 前端构建使用 `./` 作为 base（相对路径），适配 GitHub Pages
- Vue Router 使用 hash 模式（`createWebHashHistory`）
- 数据更新后需要运行 `npm run build` 并部署到 GitHub Pages