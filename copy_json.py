import os
import shutil

os.makedirs(r'd:\Software\bupt_icpc_rankings\bupt-ranking\src\data', exist_ok=True)
shutil.copy(
    r'd:\Software\bupt_icpc_rankings\bupt-ranking\public\score_data.json',
    r'd:\Software\bupt_icpc_rankings\bupt-ranking\src\data\score_data.json'
)
print("Done!")