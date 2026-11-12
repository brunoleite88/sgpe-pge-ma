import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("SELECT sigla, nome, responsavel, status_reuniao, notas_reuniao FROM unidades WHERE sigla IN ('PCF', 'PDA')")
for r in c.fetchall():
    print(f"[{r[0]}] {r[1]}")
    print(f"  Responsável: {r[2]}")
    print(f"  Status: {r[3]}")
    print(f"  Notas: {r[4][:150] if r[4] else None}")
