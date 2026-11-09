import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def q(sql):
    return pd.read_sql_query(sql, conn)

print("="*70)
print("AUDITORIA DE ANOMALIAS E HERANÇAS DE MINUTA PRELIMINAR")
print("="*70)

# 1. Definições de KRs com anomalias
print("\n--- 1. DEFINIÇÃO DE KRs CHAVE ---")
df_kr = q("""
SELECT DISTINCT kr_codigo, kr_texto_completo 
FROM acoes 
WHERE kr_codigo IN ('E7.O2.KR2', 'E5.O6.KR1', 'E5.O3.KR2', 'E4.O1.KR1', 'E6.O2.KR1', 'E8.O1.KR1', 'E8.O1.KR2', 'E8.O2.KR1', 'E9.O1.KR1', 'E9.O1.KR2', 'E9.O1.KR3')
ORDER BY kr_codigo
""")
for _, r in df_kr.iterrows():
    print(f"[{r['kr_codigo']}] {r['kr_texto_completo']}")

# 2. PRI e PRT: detalhamento completo de todas as 53 ações de PRI
print("\n--- 2. PRI: LISTA COMPLETA DE AÇÕES POR KR ---")
df_pri = q("SELECT ordem, kr_codigo, papel_unidade, acao FROM acoes WHERE sigla_unidade = 'PRI' ORDER BY ordem")
for _, r in df_pri.iterrows():
    print(f"  #{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# 3. PGA: ações no Eixo 9.O1, Eixo 8, Eixo 7, Eixo 2
print("\n--- 3. PGA: AÇÕES EM E8, E9.O1, E7.O2, E2 ---")
df_pga = q("SELECT ordem, kr_codigo, papel_unidade, acao FROM acoes WHERE sigla_unidade = 'PGA' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%' OR kr_codigo = 'E7.O2.KR2' OR eixo LIKE '%2%') ORDER BY ordem")
for _, r in df_pga.iterrows():
    print(f"  #{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")
