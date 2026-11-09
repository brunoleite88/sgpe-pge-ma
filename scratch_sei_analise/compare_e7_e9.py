import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("""
    SELECT a.sigla_unidade, a.ordem, a.acao, a.subacao, a.papel_unidade
    FROM acoes a
    WHERE a.kr_codigo = 'E7.O3.KR2'
    ORDER BY a.sigla_unidade, a.ordem
""")
e7_actions = c.fetchall()

print(f"Total ações em E7.O3.KR2: {len(e7_actions)}")
for sigla, ordem, acao, subacao, papel in e7_actions:
    c.execute("""
        SELECT ordem, acao, subacao, papel_unidade 
        FROM acoes 
        WHERE sigla_unidade = ? AND kr_codigo = 'E9.O2.KR1'
    """, (sigla,))
    e9_actions = c.fetchall()
    has_e9 = len(e9_actions)
    print(f"[{sigla}] E7:#{ordem} '{acao[:50]}' | Tem E9.O2.KR1? {has_e9} ação(ões)")
    for o_e9, a_e9, s_e9, p_e9 in e9_actions:
        print(f"   -> E9:#{o_e9} ({p_e9}) '{a_e9[:50]}'")
