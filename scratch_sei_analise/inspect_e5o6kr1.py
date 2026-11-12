import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute('SELECT id, sigla_unidade, acao, subacao FROM acoes WHERE kr_codigo = "E5.O6.KR1"')
rows = c.fetchall()
for r in rows:
    print(f"[{r[0]}] {r[1]} | {r[2]}")
print(f"Total: {len(rows)}")
