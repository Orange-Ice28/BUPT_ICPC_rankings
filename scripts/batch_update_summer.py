"""
暑期集训全场次一键批量更新脚本
"""

import os
import sys

# 导入你原有的更新函数或直接复用逻辑
# 这里我们直接通过 subprocess 调用原脚本，或者直接集成数据循环
import subprocess

BATCH_DATA = [
    # hdu 1-10
    ("hdu", 1, 9, 791),
    ("hdu", 2, 10, 684),
    ("hdu", 3, 12, 699),
    ("hdu", 4, 12, 729),
    ("hdu", 5, 12, 757),
    ("hdu", 6, 12, 713),
    ("hdu", 7, 11, 726),
    ("hdu", 8, 12, 718),
    ("hdu", 9, 11, 689),
    ("hdu", 10, 12, 652),
    # nc 1-10
    ("nc", 1, 12, 1586),
    ("nc", 2, 14, 1612),
    ("nc", 3, 13, 1576),
    ("nc", 4, 11, 1311),
    ("nc", 5, 11, 1530),
    ("nc", 6, 10, 1495),
    ("nc", 7, 13, 1426),
    ("nc", 8, 13, 1405),
    ("nc", 9, 11, 1442),
    ("nc", 10, 13, 1203),
]

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    for contest_type, num, baseline, max_rank in BATCH_DATA:
        cmd = [sys.executable, "scripts/update_summer.py", contest_type, str(num), str(baseline), str(max_rank)]
        print(f"\n>>> 正在执行: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"错误: {contest_type} 第 {num} 场更新失败")
            sys.exit(1)
            
    print("\n==========================================")
    print("  所有场次已全部批量更新并同步完成！")
    print("==========================================")

if __name__ == "__main__":
    main()