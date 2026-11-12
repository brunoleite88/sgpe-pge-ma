import sqlite3
import json

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

c.execute("SELECT count(*) FROM acoes WHERE acao LIKE '%D-3%' OR subacao LIKE '%D-3%'")
print("Acoes com D-3 no banco:", c.fetchone()[0])

c.execute("SELECT count(*) FROM acoes WHERE acao LIKE '%VxRail%' OR subacao LIKE '%VxRail%'")
print("Acoes com VxRail no banco:", c.fetchone()[0])

c.execute("SELECT count(*) FROM acoes WHERE acao LIKE '%Zabbix%' OR subacao LIKE '%Zabbix%'")
print("Acoes com Zabbix no banco:", c.fetchone()[0])

c.execute("SELECT count(*) FROM acoes WHERE acao LIKE '%3 Níveis%' OR subacao LIKE '%3 Níveis%'")
print("Acoes com 3 Níveis no banco:", c.fetchone()[0])

with open('docs/dados_sgpe.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)
print("D-3 no JSON:", json_str.count('D-3'))
print("VxRail no JSON:", json_str.count('VxRail'))
print("Zabbix no JSON:", json_str.count('Zabbix'))
print("3 Níveis no JSON:", json_str.count('3 Níveis'))
