import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

def check_lideres(kr):
    c.execute("SELECT DISTINCT sigla_unidade FROM acoes WHERE kr_codigo = ? AND papel_unidade = 'Líder'", (kr,))
    return [r[0] for r in c.fetchall()]

print("E7.O3.KR1 (Projetos Estratégicos):", check_lideres("E7.O3.KR1"))
print("E9.O3.KR1 (Honorários Sucumbenciais):", check_lideres("E9.O3.KR1"))
print("E6.O1.KR2 (Redes Sociais):", check_lideres("E6.O1.KR2"))
print("E5.O2.KR2 (Tribunais Superiores):", check_lideres("E5.O2.KR2"))
print("E9.O2.KR1 (Capacitação Institucional):", check_lideres("E9.O2.KR1"))
print("E7.O3.KR2 (Meta antiga de IA - deve ser vazio):", check_lideres("E7.O3.KR2"))

c.execute("SELECT count(*) FROM acoes WHERE kr_codigo = 'E7.O3.KR2'")
print("Total de ações com E7.O3.KR2 em qualquer papel:", c.fetchone()[0])
