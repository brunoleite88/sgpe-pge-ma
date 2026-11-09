import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== AÇÕES COM E7.O3.KR2 ===")
c.execute("""
    SELECT sigla_unidade, ordem, papel_unidade, acao, subacao 
    FROM acoes 
    WHERE kr_codigo = 'E7.O3.KR2'
    ORDER BY sigla_unidade, ordem
""")
rows = c.fetchall()
print(f"Total de ações sob E7.O3.KR2: {len(rows)}")
for r in rows:
    print(f"[{r[0]}] #{r[1]} ({r[2]}): {r[3]} | {r[4]}")
