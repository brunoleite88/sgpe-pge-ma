import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== AÇÕES DA ESAP ===")
c.execute("""
    SELECT ordem, eixo, objetivo, kr_codigo, kr_texto_completo, acao, papel_unidade 
    FROM acoes 
    WHERE sigla_unidade = 'ESAP' 
    ORDER BY ordem
""")
for r in c.fetchall():
    print(f"[{r[0]}] {r[3]} ({r[6]}): {r[4]} | AÇÃO: {r[5]}")

print("\n=== TODAS AS METAS (KRs) COM 'DIREITO DIGITAL' OU 'INTELIGÊNCIA ARTIFICIAL' OU 'CAPACITAÇÃO' NO BANCO ===")
c.execute("""
    SELECT DISTINCT kr_codigo, kr_texto_completo 
    FROM acoes 
    WHERE kr_texto_completo LIKE '%direito digital%' 
       OR kr_texto_completo LIKE '%inteligência artificial%' 
       OR kr_texto_completo LIKE '%ia%'
       OR kr_texto_completo LIKE '%capacita%'
    ORDER BY kr_codigo
""")
for r in c.fetchall():
    print(f"{r[0]} -> {r[1]}")
