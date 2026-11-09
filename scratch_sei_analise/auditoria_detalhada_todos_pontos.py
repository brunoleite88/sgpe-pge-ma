import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def q(sql):
    return pd.read_sql_query(sql, conn)

print("="*70)
print("AUDITORIA CIRÚRGICA DE HERANÇAS INDEVIDAS")
print("="*70)

# A. Verificar Eixo 8 em detalhes
print("\n--- A. EIXO 8: ANÁLISE POR UNIDADE ---")
df_a = q("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, responsaveis
FROM acoes 
WHERE eixo LIKE '%8%' 
ORDER BY sigla_unidade, kr_codigo, ordem
""")
for unit, grp in df_a.groupby('sigla_unidade'):
    print(f"\n[{unit}] ({len(grp)} ações):")
    for _, r in grp.iterrows():
        print(f"  #{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# B. Verificar Eixo 9.O1 (Infraestrutura física, Clima, Ergonomia, Copas)
print("\n" + "="*70)
print("--- B. EIXO 9.O1: ANÁLISE POR UNIDADE ---")
df_b = q("""
SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao
FROM acoes 
WHERE kr_codigo LIKE 'E9.O1%' 
ORDER BY sigla_unidade, kr_codigo, ordem
""")
for unit, grp in df_b.groupby('sigla_unidade'):
    print(f"\n[{unit}] ({len(grp)} ações):")
    for _, r in grp.iterrows():
        print(f"  #{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")

# C. Verificar PRI e PRT: De onde vieram as 53 ações de cada uma?
print("\n" + "="*70)
print("--- C. ANÁLISE COMPARATIVA DE PRI E PRT VS PGA / PGAAE ---")
df_pri = q("SELECT kr_codigo, ordem, acao, papel_unidade FROM acoes WHERE sigla_unidade = 'PRI' ORDER BY ordem")
df_prt = q("SELECT kr_codigo, ordem, acao, papel_unidade FROM acoes WHERE sigla_unidade = 'PRT' ORDER BY ordem")
print(f"PRI: {len(df_pri)} ações. KRs: {df_pri['kr_codigo'].unique()}")
print(f"PRT: {len(df_prt)} ações. KRs: {df_prt['kr_codigo'].unique()}")

# D. Verificar PGA vs PGAAE em projetos estratégicos e duplicidades
print("\n" + "="*70)
print("--- D. PGA vs PGAAE: AÇÕES COMUNS OU CONFLITOS DE LIDERANÇA ---")
df_pga_pgaae = q("""
SELECT a1.kr_codigo, a1.acao, a1.papel_unidade as papel_pga, a2.papel_unidade as papel_pgaae
FROM acoes a1
JOIN acoes a2 ON a1.acao = a2.acao AND a1.kr_codigo = a2.kr_codigo
WHERE a1.sigla_unidade = 'PGA' AND a2.sigla_unidade = 'PGAAE'
ORDER BY a1.kr_codigo
""")
print(f"Ações com texto idêntico entre PGA e PGAAE: {len(df_pga_pgaae)}")
for _, r in df_pga_pgaae.iterrows():
    print(f"  {r['kr_codigo']} | PGA: {r['papel_pga']} | PGAAE: {r['papel_pgaae']} | {r['acao'][:60]}")

# E. Verificar unidades com papel 'Líder' em KRs sistêmicos
print("\n" + "="*70)
print("--- E. LÍDERES EM KRs SISTÊMICOS QUE PODEM SER HERANÇA INDEVIDA ---")
# KRs tipicamente sistêmicos:
# E2 (Licitações/Contratos sistêmicos)
# E4.O1.KR3 (Ouvidoria)
# E5.O3.KR2 (Reuniões de prevenção)
# E5.O5.KR1 / KR3 (Automação sistêmica / produtividade)
# E5.O6.KR1 (Prazo zero / SPA)
# E5.O7.KR1 / KR2 (Quadro de pessoal)
# E6.O1 (Comunicação)
# E6.O2 (Benchmarking / Parcerias)
# E7.O1 / O2 / O3 / O4 (TI, Inovação, IA sistêmica)
# E8 (Sustentabilidade, Diversidade, Assédio)
# E9.O1 (Clima, Ergonomia, Copas)
# E9.O2 (Capacitação global)
# E9.O3 (Honorários)
