import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def check(name, query):
    df = pd.read_sql_query(query, conn)
    print(f"\n=== {name} === (total: {len(df)})")
    for _, r in df.iterrows():
        print(f"  {r['kr_codigo'] if 'kr_codigo' in r else ''} | {r['papel_unidade'] if 'papel_unidade' in r else ''} | {r['acao'][:60] if 'acao' in r else ''}")

check("ESAP Eixo 8 e E9.O1", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='ESAP' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%')")
check("ESAP E6.O2.KR1", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='ESAP' AND kr_codigo='E6.O2.KR1'")
check("CS Ações e Papéis", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='CS'")
check("PRI KRs distintos", "SELECT DISTINCT kr_codigo, count(*) as n FROM acoes WHERE sigla_unidade='PRI' GROUP BY kr_codigo")
check("PRT KRs distintos", "SELECT DISTINCT kr_codigo, count(*) as n FROM acoes WHERE sigla_unidade='PRT' GROUP BY kr_codigo")
check("PGA Eixo 8 e E9.O1", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='PGA' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%')")
check("UGAM Eixo 8", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='UGAM' AND eixo LIKE '%8%'")
check("CEQUIDADE E8.O1.KR1", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='CEQUIDADE' AND kr_codigo='E8.O1.KR1'")
check("PJEFP em E7.O2.KR2", "SELECT id, ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade='PJEFP' AND kr_codigo='E7.O2.KR2'")
