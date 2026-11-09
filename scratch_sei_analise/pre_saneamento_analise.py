import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

print("--- 1. ESAP E6.O2.KR1 ---")
df = pd.read_sql_query("SELECT id, ordem, acao, subacao, papel_unidade FROM acoes WHERE sigla_unidade='ESAP' AND kr_codigo='E6.O2.KR1' ORDER BY ordem", conn)
for _, r in df.iterrows():
    print(f"ID:{r['id']} | Ordem:{r['ordem']} | {r['papel_unidade']} | {r['acao']}")

print("\n--- 2. PRI E PRT AÇÕES DETALHADAS ---")
df = pd.read_sql_query("SELECT id, ordem, kr_codigo, papel_unidade, acao FROM acoes WHERE sigla_unidade='PRI' ORDER BY ordem", conn)
for _, r in df.iterrows():
    print(f"ID:{r['id']} | #{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

print("\n--- 3. PGA: AÇÕES DUPLICADAS COM PGAAE ---")
df = pd.read_sql_query("""
SELECT a1.id, a1.ordem, a1.kr_codigo, a1.papel_unidade as pga_papel, a2.papel_unidade as pgaae_papel, a1.acao
FROM acoes a1
JOIN acoes a2 ON a1.acao = a2.acao AND a1.kr_codigo = a2.kr_codigo
WHERE a1.sigla_unidade = 'PGA' AND a2.sigla_unidade = 'PGAAE'
ORDER BY a1.ordem
""", conn)
for _, r in df.iterrows():
    print(f"PGA ID:{r['id']} | #{r['ordem']} | {r['kr_codigo']} | PGA:{r['pga_papel']} | PGAAE:{r['pgaae_papel']} | {r['acao'][:50]}")
