import sys
sys.path.insert(0, '.')
from sgpe_app.backend import init_db_and_sync_from_xlsx, get_conn

print("Sincronizando banco SQLite com as 41 planilhas padronizadas...")
init_db_and_sync_from_xlsx(force_reset_gts=False)

conn = get_conn()
c = conn.cursor()
c.execute("SELECT count(*) FROM acoes")
print("Total ações no banco:", c.fetchone()[0])

print("\n--- DISTRIBUIÇÃO DOS EIXOS PADRONIZADOS NO BANCO ---")
c.execute("SELECT eixo, count(*) FROM acoes GROUP BY eixo ORDER BY eixo")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]} ações")

print("\n--- OBJETIVO DO EIXO 4 ---")
c.execute("SELECT DISTINCT objetivo FROM acoes WHERE kr_codigo LIKE 'E4%'")
for r in c.fetchall():
    print(f"  {r[0]}")
