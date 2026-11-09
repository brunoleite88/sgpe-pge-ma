import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== CONTAGEM ATUAL NO BANCO ===")
c.execute("SELECT count(*) FROM acoes")
print("Total acoes:", c.fetchone()[0])

# Simulate changes:
# 1. ESAP:
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade='ESAP' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%')")
print("ESAP a remover (E8 + E9.O1):", c.fetchone()[0])

c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade='ESAP' AND kr_codigo='E6.O2.KR1' AND ordem IN (36, 37, 38, 39, 40, 42, 43)")
print("ESAP a remover em E6.O2.KR1 (duplicatas PGAAE):", c.fetchone()[0])

# 2. PRI e PRT:
for sigla in ['PRI', 'PRT']:
    c.execute(f"SELECT count(*) FROM acoes WHERE sigla_unidade='{sigla}' AND (kr_codigo LIKE 'E4%' OR kr_codigo IN ('E7.O1.KR1', 'E7.O3.KR1'))")
    rem_e4_e7 = c.fetchone()[0]
    c.execute(f"SELECT count(*) FROM acoes WHERE sigla_unidade='{sigla}' AND kr_codigo='E5.O6.KR1' AND ordem IN (44, 45, 46)")
    rem_e56 = c.fetchone()[0]
    print(f"{sigla} a remover (E4 + E7 + E5.O6 central):", rem_e4_e7 + rem_e56)

# 3. PGA:
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade='PGA' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%')")
print("PGA a remover (E8 + E9.O1):", c.fetchone()[0])

# 4. UGAM:
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade='UGAM' AND eixo LIKE '%8%'")
print("UGAM a remover (E8):", c.fetchone()[0])

# 5. CEQUIDADE:
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade='CEQUIDADE' AND kr_codigo='E8.O1.KR1'")
print("CEQUIDADE a remover (E8.O1.KR1):", c.fetchone()[0])
