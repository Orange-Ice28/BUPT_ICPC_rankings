"""临时脚本：将牛客得分公式更新为 (751 - rank) / 750"""
import json
import math
import os
import shutil

SRC = r'd:\Software\bupt_icpc_rankings\bupt-ranking\src\data\summer_score_data.json'
DST_PUBLIC = r'd:\Software\bupt_icpc_rankings\bupt-ranking\public\summer_score_data.json'

RANK_OFFSET_NC = 751  # 牛客 (601 → 751)

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 重新计算牛客 0-9 场得分
for team in data['teams']:
    for i in range(10):
        if i >= len(team['contests']):
            continue
        c = team['contests'][i]
        if c.get('excused', False) or c.get('absent', False):
            continue
        solved = c.get('solved', 0) or 0
        rank = c.get('rank', 0) or 0
        baseline = data['baselines'][i] if i < len(data['baselines']) else 9
        if baseline == 0:
            score = 0.0
        else:
            score = (solved / baseline) * (RANK_OFFSET_NC - rank) / (RANK_OFFSET_NC - 1) * 100
            if score < 0 or score > 100:
                score = 0.0
        c['score'] = round(score, 2)

# 重新计算队伍总成绩
def is_effective(c):
    if c.get('excused', False):
        return False
    if c.get('absent', False):
        return True
    return c['solved'] > 0 or c['score'] > 0

for team in data['teams']:
    for c in team['contests']:
        c['isBest'] = False
    n = sum(1 for c in team['contests'] if is_effective(c))
    excused = sum(1 for c in team['contests'] if c.get('excused', False))
    if n == 0:
        team['team_total'] = 0.0
    elif n == 1:
        for c in team['contests']:
            if is_effective(c):
                team['team_total'] = round(c['score'], 2)
                c['isBest'] = True
                break
    else:
        held = sum(1 for b in data['baselines'] if b > 0)
        best_n = max(1, math.ceil(held * 0.8) - excused) if excused > 0 else max(1, math.ceil(n * 0.8))
        pairs = [(j, c['score']) for j, c in enumerate(team['contests']) if is_effective(c)]
        pairs.sort(key=lambda x: x[1], reverse=True)
        for j in {p[0] for p in pairs[:best_n]}:
            team['contests'][j]['isBest'] = True
        team['team_total'] = round(sum(p[1] for p in pairs[:best_n]) / best_n, 2)

data['teams'].sort(key=lambda x: x['team_total'], reverse=True)
for i, team in enumerate(data['teams']):
    team['rank'] = i + 1

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(DST_PUBLIC), exist_ok=True)
shutil.copy(SRC, DST_PUBLIC)

print('Updated!')
for t in data['teams'][:10]:
    print(f'  {t["rank"]:>2}. {t["name_cn"]:<20s}  {t["team_total"]:>6.2f}')