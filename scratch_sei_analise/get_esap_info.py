import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("SELECT sigla, nome, responsavel, status_reuniao FROM unidades WHERE sigla = 'ESAP'")
print(c.fetchone())
