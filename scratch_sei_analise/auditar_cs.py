import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

# All units
c = conn.cursor()
c.execute("SELECT DISTINCT sigla_unidade FROM acoes ORDER BY sigla_unidade")
unidades = [r[0] for r in c.fetchall()]
print(f"Total unidades: {len(unidades)}")
print(unidades)

# Actions of CS
print("\n--- AÇÕES DO CONSELHO SUPERIOR (CS) ---")
df_cs = pd.read_sql_query("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'CS' ORDER BY ordem", conn)
for _, r in df_cs.iterrows():
    print(f"#{r['ordem']} | {r['kr_codigo']} | {r['papel_unidade']} | {r['acao']}")
    print(f"   Subação: {r['subacao']}\n")
