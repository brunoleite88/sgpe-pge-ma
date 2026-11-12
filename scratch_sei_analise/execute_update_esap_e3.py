import sqlite3
import sys
sys.path.insert(0, '.')
from sgpe_app.backend import sync_unit_to_xlsx, exportar_relatorio
from scratch_sei_analise.preparar_github_pages import build_github_pages_bundle

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# 1. Update Action 12656 in ESAP
c.execute("""
    UPDATE acoes 
    SET papel_unidade = 'Coexecutor',
        responsaveis = 'Líder Institucional: Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI); Coexecutores: Escola Superior da Advocacia Pública (ESAP), PGAAE, PGA',
        unidades_parceiras = 'PGARI,PGAAE,PGA'
    WHERE id = 12656
""")

conn.commit()
print(f"[OK] Ação 12656 da ESAP atualizada para Coexecutor (linhas afetadas: {c.rowcount})")

# Verificar status das 5 ações da ESAP em E3.O1.KR1
c.execute("""
    SELECT id, ordem, acao, papel_unidade, responsaveis 
    FROM acoes 
    WHERE sigla_unidade = 'ESAP' AND kr_codigo = 'E3.O1.KR1'
    ORDER BY ordem
""")
for r in c.fetchall():
    print(f"  - ID {r[0]} | #{r[1]} | Papel: {r[3]} | {r[2]}")

conn.close()

# 2. Sincronizar planilha da ESAP
print("\nSincronizando planilha da ESAP...")
sync_unit_to_xlsx('ESAP')
print("  [OK] Planilha ESAP sincronizada com sucesso")

# 3. Exportar Quadro de Metas da ESAP e Consolidado Geral
print("\nRegenerando arquivos de Quadro de Metas...")
for fmt in ['md', 'docx', 'xlsx']:
    exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla='ESAP')
    print(f"  [OK] Quadro_Eixos_Objetivos_Metas_ESAP.{fmt} gerado")

for fmt in ['md', 'docx', 'xlsx']:
    exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla=None)
    print(f"  [OK] Quadro_Eixos_Objetivos_Metas_Consolidado_Geral.{fmt} gerado")

# 4. Reconstruir bundle do GitHub Pages
print("\nReconstruindo bundle do GitHub Pages...")
build_github_pages_bundle()

# 5. Verificação nos arquivos gerados
print("\n--- VERIFICAÇÃO FINAL ---")
with open('docs/exports/Quadro_Eixos_Objetivos_Metas_ESAP.md', 'r', encoding='utf-8') as f:
    text_esap = f.read()

print("E3.O1.KR1 ainda consta no Quadro de Metas da ESAP?", "E3.O1.KR1" in text_esap)
print("Quadro de Metas da ESAP (linhas com KR):")
for l in text_esap.split('\n'):
    if '| `E' in l:
        print(" ", l[:100])

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade = 'ESAP'")
total_esap = c.fetchone()[0]
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade = 'ESAP' AND kr_codigo = 'E3.O1.KR1'")
total_esap_e3 = c.fetchone()[0]
print(f"\nTotal de ações da ESAP no banco: {total_esap}")
print(f"Total de ações da ESAP em E3.O1.KR1 preservadas: {total_esap_e3}")
conn.close()
