import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
cursor = conn.cursor()

print('=== ACOES DA SI ===')
cursor.execute('SELECT kr_codigo, acao, subacao, prazo FROM acoes WHERE sigla_unidade = ?', ('SI',))
for r in cursor.fetchall():
    print(f'{r[0]} | {r[1]} | {r[2]} | {r[3]}')

print('\n=== ACOES DA PGAAE ===')
cursor.execute('SELECT kr_codigo, acao, subacao, prazo FROM acoes WHERE sigla_unidade = ?', ('PGAAE',))
for r in cursor.fetchall():
    print(f'{r[0]} | {r[1]} | {r[2]} | {r[3]}')
