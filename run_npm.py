import subprocess
import os
import sys

cwd = r'd:\Software\bupt_icpc_rankings\bupt-ranking'
log_path = r'd:\Software\bupt_icpc_rankings\bupt-ranking\npm_log.txt'

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(f"CWD: {cwd}\n")
    f.write(f"Exists: {os.path.exists(cwd)}\n")
    f.write(f"package.json: {os.path.exists(os.path.join(cwd, 'package.json'))}\n")

    r = subprocess.run(['node', '--version'], capture_output=True, text=True)
    f.write(f"Node: {r.stdout.strip()} | err={r.stderr.strip()} | rc={r.returncode}\n")

    r = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    f.write(f"npm: {r.stdout.strip()} | err={r.stderr.strip()} | rc={r.returncode}\n")

    f.write("\n--- Running npm install ---\n")
    f.flush()
    r = subprocess.run(['npm', 'install'], capture_output=True, text=True, cwd=cwd)
    f.write(f"STDOUT:\n{r.stdout}\n")
    f.write(f"STDERR:\n{r.stderr}\n")
    f.write(f"RC: {r.returncode}\n")
    f.write(f"node_modules exists: {os.path.exists(os.path.join(cwd, 'node_modules'))}\n")

print("DONE")