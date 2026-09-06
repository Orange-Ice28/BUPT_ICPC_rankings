"""
网络赛成绩更新脚本
==================
用法:
  python scripts/update_net_contest.py 1          # 更新网络赛第1场
  python scripts/update_net_contest.py 1 12       # 更新网络赛第1场，指定 baseline=12
  python scripts/update_net_contest.py 2          # 更新网络赛第2场
  python scripts/update_net_contest.py 3 10       # 更新网络赛第3场，指定 baseline=10

功能:
  1. 读取对应 Excel sheet 的队伍数据
  2. 按公式计算每队得分，填回 Excel
  3. 更新 data/net_score_data.json
  4. 重新计算队伍总成绩（3场平均分）和排名
  5. 同步到 bupt-ranking/ 前端目录
"""

import openpyxl
import json
import math
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Resolve project root (script lives in scripts/)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================
# 配置
# ============================================================
EXCEL_FILE = "data/net_contest.xlsx"
SHEET_TEMPLATE = "net{num}"       # net1, net2, net3
JSON_FILE = os.path.join("data", "net_score_data.json")
RANK_OFFSET = 1001                # 公式中的排名上限参数
DEFAULT_BASELINE = 12
CONTEST_COUNT = 3                 # 总共 3 场网络赛

# Excel 列映射（0-based）: 队名, 学校, 过题数, 排名, Baseline, 得分
COL_NAME = 0
COL_SCHOOL = 1
COL_SOLVED = 2
COL_RANK = 3
COL_BASELINE = 4
COL_SCORE = 5

# 前端同步目录
FRONTEND_DIRS = [
    os.path.join("bupt-ranking", "src", "data"),
    os.path.join("bupt-ranking", "public"),
]

# 队伍名映射（Excel 中的名字 → JSON 中的 name_cn）
NAME_MAPPING = {
    # 示例: 'Excel中的名字': 'JSON中的名字',
}

# ============================================================
# 工具函数
# ============================================================

def parse_special_value(val):
    """解析 Excel 单元格值，处理特殊文本（因公出差、未参加等）
    返回 (numeric_value, special_type)
      special_type: 'excused' (因公出差), 'absent' (未参加), None (正常)
    """
    if val is None:
        return 0, None
    if isinstance(val, str):
        s = val.strip()
        if '因公出差' in s:
            return 0, 'excused'
        if '未参加' in s:
            return 0, 'absent'
    try:
        return int(val), None
    except (ValueError, TypeError):
        return 0, None


def calc_score(solved, rank, baseline):
    """计算网络赛单场得分
    公式: 得分 = 过题数 / baseline × (1001 − 排名) / 1000 × 100
    得分 clamp 到 [0, 100]
    """
    if baseline == 0:
        return 0.0
    score = (solved / baseline) * (RANK_OFFSET - rank) / (RANK_OFFSET - 1) * 100
    if score < 0 or score > 100:
        return 0.0
    return round(score, 2)


def load_excel_teams(sheet_name):
    """从 Excel 读取队伍数据"""
    if not os.path.exists(EXCEL_FILE):
        print(f"错误: 找不到文件 '{EXCEL_FILE}'")
        return None, None, None

    wb = openpyxl.load_workbook(EXCEL_FILE)

    if sheet_name not in wb.sheetnames:
        print(f"错误: 找不到 sheet '{sheet_name}'")
        print(f"可用的 sheet: {wb.sheetnames}")
        wb.close()
        return None, None, None

    ws = wb[sheet_name]
    teams = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        name = row[COL_NAME] if COL_NAME < len(row) else None
        if name is None:
            continue

        raw_solved = row[COL_SOLVED] if COL_SOLVED < len(row) else None
        raw_rank = row[COL_RANK] if COL_RANK < len(row) else None

        solved_val, special_s = parse_special_value(raw_solved)
        rank_val, special_r = parse_special_value(raw_rank)

        is_excused = (special_s == 'excused' or special_r == 'excused')
        is_absent = (special_s == 'absent' or special_r == 'absent')

        teams.append({
            "name": name,
            "solved": solved_val,
            "rank": rank_val,
            "baseline": int(row[COL_BASELINE]) if COL_BASELINE < len(row) and row[COL_BASELINE] else 0,
            "score": row[COL_SCORE] if COL_SCORE < len(row) else None,
            "excused": is_excused,
            "absent": is_absent,
        })

    return wb, ws, teams


def load_net_data():
    """加载 net_score_data.json"""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_net_data(data):
    """保存 net_score_data.json 并同步到前端"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {JSON_FILE}")

    for d in FRONTEND_DIRS:
        target = os.path.join(d, "net_score_data.json")
        os.makedirs(d, exist_ok=True)
        shutil.copy(JSON_FILE, target)
        print(f"  已同步: {target}")


def match_team(excel_name, net_teams):
    """将 Excel 中的队伍名匹配到 net_score_data.json 中的队伍"""
    # 先检查映射表
    if excel_name in NAME_MAPPING:
        mapped = NAME_MAPPING[excel_name]
        for t in net_teams:
            if t["name_cn"] == mapped:
                return t

    # 精确匹配中文名
    for t in net_teams:
        if t["name_cn"] == excel_name:
            return t

    # 模糊匹配中文名
    for t in net_teams:
        if excel_name in t["name_cn"] or t["name_cn"] in excel_name:
            return t

    # 匹配英文名（标准化后比较）
    def normalize(s):
        return s.replace(" ", "").replace("://", "").replace("!", "").lower()

    nc_norm = normalize(excel_name)
    for t in net_teams:
        en_norm = normalize(t.get("name_en", ""))
        if en_norm and (nc_norm == en_norm or en_norm in nc_norm or nc_norm in en_norm):
            return t

    return None


def recalc_team_totals(data):
    """重新计算所有队伍的网络赛总成绩和排名
    网络赛规则：3 场全部计入，取平均分
    """
    for team in data["teams"]:
        scores = []
        for c in team["contests"]:
            if c.get("excused", False):
                # 因公出差：不计入
                continue
            if c.get("absent", False):
                # 未参加：按 0 分计入
                scores.append(0.0)
                continue
            if c["solved"] > 0 or c["score"] > 0:
                scores.append(c["score"])
            # 如果过题数和得分都为 0，视为尚未参赛，不计入

        if len(scores) == 0:
            team["team_total"] = 0.0
        else:
            team["team_total"] = round(sum(scores) / 3, 2)

    # 排序并更新排名
    data["teams"].sort(key=lambda x: x["team_total"], reverse=True)
    for i, team in enumerate(data["teams"]):
        team["rank"] = i + 1


def init_net_data():
    """首次运行时，从 score_data.json 读取队伍信息创建模板"""
    score_data_file = os.path.join("data", "score_data.json")
    if not os.path.exists(score_data_file):
        print(f"错误: 找不到 {score_data_file}，无法初始化队伍模板")
        sys.exit(1)

    with open(score_data_file, "r", encoding="utf-8") as f:
        spring_data = json.load(f)

    teams = []
    for t in spring_data["teams"]:
        team = {
            "name_cn": t["name_cn"],
            "name_en": t.get("name_en", ""),
            "members": [{"name": m["name"]} for m in t["members"]],
            "team_total": 0.0,
            "rank": 0,
            "contests": [
                {"solved": 0, "rank": 0, "score": 0.0, "excused": False, "absent": False}
                for _ in range(CONTEST_COUNT)
            ],
        }
        teams.append(team)

    data = {
        "baselines": [0] * CONTEST_COUNT,
        "teams": teams,
    }

    save_net_data(data)
    print(f"  已初始化 {len(teams)} 支队伍的网络赛数据模板")
    return data


# ============================================================
# 主流程
# ============================================================

def main():
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("用法: python scripts/update_net_contest.py <场次> [baseline]")
        print()
        print("示例:")
        print("  python scripts/update_net_contest.py 1       # 网络赛第1场")
        print("  python scripts/update_net_contest.py 1 12    # 网络赛第1场，baseline=12")
        print("  python scripts/update_net_contest.py 2       # 网络赛第2场")
        print("  python scripts/update_net_contest.py 3 10    # 网络赛第3场，baseline=10")
        sys.exit(1)

    try:
        contest_num = int(sys.argv[1])
    except (ValueError, IndexError):
        print("错误: 场次必须是整数")
        sys.exit(1)

    if contest_num < 1 or contest_num > CONTEST_COUNT:
        print(f"错误: 场次必须在 1~{CONTEST_COUNT} 之间")
        sys.exit(1)

    sheet_name = SHEET_TEMPLATE.format(num=contest_num)
    contest_idx = contest_num - 1  # net1 → index 0, net2 → index 1, net3 → index 2
    default_baseline = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    print("=" * 65)
    print(f"  更新网络赛第 {contest_num} 场 (sheet: {sheet_name}, idx: {contest_idx})")
    print("=" * 65)
    print()

    # ---- 第1步：读取 Excel 数据 ----
    print("[1/5] 读取 Excel 数据...")
    wb, ws, excel_teams = load_excel_teams(sheet_name)
    if excel_teams is None:
        sys.exit(1)
    print(f"  从 {EXCEL_FILE} / {sheet_name} 读取到 {len(excel_teams)} 支队伍")

    # ---- 第2步：计算得分 ----
    print()
    formula_desc = f"(solved/baseline) × ({RANK_OFFSET} - rank) / {RANK_OFFSET - 1} × 100"
    print(f"[2/5] 计算得分 — 公式: {formula_desc}")
    print()

    for team in excel_teams:
        if team["excused"]:
            team["score"] = 0.0
            team["baseline"] = default_baseline or team["baseline"] or DEFAULT_BASELINE
            print(f"  {team['name']:<35s}  ⚠ 因公出差 → 不计入成绩")
        elif team["absent"]:
            team["score"] = 0.0
            team["baseline"] = default_baseline or team["baseline"] or DEFAULT_BASELINE
            print(f"  {team['name']:<35s}  ✘ 未参加 → 得分=0.00")
        else:
            baseline = default_baseline or team["baseline"] or DEFAULT_BASELINE
            if team["baseline"] == 0 or team["baseline"] is None:
                team["baseline"] = baseline

            score = calc_score(team["solved"], team["rank"], baseline)
            team["score"] = score
            team["baseline"] = baseline
            print(f"  {team['name']:<35s}  "
                  f"solved={team['solved']:<3d}  rank={team['rank']:<6d}  "
                  f"baseline={baseline}  →  score={score:>7.2f}")

    # ---- 第3步：写回 Excel ----
    print()
    print("[3/5] 写回 Excel...")
    score_col = COL_SCORE + 1    # openpyxl 1-indexed
    baseline_col = COL_BASELINE + 1

    for i, team in enumerate(excel_teams):
        row_idx = i + 2  # 第1行是表头
        ws.cell(row=row_idx, column=score_col).value = team["score"]
        existing_baseline = ws.cell(row=row_idx, column=baseline_col).value
        if existing_baseline is None or existing_baseline == 0:
            ws.cell(row=row_idx, column=baseline_col).value = team["baseline"]

    wb.save(EXCEL_FILE)
    wb.close()
    print(f"  已保存到: {EXCEL_FILE}")

    # ---- 第4步：更新 net_score_data.json ----
    print()
    print("[4/5] 更新 net_score_data.json...")

    # 如果 JSON 文件不存在，先初始化
    if not os.path.exists(JSON_FILE):
        print("  首次运行，正在初始化网络赛数据模板...")
        data = init_net_data()
    else:
        data = load_net_data()

    # 确保 baselines 数组长度足够
    while len(data["baselines"]) <= contest_idx:
        data["baselines"].append(0)

    used_baseline = excel_teams[0]["baseline"] if excel_teams else DEFAULT_BASELINE
    data["baselines"][contest_idx] = used_baseline
    print(f"  baselines[{contest_idx}] = {used_baseline}")

    # 更新每支队伍的 contest 数据
    matched_count = 0
    unmatched = []

    for excel_team in excel_teams:
        matched = match_team(excel_team["name"], data["teams"])
        if matched:
            # 确保 contests 数组足够长
            while len(matched["contests"]) <= contest_idx:
                matched["contests"].append({
                    "solved": 0, "rank": 0, "score": 0.0,
                    "excused": False, "absent": False,
                })

            matched["contests"][contest_idx] = {
                "solved": excel_team["solved"],
                "rank": excel_team["rank"],
                "score": excel_team["score"],
                "excused": excel_team["excused"],
                "absent": excel_team["absent"],
            }
            matched_count += 1
            print(f"  OK '{excel_team['name']}' → '{matched['name_cn']}' "
                  f"(solved={excel_team['solved']}, rank={excel_team['rank']}, score={excel_team['score']})")
        else:
            unmatched.append(excel_team["name"])
            print(f"  !! '{excel_team['name']}' → 未找到匹配队伍!")

    if unmatched:
        print()
        print(f"  警告: {len(unmatched)} 支队伍未匹配:")
        for name in unmatched:
            print(f"    - {name}")
        print(f"  请在脚本顶部的 NAME_MAPPING 中添加映射。")

    # ---- 第5步：重新计算总成绩并保存 ----
    print()
    print("[5/5] 重新计算队伍总成绩...")
    recalc_team_totals(data)

    # 打印排名
    print()
    print("  Top 10 队伍总成绩:")
    for team in data["teams"][:10]:
        n_data = sum(1 for c in team["contests"]
                     if (c["solved"] > 0 or c["score"] > 0 or c.get("absent", False))
                     and not c.get("excused", False))
        print(f"    {team['rank']:>2}. {team['name_cn']:<20s}  "
              f"{team['team_total']:>6.2f}  (已有数据: {n_data}场)")

    save_net_data(data)

    # ---- 完成 ----
    print()
    print("=" * 65)
    print(f"  网络赛第 {contest_num} 场更新完成! 共处理 {len(excel_teams)} 支队伍")
    print("=" * 65)


if __name__ == "__main__":
    main()