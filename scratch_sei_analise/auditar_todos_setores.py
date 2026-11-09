import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def run_query(q):
    return pd.read_sql_query(q, conn)

print("="*60)
print("AUDITORIA SISTÊMICA DE HERANÇAS INDEVIDAS")
print("="*60)

# 1. Checar Eixo 8 completo: todas as unidades e suas ações
print("\n--- 1. EIXO 8: DETALHE DE TODAS AS AÇÕES POR UNIDADE ---")
df_e8 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao 
FROM acoes 
WHERE eixo LIKE '%8%' 
ORDER BY kr_codigo, sigla_unidade, ordem
""")
for idx, r in df_e8.iterrows():
    print(f"[{r['sigla_unidade']}] {r['kr_codigo']} | {r['papel_unidade']} | #{r['ordem']} {r['acao']}")

# 2. Checar Eixo 9.O1 completo: todas as unidades e suas ações
print("\n--- 2. EIXO 9 - OBJETIVO 1 (Infra, Clima, Ergonomia, Saúde) ---")
df_e91 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao 
FROM acoes 
WHERE kr_codigo LIKE 'E9.O1%' 
ORDER BY kr_codigo, sigla_unidade, ordem
""")
for idx, r in df_e91.iterrows():
    print(f"[{r['sigla_unidade']}] {r['kr_codigo']} | {r['papel_unidade']} | #{r['ordem']} {r['acao']}")

# 3. Checar unidades com Eixo 2 (Licitações/Contratos)
print("\n--- 3. EIXO 2 (Licitações e Contratos): UNIDADES E PAPÉIS ---")
df_e2 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n
FROM acoes 
WHERE eixo LIKE '%2%' 
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY kr_codigo, sigla_unidade
""")
for idx, r in df_e2.iterrows():
    print(f"[{r['sigla_unidade']}] {r['kr_codigo']} | {r['papel_unidade']} | {r['n']} ações")

# 4. Checar Eixo 4 (Atendimento / Ouvidoria / Consultas)
print("\n--- 4. EIXO 4: UNIDADES E PAPÉIS ---")
df_e4 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n
FROM acoes 
WHERE eixo LIKE '%4%' 
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY kr_codigo, sigla_unidade
""")
for idx, r in df_e4.iterrows():
    print(f"[{r['sigla_unidade']}] {r['kr_codigo']} | {r['papel_unidade']} | {r['n']} ações")

# 5. Checar Eixo 5.O6.KR1 (Prazo Zero Perdido)
print("\n--- 5. E5.O6.KR1 (Prazo Zero Perdido): AÇÕES COM PAPEL LÍDER ---")
df_e56 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao 
FROM acoes 
WHERE kr_codigo = 'E5.O6.KR1' AND (papel_unidade LIKE '%der%' OR papel_unidade LIKE '%L%der%')
ORDER BY sigla_unidade, ordem
""")
for idx, r in df_e56.iterrows():
    print(f"[{r['sigla_unidade']}] #{r['ordem']} {r['acao']} | Sub: {str(r['subacao'])[:60]}")

# 6. Checar E7.O1.KR1 (Automações e IA)
print("\n--- 6. E7.O1.KR1: LÍDERES ---")
df_e71 = run_query("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao 
FROM acoes 
WHERE kr_codigo = 'E7.O1.KR1' AND (papel_unidade LIKE '%der%' OR papel_unidade LIKE '%L%der%')
ORDER BY sigla_unidade, ordem
""")
for idx, r in df_e71.iterrows():
    print(f"[{r['sigla_unidade']}] #{r['ordem']} {r['acao']} | Sub: {str(r['subacao'])[:60]}")
