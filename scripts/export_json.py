import json
import os
import re

import openpyxl


# Resolve project root (script lives in scripts/)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DATA_DIR = "data"

SCORE_FILE = f"{DATA_DIR}/score_result.xlsx"
RANK_FILE = f"{DATA_DIR}/hdu_rank_all.xlsx"
BASELINE_FILE = f"{DATA_DIR}/baseline.xlsx"
TEAM_FILE = f"{DATA_DIR}/team.xlsx"

# 新增：考勤和录屏文件
ATTENDANCE_FILE = f"{DATA_DIR}/考勤.xlsx"
RECORDING_FILE = f"{DATA_DIR}/录屏.xlsx"


NUM_CONTESTS = 10
BEST_N_OLD = 7
BEST_N_NEW = 5
TEAM_THRESHOLD = 1791


def load_baseline():
    """
    读取 baseline.xlsx

    第 2 列：baseline
    第 3 列：max_rank
    """
    wb = openpyxl.load_workbook(BASELINE_FILE, data_only=True)
    ws = wb.active

    baselines_data = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        baseline_val = int(row[1]) if row[1] is not None else 0
        max_rank_val = (
            int(row[2])
            if len(row) > 2 and row[2] is not None
            else 800
        )

        baselines_data.append({
            "baseline": baseline_val,
            "max_rank": max_rank_val,
        })

    wb.close()

    return baselines_data


def load_teams():
    """
    读取 team.xlsx
    """
    wb = openpyxl.load_workbook(TEAM_FILE, data_only=True)
    ws = wb.active

    teams = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        seq, name_cn, name_en, leader, m1, m2 = row

        if name_cn is None:
            continue

        members = [
            m for m in (leader, m1, m2)
            if m is not None
        ]

        teams.append({
            "seq": seq,
            "name_cn": name_cn,
            "name_en": name_en,
            "members": members,
        })

    wb.close()

    return teams


def load_rank_data():
    """
    读取 hdu_rank_all.xlsx

    数据结构：

    team_id | name | 第1场solved | 第1场rank | 第2场solved | 第2场rank | ...

    最终：

    [
        {
            "team_id": "...",
            "name": "...",
            "contests": [
                {
                    "solved": 5,
                    "rank": 20
                },
                ...
            ]
        }
    ]
    """
    wb = openpyxl.load_workbook(RANK_FILE, data_only=True)
    ws = wb.active

    data = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        team_id = row[0]
        name = row[1]

        contests = []

        for i in range(NUM_CONTESTS):
            solved = row[2 + i * 2]
            rank = row[3 + i * 2]

            if solved is None:
                solved = 0

            if rank is None:
                rank = 0

            contests.append({
                "solved": int(solved),
                "rank": int(rank),
            })

        data.append({
            "team_id": team_id,
            "name": name,
            "contests": contests,
        })

    wb.close()

    return data


def load_recording_status():
    """
    读取录屏.xlsx

    表格格式：

    姓名 | 第1场 | 第2场 | ... | 第10场
    丁培钊 | 已提交 | 已提交 | ... | 已提交
    侯尔为 | 已提交 | 已提交 | ... | 未提交

    返回：

    {
        "丁培钊": [
            "已提交",
            "已提交",
            ...
        ],
        "侯尔为": [
            "已提交",
            "已提交",
            ...
            "未提交"
        ]
    }
    """
    if not os.path.exists(RECORDING_FILE):
        print(f"警告：找不到录屏文件：{RECORDING_FILE}")
        print("录屏状态将全部按照正常处理。")
        return {}

    wb = openpyxl.load_workbook(RECORDING_FILE, data_only=True)
    ws = wb.active

    data = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row:
            continue

        name = row[0]

        if name is None:
            continue

        name = str(name).strip()

        statuses = []

        for i in range(NUM_CONTESTS):
            col_index = 1 + i

            if col_index < len(row) and row[col_index] is not None:
                status = str(row[col_index]).strip()
            else:
                status = ""

            statuses.append(status)

        data[name] = statuses

    wb.close()

    print(f"读取录屏记录：{len(data)} 人")

    return data


def load_attendance_status():
    """
    读取考勤.xlsx

    表格格式：

    姓名 | 校区 | 第1场 | 第2场 | ... | 第10场
    安澍 | 西土城 | 正常 | 正常 | ... | 正常
    常昊天 | 沙河 | 正常 | 正常 | ... | 缺勤

    返回：

    {
        "安澍": [
            "正常",
            "正常",
            ...
        ],
        "常昊天": [
            "正常",
            "正常",
            ...
            "缺勤"
        ]
    }
    """
    if not os.path.exists(ATTENDANCE_FILE):
        print(f"警告：找不到考勤文件：{ATTENDANCE_FILE}")
        print("考勤状态将全部按照正常处理。")
        return {}

    wb = openpyxl.load_workbook(ATTENDANCE_FILE, data_only=True)
    ws = wb.active

    data = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row:
            continue

        name = row[0]

        if name is None:
            continue

        name = str(name).strip()

        statuses = []

        for i in range(NUM_CONTESTS):
            # 第 0 列：姓名
            # 第 1 列：校区
            # 第 2～11 列：第1～10场
            col_index = 2 + i

            if col_index < len(row) and row[col_index] is not None:
                status = str(row[col_index]).strip()
            else:
                status = ""

            statuses.append(status)

        data[name] = statuses

    wb.close()

    print(f"读取考勤记录：{len(data)} 人")

    return data


def calc_contest_score(solved, rank, baseline, max_rank):
    """
    正常情况下计算单场成绩。

    invalid 的场次不会调用这个函数，
    而是在外部直接将 score 设置为 0。
    """
    if baseline == 0 or max_rank == 0:
        return 0.0

    score = (
        (solved / baseline)
        * ((max_rank + 1) - rank)
        / max_rank
        * 100
    )

    if score < 0 or score > 100:
        return 0.0

    return score


def calc_personal_total(scores, team_id):
    """
    计算个人最终成绩。

    注意：
    invalid 场次虽然 score = 0，
    但仍然保留在 scores 中。

    因此：
        invalid 场次可以进入 best_indices；
        如果进入 best_indices，则这个 0 分会计入最终 total_score。

    例如 BEST_N = 5：

        scores = [90, 80, 70, 0, 0, 60, 50, 40, 30, 20]

    排序后取前 5：

        [90, 80, 70, 60, 50]

    0 分没有进入最佳 5。

    如果有效成绩不足 BEST_N，例如：

        scores = [90, 80, 70, 0, 0, 0, 0, 0, 0, 0]

    则前 5 是：

        [90, 80, 70, 0, 0]

    两个 invalid 的 0 分仍然可以进入 best_indices，
    并且最终仍然除以 BEST_N。
    """
    match = re.search(r"team(\d+)", team_id)
    num = int(match.group(1)) if match else 0

    best_n = BEST_N_OLD if num <= TEAM_THRESHOLD else BEST_N_NEW

    pairs = [
        (scores[i], i)
        for i in range(len(scores))
    ]

    if not pairs:
        return 0.0, set()

    pairs.sort(key=lambda x: x[0], reverse=True)

    top = pairs[:best_n]

    best_indices = {
        p[1]
        for p in top
    }

    total = sum(p[0] for p in top) / best_n

    return total, best_indices


def main():
    # ---------------------------------------------------------
    # 1. 读取基础数据
    # ---------------------------------------------------------

    baselines_data = load_baseline()
    teams = load_teams()
    rank_data = load_rank_data()

    # 保持原项目逻辑：排除 team1790
    rank_data = [
        item
        for item in rank_data
        if item["team_id"] != "team1790"
    ]

    # ---------------------------------------------------------
    # 2. 读取考勤、录屏数据
    # ---------------------------------------------------------

    recording_status = load_recording_status()
    attendance_status = load_attendance_status()

    # ---------------------------------------------------------
    # 3. 建立姓名 / team_id 映射
    # ---------------------------------------------------------

    name_to_team_id = {}

    for item in rank_data:
        name_to_team_id[item["name"]] = item["team_id"]

    team_id_to_data = {}

    for item in rank_data:
        team_id_to_data[item["team_id"]] = item

    # ---------------------------------------------------------
    # 4. 获取所有组队成员姓名
    # ---------------------------------------------------------

    team_member_names = set()

    for team in teams:
        for m in team["members"]:
            team_member_names.add(m)

    # ---------------------------------------------------------
    # 5. 计算个人成绩
    # ---------------------------------------------------------

    personal_results = []

    for item in rank_data:
        tid = item["team_id"]
        name = item["name"]

        scores = []
        contest_details = []

        # 获取该人的考勤和录屏记录
        person_recording = recording_status.get(name)
        person_attendance = attendance_status.get(name)

        for i, c in enumerate(item["contests"]):
            b_val = baselines_data[i]["baseline"]
            m_rank = baselines_data[i]["max_rank"]

            # -------------------------------------------------
            # 获取录屏状态
            # -------------------------------------------------

            if (
                person_recording is not None
                and i < len(person_recording)
            ):
                recording = person_recording[i]
            else:
                recording = ""

            # -------------------------------------------------
            # 获取考勤状态
            # -------------------------------------------------

            if (
                person_attendance is not None
                and i < len(person_attendance)
            ):
                attendance = person_attendance[i]
            else:
                attendance = ""

            # -------------------------------------------------
            # 判断本场是否无效
            #
            # 未提交 OR 缺勤
            # 任意一个成立，则 invalid = true
            # -------------------------------------------------

            invalid = (
                recording == "未提交"
                or attendance == "缺勤"
            )

            # -------------------------------------------------
            # 计算成绩
            #
            # invalid：
            #     score = 0
            #
            # 正常：
            #     按原公式计算
            # -------------------------------------------------

            if invalid:
                s = 0.0
            else:
                s = calc_contest_score(
                    c["solved"],
                    c["rank"],
                    b_val,
                    m_rank,
                )

            scores.append(s)

            contest_details.append({
                "solved": c["solved"],
                "rank": c["rank"],
                "score": round(s, 2),
                "invalid": invalid,
            })

        # -----------------------------------------------------
        # 6. 计算个人总成绩
        #
        # 注意：
        # invalid 的 0 分仍然在 scores 中，
        # 所以仍然可以进入 best_indices。
        # -----------------------------------------------------

        total, best_indices = calc_personal_total(
            scores,
            tid,
        )

        personal_results.append({
            "team_id": tid,
            "name": name,
            "total_score": round(total, 2),
            "contests": contest_details,
            "best_indices": sorted(list(best_indices)),
            "in_team": name in team_member_names,
        })

    # ---------------------------------------------------------
    # 7. 特殊处理：周弋然第 8 场成绩强制为 0
    #
    # 保持原项目逻辑
    # ---------------------------------------------------------

    zhou_team_id = name_to_team_id.get("周弋然")

    if zhou_team_id:
        for p in personal_results:
            if p["team_id"] == zhou_team_id:
                p["contests"][7]["score"] = 0.0

                scores = [
                    d["score"]
                    for d in p["contests"]
                ]

                total, best_indices = calc_personal_total(
                    scores,
                    zhou_team_id,
                )

                p["total_score"] = round(total, 2)
                p["best_indices"] = sorted(
                    list(best_indices)
                )

                break

    # ---------------------------------------------------------
    # 8. 个人排名
    # ---------------------------------------------------------

    personal_results.sort(
        key=lambda x: x["total_score"],
        reverse=True,
    )

    for i, p in enumerate(personal_results):
        p["rank"] = i + 1

    # ---------------------------------------------------------
    # 9. 计算团队成绩
    # ---------------------------------------------------------

    team_results = []

    # 建立 team_id -> personal_result 映射
    personal_result_map = {
        p["team_id"]: p
        for p in personal_results
    }

    for team in teams:
        member_info = []
        member_scores = []

        for member_name in team["members"]:
            tid = name_to_team_id.get(member_name)

            if tid:
                pr = personal_result_map.get(tid)

                if pr:
                    member_info.append({
                        "name": member_name,
                        "total_score": pr["total_score"],
                    })

                    member_scores.append(
                        pr["total_score"]
                    )
                else:
                    member_info.append({
                        "name": member_name,
                        "total_score": 0.0,
                    })

                    member_scores.append(0.0)

            else:
                member_info.append({
                    "name": member_name,
                    "total_score": 0.0,
                })

                member_scores.append(0.0)

        team_total = (
            sum(member_scores) / len(member_scores)
            if member_scores
            else 0.0
        )

        team_results.append({
            "name_cn": team["name_cn"],
            "name_en": team["name_en"],
            "members": member_info,
            "team_total": round(team_total, 2),
        })

    # ---------------------------------------------------------
    # 10. 团队排名
    # ---------------------------------------------------------

    team_results.sort(
        key=lambda x: x["team_total"],
        reverse=True,
    )

    for i, t in enumerate(team_results):
        t["rank"] = i + 1

    # ---------------------------------------------------------
    # 11. 生成 JSON
    # ---------------------------------------------------------

    baselines_list = [
        b["baseline"]
        for b in baselines_data
    ]

    result = {
        "baselines": baselines_list,
        "personal": personal_results,
        "teams": team_results,
    }

    output_file = f"{DATA_DIR}/score_data.json"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2,
        )

    # ---------------------------------------------------------
    # 12. 输出日志
    # ---------------------------------------------------------

    invalid_count = 0

    for p in personal_results:
        for contest in p["contests"]:
            if contest["invalid"]:
                invalid_count += 1

    with open(
        f"{DATA_DIR}/export_log.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            f"Personal count: {len(personal_results)}\n"
        )

        f.write(
            f"Team count: {len(team_results)}\n"
        )

        f.write(
            f"Baselines: {baselines_list}\n"
        )

        f.write(
            f"Invalid contest count: {invalid_count}\n"
        )

        f.write("Done.\n")

    print()
    print("========================================")
    print("JSON 导出完成")
    print("========================================")
    print(f"个人数量：{len(personal_results)}")
    print(f"团队数量：{len(team_results)}")
    print(f"Baselines：{baselines_list}")
    print(f"无效场次数量：{invalid_count}")
    print(f"输出文件：{output_file}")
    print("========================================")


if __name__ == "__main__":
    main()
