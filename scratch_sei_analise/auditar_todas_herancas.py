import sqlite3
import pandas as pd
import sys

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

# 1. Leaders per KR
query_leaders = """
SELECT kr_codigo, sigla_unidade, count(*) as n_acoes
FROM acoes 
WHERE papel_unidade LIKE '%der%' OR papel_unidade LIKE '%L%der%'
GROUP BY kr_codigo, sigla_unidade
ORDER BY kr_codigo, sigla_unidade
"""
df_leaders = pd.read_sql_query(query_leaders, conn)
print("=== 1. LÍDERES POR KR ===")
for kr, group in df_leaders.groupby('kr_codigo'):
    leaders_str = ', '.join([f"{row['sigla_unidade']}({row['n_acoes']})" for _, row in group.iterrows()])
    print(f"[{kr}]: {leaders_str}")

# 2. Units in Eixo 8
print("\n=== 2. TODAS AS UNIDADES NO EIXO 8 ===")
query_e8 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE eixo LIKE '%8%'
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e8 = pd.read_sql_query(query_e8, conn)
for unit, group in df_e8.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")

# 3. Units in Eixo 9.O1 (Infra, Clima, Ergonomia, Refeitório)
print("\n=== 3. UNIDADES NO EIXO 9 - OBJETIVO 1 (Infra/Clima/Saúde/Copas) ===")
query_e9o1 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE kr_codigo LIKE 'E9.O1%'
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e9o1 = pd.read_sql_query(query_e9o1, conn)
for unit, group in df_e9o1.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")

# 4. Units in Eixo 2 (Licitações/Contratos)
print("\n=== 4. UNIDADES NO EIXO 2 (Licitações e Contratos) ===")
query_e2 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE eixo LIKE '%2%'
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e2 = pd.read_sql_query(query_e2, conn)
for unit, group in df_e2.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")

# 5. Units in Eixo 4 (Atendimento/Ouvidoria)
print("\n=== 5. UNIDADES NO EIXO 4 (Atendimento/Ouvidoria) ===")
query_e4 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE eixo LIKE '%4%'
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e4 = pd.read_sql_query(query_e4, conn)
for unit, group in df_e4.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")

# 6. Units in Eixo 7 (TI/Inovação)
print("\n=== 6. LÍDERES NO EIXO 7 (TI/Inovação) ===")
query_e7 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE eixo LIKE '%7%' AND (papel_unidade LIKE '%der%' OR papel_unidade LIKE '%L%der%')
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e7 = pd.read_sql_query(query_e7, conn)
for unit, group in df_e7.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")

# 7. Units in Eixo 1 (Fiscal)
print("\n=== 7. UNIDADES NO EIXO 1 (Fiscal) ===")
query_e1 = """
SELECT sigla_unidade, kr_codigo, papel_unidade, count(*) as n_acoes
FROM acoes 
WHERE eixo LIKE '%1%'
GROUP BY sigla_unidade, kr_codigo, papel_unidade
ORDER BY sigla_unidade, kr_codigo
"""
df_e1 = pd.read_sql_query(query_e1, conn)
for unit, group in df_e1.groupby('sigla_unidade'):
    krs = ', '.join([f"{row['kr_codigo']} ({row['papel_unidade']}: {row['n_acoes']})" for _, row in group.iterrows()])
    print(f"{unit}: {krs}")
