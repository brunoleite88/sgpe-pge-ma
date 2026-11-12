import sqlite3

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

ids_d3 = [13497, 13498, 13181, 13275, 12803, 12859, 12914, 12939, 12968, 13291, 13313, 13352, 13388, 13399, 13419, 13450, 12738, 13483]
ids_infra = [13571, 13210, 13213]

print("=== CURRENT D-3 TARGET ACTIONS ===")
for aid in ids_d3:
    c.execute("SELECT sigla_unidade, acao, subacao FROM acoes WHERE id = ?", (aid,))
    r = c.fetchone()
    if r:
        print(f"[{aid}] {r[0]}: {r[1]}")
        print(f"     Sub: {r[2]}")

print("\n=== CURRENT INFRA/CRISE TARGET ACTIONS ===")
for aid in ids_infra:
    c.execute("SELECT sigla_unidade, acao, subacao FROM acoes WHERE id = ?", (aid,))
    r = c.fetchone()
    if r:
        print(f"[{aid}] {r[0]}: {r[1]}")
        print(f"     Sub: {r[2]}")
