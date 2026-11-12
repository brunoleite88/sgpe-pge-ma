import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("""
    SELECT id, sigla_unidade, ordem, acao, subacao, responsaveis, prazo, pilar_3ps, papel_unidade, unidades_parceiras, status_execucao
    FROM acoes 
    WHERE sigla_unidade IN ('SI', 'PGAAE') AND kr_codigo = 'E7.O2.KR2'
    ORDER BY sigla_unidade, ordem
""")
rows = c.fetchall()
for r in rows:
    print(f"ID {r[0]} | {r[1]} #{r[2]} | {r[3]}\n   Sub: {r[4]}\n   Resp: {r[5]} | Prazo: {r[6]} | 3Ps: {r[7]} | Papel: {r[8]} | Parc: {r[9]}\n")
