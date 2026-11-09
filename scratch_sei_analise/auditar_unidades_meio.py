import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def q(sql):
    return pd.read_sql_query(sql, conn)

print("="*70)
print("AUDITORIA DE AÇÕES ATÍPICAS EM UNIDADES MEIO E DE APOIO")
print("="*70)

# 1. SGA
print("\n--- SGA: TODAS AS AÇÕES ---")
df = q("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'SGA' ORDER BY ordem")
for _, r in df.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# 2. SGT
print("\n--- SGT: TODAS AS AÇÕES ---")
df = q("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'SGT' ORDER BY ordem")
for _, r in df.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# 3. SMP
print("\n--- SMP: TODAS AS AÇÕES ---")
df = q("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'SMP' ORDER BY ordem")
for _, r in df.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# 4. SI (Sistemas / TI)
print("\n--- SI: TODAS AS AÇÕES ---")
df = q("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'SI' ORDER BY ordem")
for _, r in df.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# 5. UGAM
print("\n--- UGAM: TODAS AS AÇÕES ---")
df = q("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'UGAM' ORDER BY ordem")
for _, r in df.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")
