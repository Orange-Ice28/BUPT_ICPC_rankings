import subprocess
import os

os.chdir(r'd:\Software\bupt_icpc_rankings')

subprocess.run(['git', 'init'], check=True)
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Initial commit: ICPC ranking website'], check=True)
print("Done! Git repo initialized and committed.")