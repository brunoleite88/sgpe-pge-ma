import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("""
    SELECT DISTINCT kr_codigo, kr_texto_completo, sigla_unidade, papel_unidade 
    FROM acoes 
    WHERE kr_texto_completo LIKE '%direito digital%' 
       OR kr_texto_completo LIKE '%inteligência artificial%' 
       OR kr_texto_completo LIKE '%capacita%' 
       OR acao LIKE '%direito digital%'
       OR acao LIKE '%inteligência artificial%'
    ORDER BY kr_codigo, sigla_unidade
""")
rows = c.fetchall()
print(f"Total encontrados: {len(rows)}")
for r in rows:
    print(r)
