import sqlite3
import json

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# Let's inspect specialized units in E5.O6.KR1
specialized_units = ['PA', 'PB', 'PCF', 'PDA', 'PEDU', 'PERJP', 'PJ', 'PJEFP', 'PPIMA', 'PRI', 'PRT', 'PSAU', 'PSP', 'PT', 'SDD', 'NCIA', 'SGA', 'PGAAE']

print("=== CHECKING UNITS IN E5.O6.KR1 ===")
for u in specialized_units:
    c.execute("SELECT id, acao, subacao FROM acoes WHERE sigla_unidade = ? AND kr_codigo = 'E5.O6.KR1'", (u,))
    rows = c.fetchall()
    print(f"[{u}] has {len(rows)} actions in E5.O6.KR1")
    for r in rows:
        print(f"   - ID {r[0]}: {r[1]}")
