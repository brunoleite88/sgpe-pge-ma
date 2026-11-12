import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("""
    SELECT id, ordem, kr_codigo, acao, subacao, responsaveis, prazo, papel_unidade, unidades_parceiras
    FROM acoes WHERE sigla_unidade = 'SI' ORDER BY ordem
""")
rows = c.fetchall()
print(f"Total acoes SI: {len(rows)}")
for r in rows:
    print(f"#{r[1]} (ID {r[0]}) | {r[2]} | {r[3][:60]}")
