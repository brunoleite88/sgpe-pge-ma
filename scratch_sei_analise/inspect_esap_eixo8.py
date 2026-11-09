import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== TODAS AS AÇÕES DA ESAP NO EIXO 8 ===")
c.execute("""
    SELECT ordem, kr_codigo, kr_texto_completo, acao, subacao, responsaveis, papel_unidade 
    FROM acoes 
    WHERE sigla_unidade = 'ESAP' AND (eixo LIKE '%8%' OR kr_codigo LIKE '%E8%')
    ORDER BY ordem
""")
rows = c.fetchall()
print(f"Total de ações da ESAP no Eixo 8: {len(rows)}")
for r in rows:
    print(f"\n[Ordem #{r[0]}] KR: {r[1]} ({r[6]})\nKR Completo: {r[2]}\nAção: {r[3]}\nSubação: {r[4]}\nResponsáveis: {r[5]}")
