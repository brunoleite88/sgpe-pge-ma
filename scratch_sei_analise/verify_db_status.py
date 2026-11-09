import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("SELECT count(*) FROM acoes WHERE kr_codigo = 'E7.O3.KR2'")
count_e7 = c.fetchone()[0]
print(f"Total de ações com E7.O3.KR2 no banco: {count_e7}")

c.execute("SELECT count(*) FROM acoes")
total_acoes = c.fetchone()[0]
print(f"Total de ações no banco: {total_acoes}")

c.execute("SELECT acao, subacao, papel_unidade FROM acoes WHERE sigla_unidade = 'ESAP' AND acao LIKE '%Direito Digital e Inteligência Artificial%'")
esap_ia = c.fetchall()
print(f"Ação Prioritária da ESAP em IA: {esap_ia}")

c.execute("SELECT sigla_unidade, acao FROM acoes WHERE kr_codigo = 'E9.O2.KR1' AND papel_unidade = 'Líder'")
lideres_e9 = c.fetchall()
print(f"Líderes de E9.O2.KR1: {lideres_e9}")
