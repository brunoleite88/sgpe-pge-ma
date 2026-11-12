import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

def check(name, term):
    c.execute('SELECT count(*) FROM acoes WHERE acao LIKE ? OR subacao LIKE ?', (f'%{term}%', f'%{term}%'))
    cnt = c.fetchone()[0]
    print(f'{name} ({term}): {cnt}')

check('Zabbix', 'zabbix')
check('D-3', 'D-3')
check('Resolução 58', '58/2026')
check('Coreplan', 'coreplan')
check('AlexandrIA', 'alexandria')
check('Nimbus', 'nimbus')
check('Procuradoria-PDF', 'procuradoria-pdf')
check('Dell VxRail', 'vxrail')
check('Nutanix', 'nutanix')
check('Sala Cofre', 'sala cofre')
check('Comite de Crise', 'crise')
check('Bacelar', 'bacelar')
check('Delay 5 a 7', '5 a 7')
