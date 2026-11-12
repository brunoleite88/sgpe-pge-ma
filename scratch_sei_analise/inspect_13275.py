import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute('SELECT id, sigla_unidade, acao, subacao FROM acoes WHERE id = 13275')
r = c.fetchone()
print(f"ID {r[0]} [{r[1]}]:\nACAO: {r[2]}\nSUBAÇÃO: {r[3]}")
