import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("SELECT count(id) FROM acoes WHERE kr_codigo IS NULL OR kr_codigo = ''")
print("Rows without kr_codigo:", c.fetchone()[0])

c.execute("SELECT DISTINCT substr(kr_codigo, 1, 2) FROM acoes")
print("Prefixes of kr_codigo:", [r[0] for r in c.fetchall()])
