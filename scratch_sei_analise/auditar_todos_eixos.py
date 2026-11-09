import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def q(sql):
    return pd.read_sql_query(sql, conn)

print("="*70)
print("AUDITORIA POR EIXO E UNIDADE: IDENTIFICANDO TODAS AS HERANÇAS")
print("="*70)

# 1. Eixo 1
print("\n--- EIXO 1 (Fiscal) ---")
df1 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%1%' ORDER BY sigla_unidade")
print(df1.to_string())

# 2. Eixo 2
print("\n--- EIXO 2 (Licitações e Contratos) ---")
df2 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%2%' ORDER BY sigla_unidade")
print(df2.to_string())

# 3. Eixo 3
print("\n--- EIXO 3 (Orçamento e Captação) ---")
df3 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%3%' ORDER BY sigla_unidade")
print(df3.to_string())

# 4. Eixo 4
print("\n--- EIXO 4 (Atendimento e Ouvidoria) ---")
df4 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%4%' ORDER BY sigla_unidade")
print(df4.to_string())

# 5. Eixo 5
print("\n--- EIXO 5 (Contencioso / Eficiência) - LÍDERES ---")
df5 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%5%' AND papel_unidade LIKE '%der%' ORDER BY kr_codigo, sigla_unidade")
print(df5.to_string())

# 6. Eixo 6
print("\n--- EIXO 6 (Comunicação e Relações) ---")
df6 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%6%' ORDER BY sigla_unidade")
print(df6.to_string())

# 7. Eixo 7
print("\n--- EIXO 7 (TI e Inovação) - LÍDERES ---")
df7 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%7%' AND papel_unidade LIKE '%der%' ORDER BY kr_codigo, sigla_unidade")
print(df7.to_string())

# 8. Eixo 8
print("\n--- EIXO 8 (Sustentabilidade e Integridade) ---")
df8 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%8%' ORDER BY sigla_unidade")
print(df8.to_string())

# 9. Eixo 9
print("\n--- EIXO 9 (Pessoas e Clima) ---")
df9 = q("SELECT DISTINCT sigla_unidade, kr_codigo, papel_unidade FROM acoes WHERE eixo LIKE '%9%' AND kr_codigo NOT LIKE 'E9.O2.KR1' ORDER BY sigla_unidade")
print(df9.to_string())
