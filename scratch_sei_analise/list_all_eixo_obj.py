import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
df = pd.read_sql_query("SELECT DISTINCT eixo, objetivo FROM acoes ORDER BY eixo, objetivo", conn)
for _, r in df.iterrows():
    print(f"[{r['eixo']}] -> [{r['objetivo']}]")
