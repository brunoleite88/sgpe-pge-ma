import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
df = pd.read_sql_query("SELECT ordem, kr_codigo, papel_unidade, acao, subacao FROM acoes WHERE sigla_unidade = 'PJEFP' AND kr_codigo LIKE 'E7%'", conn)
for _, r in df.iterrows():
    print(r.to_dict())
