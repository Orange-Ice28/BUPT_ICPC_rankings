import os
import pickle
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl

COOKIE_FILE = "hdu_cookies.pkl"

BASE_URL = "https://acm.hdu.edu.cn/contest/rank?cid={cid}&group=all&search=%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5"

CONTEST_IDS = list(range(1197, 1207))

DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "hdu_rank_all.xlsx")


def create_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def save_cookies(driver, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"Cookies 已保存到 {filepath}")


def load_cookies(driver, filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "rb") as f:
        cookies = pickle.load(f)
    driver.get("https://acm.hdu.edu.cn/")
    time.sleep(1)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
    print(f"Cookies 已从 {filepath} 加载")
    return True


def is_logged_in(driver):
    try:
        driver.get(BASE_URL.format(cid=CONTEST_IDS[0]))
        time.sleep(2)
        current_url = driver.current_url
        if "login" in current_url:
            return False
        return True
    except Exception:
        return False


def wait_for_login(driver):
    driver.get(BASE_URL.format(cid=CONTEST_IDS[0]))
    print("\n" + "=" * 60)
    print("检测到需要登录，请在浏览器中手动登录 HDU 账号")
    print("登录成功后脚本会自动继续...")
    print("=" * 60 + "\n")

    while True:
        time.sleep(2)
        current_url = driver.current_url
        if "login" not in current_url:
            print("登录成功！")
            save_cookies(driver, COOKIE_FILE)
            break


def parse_rank_page(driver):
    results = []

    tables = driver.find_elements(By.CSS_SELECTOR, "table")
    target_table = None
    for table in tables:
        rows = table.find_elements(By.CSS_SELECTOR, "tr")
        if len(rows) > 3:
            target_table = table
            break

    if target_table is None:
        return results

    rows = target_table.find_elements(By.CSS_SELECTOR, "tr")

    header_row = rows[0]
    header_cells = header_row.find_elements(By.CSS_SELECTOR, "th, td")
    header_texts = [c.text.strip() for c in header_cells]

    author_idx = None
    rank_idx = None
    solved_idx = None

    for i, h in enumerate(header_texts):
        h_lower = h.lower()
        if h_lower in ("author", "team", "name", "nickname"):
            author_idx = i
        elif h_lower == "rank":
            rank_idx = i
        elif h_lower == "solved":
            solved_idx = i

    if author_idx is None:
        for i, h in enumerate(header_texts):
            h_lower = h.lower()
            if "author" in h_lower or "team" in h_lower or "name" in h_lower:
                author_idx = i
                break

    if rank_idx is None:
        for i, h in enumerate(header_texts):
            if h.lower() == "rank":
                rank_idx = i
                break

    if solved_idx is None:
        for i, h in enumerate(header_texts):
            if h.lower() == "solved":
                solved_idx = i
                break

    if author_idx is None:
        print("  无法定位 Author/Team 列")
        return results

    team_pattern = re.compile(r"team(\d+)", re.IGNORECASE)

    for row in rows[1:]:
        cells = row.find_elements(By.CSS_SELECTOR, "td, th")
        if len(cells) <= author_idx:
            continue

        cell_text = cells[author_idx].text.strip()
        if not cell_text:
            continue

        parts = [p.strip() for p in cell_text.split("\n") if p.strip()]

        team_id = None
        team_name = ""

        for part in parts:
            tm = team_pattern.match(part)
            if tm:
                team_id = tm.group(0)
            elif team_id:
                team_name = part
                break

        if not team_id:
            continue

        if not team_name:
            team_name = parts[1] if len(parts) > 1 else ""

        rank_val = ""
        solved_val = ""

        if rank_idx is not None and len(cells) > rank_idx:
            rank_val = cells[rank_idx].text.strip()
        if solved_idx is not None and len(cells) > solved_idx:
            solved_val = cells[solved_idx].text.strip()

        results.append({
            "team_id": team_id,
            "name": team_name,
            "rank": rank_val,
            "solved": solved_val,
        })

    return results


def crawl_all_contests(driver):
    all_data = {}

    for cid in CONTEST_IDS:
        url = BASE_URL.format(cid=cid)
        print(f"\n正在爬取 cid={cid} ...")
        driver.get(url)
        time.sleep(3)

        results = parse_rank_page(driver)
        print(f"  获取到 {len(results)} 条记录")

        for item in results:
            tid = item["team_id"]
            if tid not in all_data:
                all_data[tid] = {
                    "name": item["name"],
                    "contests": {},
                }
            all_data[tid]["contests"][cid] = {
                "solved": item["solved"],
                "rank": item["rank"],
            }

    return all_data


def save_merged_xlsx(all_data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "HDU Rank"

    headers = ["队伍编号", "姓名"]
    for i, cid in enumerate(CONTEST_IDS, 1):
        headers.append(f"第{i}场 题数")
        headers.append(f"第{i}场 排名")
    ws.append(headers)

    sorted_teams = sorted(all_data.keys(), key=lambda x: int(re.search(r"team(\d+)", x).group(1)))

    for tid in sorted_teams:
        info = all_data[tid]
        row_data = [tid, info["name"]]
        for cid in CONTEST_IDS:
            contest = info["contests"].get(cid, {})
            row_data.append(contest.get("solved", 0) or 0)
            row_data.append(contest.get("rank", 0) or 0)
        ws.append(row_data)

    col_widths = {"A": 14, "B": 16}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(filepath)
    print(f"\n数据已保存到 {filepath}，共 {len(sorted_teams)} 支队伍")


def main():
    print("正在启动浏览器...")
    driver = create_driver()

    try:
        if load_cookies(driver, COOKIE_FILE) and is_logged_in(driver):
            print("已通过 cookies 恢复登录状态")
        else:
            wait_for_login(driver)

        all_data = crawl_all_contests(driver)
        save_merged_xlsx(all_data, OUTPUT_FILE)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()