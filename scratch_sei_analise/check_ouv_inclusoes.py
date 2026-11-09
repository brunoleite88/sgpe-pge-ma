import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

print("=== AÇÕES DA OUVIDORIA NO BANCO ===")
c.execute("SELECT ordem, kr_codigo, acao, papel_unidade FROM acoes WHERE sigla_unidade = 'OUV' ORDER BY ordem")
for r in c.fetchall():
    print(r)

print("\n=== BUSCA POR 'escuta ativa' OU 'comunicação não violenta' OU 'cnv' NO BANCO ===")
c.execute("SELECT sigla_unidade, kr_codigo, acao, subacao FROM acoes WHERE acao LIKE '%escuta ativa%' OR acao LIKE '%comunicação não violenta%' OR acao LIKE '%cnv%' OR subacao LIKE '%escuta ativa%' OR subacao LIKE '%comunicação não violenta%' OR subacao LIKE '%cnv%'")
for r in c.fetchall():
    print(r)

print("\n=== BUSCA POR 'cartilha' NO BANCO ===")
c.execute("SELECT sigla_unidade, kr_codigo, acao, subacao FROM acoes WHERE acao LIKE '%cartilha%' OR subacao LIKE '%cartilha%'")
for r in c.fetchall():
    print(r)
