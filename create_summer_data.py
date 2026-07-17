import json
import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 读取 nowcoder_contest1.xlsx
wb = openpyxl.load_workbook('data/nowcoder_contest1.xlsx')
ws = wb.active

# 读取队伍信息
with open('data/score_data.json', 'r', encoding='utf-8') as f:
    score_data = json.load(f)

# 构建队伍名称到队伍数据的映射
teams = score_data['teams']
team_name_to_data = {team['name_cn']: team for team in teams}

# 读取牛客第一场成绩
nowcoder_data = []
for row in ws.iter_rows(min_row=2, values_only=True):
    rank, name, school, solved, penalty, baseline, score = row
    nowcoder_data.append({
        "rank": int(rank) if rank else 0,
        "name": name,
        "school": school,
        "solved": int(solved) if solved else 0,
        "penalty": penalty,
        "baseline": baseline,
        "score": score if score else 0.0
    })

print(f"读取到 {len(nowcoder_data)} 条牛客第一场成绩")

# 创建暑期训练数据结构
summer_data = {
    "baselines": [0] * 20,  # 20场比赛的 baseline
    "teams": []
}

# 设置牛客第一场的 baseline
summer_data["baselines"][0] = 9

# 为每个队伍创建暑期训练数据
for team in teams:
    team_name = team['name_cn']
    team_name_en = team.get('name_en', '')
    
    # 查找该队伍在牛客第一场的成绩（模糊匹配中文名和英文名）
    nowcoder_record = None
    for record in nowcoder_data:
        nc_name = record['name']
        # 匹配中文名
        if nc_name == team_name or team_name in nc_name or nc_name in team_name:
            nowcoder_record = record
            break
        # 匹配英文名（去除空格和特殊字符后比较）
        if team_name_en:
            nc_name_clean = nc_name.replace(' ', '').replace('://', '').replace('!', '').lower()
            en_name_clean = team_name_en.replace(' ', '').replace('://', '').replace('!', '').lower()
            if nc_name_clean == en_name_clean or en_name_clean in nc_name_clean or nc_name_clean in en_name_clean:
                nowcoder_record = record
                break
    
    # 创建队伍的暑期训练数据
    summer_team = {
        "name_cn": team['name_cn'],
        "name_en": team['name_en'],
        "members": team['members'],
        "team_total": 0.0,
        "rank": 0,
        "contests": [{"solved": 0, "rank": 0, "score": 0.0}] * 20
    }
    
    # 如果有牛客第一场成绩，更新 contests[0]
    if nowcoder_record:
        summer_team["contests"][0] = {
            "solved": nowcoder_record["solved"],
            "rank": nowcoder_record["rank"],
            "score": nowcoder_record["score"]
        }
        print(f"队伍 {team_name}: 过题={nowcoder_record['solved']}, 排名={nowcoder_record['rank']}, 得分={nowcoder_record['score']}")
    
    summer_data["teams"].append(summer_team)

# 计算队伍总成绩（动态计算有效场次数）
import math

for team in summer_data["teams"]:
    scores = [c["score"] for c in team["contests"]]
    # 计算有数据的场次数（得分 > 0 或 过题数 > 0）
    contests_with_data = sum(1 for c in team["contests"] if c["solved"] > 0 or c["score"] > 0)
    
    # 初始化所有 contests 的 isBest 为 False
    for contest in team["contests"]:
        contest["isBest"] = False
    
    if contests_with_data == 0:
        team["team_total"] = 0.0
    elif contests_with_data == 1:
        # 只有1场时直接计入
        for i, c in enumerate(team["contests"]):
            if c["solved"] > 0 or c["score"] > 0:
                team["team_total"] = round(c["score"], 2)
                c["isBest"] = True
                break
    else:
        # 有效场次数 = 有数据的场次 * 80% 向上取整
        best_n = math.ceil(contests_with_data * 0.8)
        # 获取有数据的场次索引和分数
        contest_pairs = [(i, c["score"]) for i, c in enumerate(team["contests"]) if c["solved"] > 0 or c["score"] > 0]
        # 按分数降序排序
        contest_pairs.sort(key=lambda x: x[1], reverse=True)
        # 取最好N场
        best_pairs = contest_pairs[:best_n]
        best_indices = set(p[0] for p in best_pairs)
        # 标记 best contests
        for i in best_indices:
            team["contests"][i]["isBest"] = True
        
        best_scores = [p[1] for p in best_pairs]
        team["team_total"] = round(sum(best_scores) / best_n, 2)

# 按队伍总成绩排序
summer_data["teams"].sort(key=lambda x: x["team_total"], reverse=True)
for i, team in enumerate(summer_data["teams"]):
    team["rank"] = i + 1

# 保存暑期训练数据
with open('data/summer_score_data.json', 'w', encoding='utf-8') as f:
    json.dump(summer_data, f, ensure_ascii=False, indent=2)

print(f"\n已创建 data/summer_score_data.json")
print(f"队伍数: {len(summer_data['teams'])}")
print(f"比赛场数: {len(summer_data['baselines'])}")

# 同时复制到前端
import shutil
shutil.copy('data/summer_score_data.json', 'bupt-ranking/src/data/summer_score_data.json')
shutil.copy('data/summer_score_data.json', 'bupt-ranking/public/summer_score_data.json')
print("已复制到前端目录")