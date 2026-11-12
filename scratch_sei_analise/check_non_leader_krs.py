import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("""
    SELECT sigla_unidade, kr_codigo, 
           SUM(CASE WHEN papel_unidade = 'Líder' THEN 1 ELSE 0 END) as qtd_lider,
           SUM(CASE WHEN papel_unidade != 'Líder' THEN 1 ELSE 0 END) as qtd_apoio
    FROM acoes
    WHERE kr_codigo != 'SEM_CODIGO'
    GROUP BY sigla_unidade, kr_codigo
    HAVING qtd_lider = 0
    ORDER BY sigla_unidade, kr_codigo
""")
rows = c.fetchall()
print(f"Total de pares (unidade, KR) onde a unidade NÃO é Líder: {len(rows)}")
for r in rows[:25]:
    print(f"[{r[0]}] {r[1]} -> Lider: {r[2]}, Apoio: {r[3]}")
