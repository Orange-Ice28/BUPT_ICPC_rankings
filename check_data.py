import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/score_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Baselines: {data['baselines']}")
print(f"Number of baselines: {len(data['baselines'])}")

# 检查第一个人的比赛数据
if data['personal']:
    first = data['personal'][0]
    print(f"\nFirst person: {first['name']}")
    print(f"Number of contests: {len(first['contests'])}")
    print(f"Contests: {first['contests']}")