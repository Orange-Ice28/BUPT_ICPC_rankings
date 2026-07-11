import json
import openpyxl
import sys

wb = openpyxl.load_workbook(r'd:\Software\bupt_icpc_rankings\data\history.xlsx')
ws = wb.active
rows = []
for row in ws.iter_rows(values_only=True):
    rows.append([str(c) if c is not None else '' for c in row])

sys.stdout.reconfigure(encoding='utf-8')
print("HEADERS: " + json.dumps(rows[0], ensure_ascii=False))
print("TOTAL: " + str(len(rows)))
for i, row in enumerate(rows):
    print(f"ROW{i}: " + json.dumps(row, ensure_ascii=False))