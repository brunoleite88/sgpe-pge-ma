import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

for sigla in ['PB', 'PJ', 'PJEFP', 'PGAAE', 'SGRH', 'SI']:
    print(f"=== {sigla} ===")
    c.execute("SELECT ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade = ? ORDER BY ordem", (sigla,))
    for r in c.fetchall():
        print(f"  #{r[0]} [{r[1]}] ({r[3]}): {r[2]}")
