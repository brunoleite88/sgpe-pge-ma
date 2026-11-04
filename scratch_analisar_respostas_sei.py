import os
import sys
import re
from bs4 import BeautifulSoup
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

base_dir = 'scratch_sei_analise'

processes = [
    'SEI_2026.11103.07207',
    'SEI_2026.11103.07208',
    'SEI_2026.11103.07209',
    'SEI_2026.11103.07215',
    'SEI_2025.11103.05165'
]

def clean_html(html_path):
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator='\n')
        # Break into lines and remove leading and trailing space on each
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)

for p in processes:
    p_path = os.path.join(base_dir, p)
    print(f"\n{'='*70}")
    print(f"PROCESSO: {p}")
    print(f"{'='*70}")
    
    files = sorted(os.listdir(p_path))
    for f in files:
        f_path = os.path.join(p_path, f)
        print(f"\n--- ARQUIVO: {f} ---")
        if f.endswith('.html'):
            txt = clean_html(f_path)
            # Print first 2500 characters or key sections
            print(txt[:2500])
            if len(txt) > 2500:
                print(f"\n[... truncado {len(txt)-2500} caracteres ...]")
                # Print last 1000 characters if it's long
                print("\n[FINAL DO DOCUMENTO]:")
                print(txt[-1000:])
        elif f.endswith('.xlsx'):
            wb = openpyxl.load_workbook(f_path, data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
            print(f"Planilha Excel: {ws.title} ({len(rows)} linhas)")
            for r in rows[:8]:
                if any(r):
                    print("  ", [str(c)[:30] if c is not None else '' for c in r[:6]])
        elif f.endswith('.pdf'):
            print(f"Arquivo PDF ({os.path.getsize(f_path)} bytes)")
