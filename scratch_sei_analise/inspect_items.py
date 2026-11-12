import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== ACOES E5.O6.KR1 ===")
c.execute('SELECT id, sigla_unidade, kr_codigo, acao, subacao FROM acoes WHERE kr_codigo = "E5.O6.KR1"')
rows1 = c.fetchall()
for r in rows1:
    print(f"[{r[0]}] {r[1]} | {r[3]} | {r[4]}")

print(f"\nTotal acoes com E5.O6.KR1: {len(rows1)}")

print("\n=== ACOES SI & PGAAE E7.O2.KR2 ===")
c.execute('SELECT id, sigla_unidade, kr_codigo, acao, subacao FROM acoes WHERE sigla_unidade IN ("SI", "PGAAE") AND kr_codigo = "E7.O2.KR2"')
rows2 = c.fetchall()
for r in rows2:
    print(f"[{r[0]}] {r[1]} | {r[3]} | {r[4]}")
