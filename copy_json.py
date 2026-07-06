import os
import shutil

src = r'd:\Software\bupt_icpc_rankings\data\score_data.json'
dst1 = r'd:\Software\bupt_icpc_rankings\bupt-ranking\public\score_data.json'
dst2 = r'd:\Software\bupt_icpc_rankings\bupt-ranking\src\data\score_data.json'

os.makedirs(os.path.dirname(dst2), exist_ok=True)

shutil.copy(src, dst1)
shutil.copy(src, dst2)

print(f"Copied {src} -> {dst1}")
print(f"Copied {src} -> {dst2}")
print("Done!")