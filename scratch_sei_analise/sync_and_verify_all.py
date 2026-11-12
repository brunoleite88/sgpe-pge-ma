import sys
sys.path.insert(0, '.')
from sgpe_app.backend import exportar_relatorio
import subprocess

print("Exportando Quadro_Eixos_Objetivos_Metas_Consolidado_Geral...")
for fmt in ['md', 'docx', 'xlsx']:
    exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla=None)
    print(f"  [OK] Consolidado Geral em {fmt} gerado")

print("\nExecutando preparar_github_pages.py...")
from scratch_sei_analise.preparar_github_pages import build_github_pages_bundle
build_github_pages_bundle()

print("\nVerificando remoção de E5.O5 dos arquivos de PCF e PDA em docs/exports/...")
for sigla in ['PCF', 'PDA']:
    with open(f'docs/exports/Quadro_Eixos_Objetivos_Metas_{sigla}.md', 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"  Quadro {sigla}: E5.O5 presente? {'E5.O5' in text}")

print("\nVerificando permanência das 6 ações no banco...")
import sqlite3
conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("""
    SELECT sigla_unidade, kr_codigo, papel_unidade, acao 
    FROM acoes 
    WHERE sigla_unidade IN ('PCF', 'PDA') AND kr_codigo IN ('E5.O5.KR1', 'E5.O5.KR3')
    ORDER BY sigla_unidade, kr_codigo
""")
rows = c.fetchall()
print(f"Total de ações preservadas: {len(rows)}")
for r in rows:
    print(f"  [{r[0]}] {r[1]} ({r[2]}): {r[3]}")
conn.close()
