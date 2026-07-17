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

# 读取 nowcoder_contest1.xlsx 中的队伍名称
nowcoder_names = []
for row in ws.iter_rows(min_row=2, values_only=True):
    rank, name, school, solved, penalty, baseline, score = row
    nowcoder_names.append(name)

print("Nowcoder 队伍名称:")
for name in nowcoder_names:
    print(f"  - {name}")

# 读取 score_data.json 中的队伍名称
score_team_names = [team['name_cn'] for team in score_data['teams']]
print(f"\nscore_data.json 队伍数量: {len(score_team_names)}")

# 查找匹配的队伍
matched = []
unmatched = []
for nc_name in nowcoder_names:
    found = False
    for st_name in score_team_names:
        if nc_name == st_name or nc_name in st_name or st_name in nc_name:
            matched.append((nc_name, st_name))
            found = True
            break
    if not found:
        unmatched.append(nc_name)

print(f"\n匹配的队伍 ({len(matched)}):")
for nc, st in matched:
    print(f"  '{nc}' -> '{st}'")

print(f"\n未匹配的队伍 ({len(unmatched)}):")
for nc in unmatched:
    print(f"  - {nc}")