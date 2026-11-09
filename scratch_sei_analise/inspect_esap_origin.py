import sqlite3
import glob
from pathlib import Path

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("SELECT * FROM unidades WHERE sigla = 'ESAP'")
row = c.fetchone()
print('Unidade ESAP:', row)

# Look for files mentioning ESAP in Cotejamento or Relatorios
for p in Path('.').glob('**/*ESAP*'):
    if p.suffix in ['.md', '.txt', '.pdf']:
        print(f"File: {p}")

for p in Path('.').glob('**/*Cotejamento*'):
    print(f"Cotejamento: {p}")
