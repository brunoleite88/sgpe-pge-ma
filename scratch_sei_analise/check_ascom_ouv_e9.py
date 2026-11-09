import sqlite3
conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("SELECT sigla_unidade, acao, responsaveis, papel_unidade FROM acoes WHERE kr_codigo = 'E9.O2.KR1' AND sigla_unidade IN ('ASCOM', 'OUV')")
for r in c.fetchall():
    print(r)
