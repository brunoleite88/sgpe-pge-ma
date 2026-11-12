import sqlite3
import sys
sys.path.insert(0, '.')
from sgpe_app.backend import sync_unit_to_xlsx, exportar_relatorio
from scratch_sei_analise.preparar_github_pages import build_github_pages_bundle

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# 1. Atualizar textos dos KRs globais
novos_textos_kr = {
    'E1.O2.KR2': '[E1.O2.KR2] KR2: Tornar o ajuizamento de execuções fiscais 100% estratégico e condicionado a critérios de recuperabilidade até 2027',
    'E1.O5.KR1': '[E1.O5.KR1] KR1: Realizar pesquisa patrimonial sistematizada em 100% das execuções fiscais prioritárias de grandes devedores até 2028',
    'E1.O2.KR3': '[E1.O2.KR3] KR3: Encaminhar a protesto extrajudicial 100% das CDAs triadas e aptas na política de ajuizamento até 2028',
    'E1.O4.KR3': '[E1.O4.KR3] KR3: Submeter 100% das CDAs de grande valor à triagem pré-ajuizamento com a SEFAZ para expurgo de inconsistências e prevenção de sucumbência até 2027'
}

for krc, txt in novos_textos_kr.items():
    c.execute("UPDATE acoes SET kr_texto_completo = ? WHERE kr_codigo = ?", (txt, krc))
    print(f"[OK] KR {krc} atualizado para: {txt} ({c.rowcount} acoes afetadas)")

# 2. Ajustes específicos na PDA para remover E5.O1.KR3 e E1.O1.KR1 do seu Quadro de Metas
# Ação 12906 em E5.O1.KR3 passa para Apoio Operacional
c.execute("""
    UPDATE acoes 
    SET papel_unidade = 'Apoio Operacional',
        responsaveis = 'Líder Institucional: SGA / PGAAJ; Execução Setorial: Procuradoria da Dívida Ativa (PDA)'
    WHERE id = 12906
""")
print(f"[OK] PDA Ação 12906 (E5.O1.KR3) reclassificada para Apoio Operacional (afetadas: {c.rowcount})")

# Ação 12868 em E1.O1.KR1 passa para Apoio Operacional (matéria de precatórios/RPVs da PERJP)
c.execute("""
    UPDATE acoes 
    SET papel_unidade = 'Apoio Operacional',
        responsaveis = 'Líder Institucional: PERJP / NC; Apoio em Execuções Fiscais: Procuradoria da Dívida Ativa (PDA)'
    WHERE id = 12868
""")
print(f"[OK] PDA Ação 12868 (E1.O1.KR1) reclassificada para Apoio Operacional (afetadas: {c.rowcount})")

conn.commit()
conn.close()

# 3. Sincronizar planilhas XLSX das unidades afetadas
unidades_afetadas = ['PDA', 'NIRF', 'PGAAE']
print(f"\nSincronizando planilhas XLSX de {unidades_afetadas}...")
for sigla in unidades_afetadas:
    sync_unit_to_xlsx(sigla)
    print(f"  [OK] Planilha {sigla} sincronizada com sucesso")

# 4. Exportar Quadro de Metas das 3 unidades e Consolidado Geral
print("\nRegenerando arquivos de Quadro de Metas...")
for sigla in unidades_afetadas:
    for fmt in ['md', 'docx', 'xlsx']:
        exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla=sigla)
        print(f"  [OK] Quadro_Eixos_Objetivos_Metas_{sigla}.{fmt} gerado")

for fmt in ['md', 'docx', 'xlsx']:
    exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla=None)
    print(f"  [OK] Quadro_Eixos_Objetivos_Metas_Consolidado_Geral.{fmt} gerado")

# 5. Reconstruir bundle do GitHub Pages
print("\nReconstruindo bundle do GitHub Pages...")
build_github_pages_bundle()

# 6. Verificações nos arquivos gerados
print("\n--- VERIFICAÇÃO FINAL ---")
with open('docs/exports/Quadro_Eixos_Objetivos_Metas_PDA.md', 'r', encoding='utf-8') as f:
    text_pda = f.read()

print("E5.O1.KR3 consta no Quadro de Metas da PDA?", "E5.O1.KR3" in text_pda)
print("E1.O1.KR1 consta no Quadro de Metas da PDA?", "E1.O1.KR1" in text_pda)
print("Novo E1.O2.KR2 consta no Quadro da PDA?", "Tornar o ajuizamento de execuções fiscais 100% estratégico" in text_pda)
print("Novo E1.O5.KR1 consta no Quadro da PDA?", "Realizar pesquisa patrimonial sistematizada em 100%" in text_pda)
print("Novo E1.O2.KR3 consta no Quadro da PDA?", "Encaminhar a protesto extrajudicial 100%" in text_pda)
print("Novo E1.O4.KR3 consta no Quadro da PDA?", "Submeter 100% das CDAs de grande valor" in text_pda)

print("\nVerificando permanência de E5.O1.KR3 nas outras especializadas (ex: PJ)...")
with open('docs/exports/Quadro_Eixos_Objetivos_Metas_PJ.md', 'r', encoding='utf-8') as f:
    text_pj = f.read()
print("E5.O1.KR3 permanece intacta no Quadro da PJ?", "E5.O1.KR3" in text_pj and "Atingir taxa de êxito de 80%" in text_pj)

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()
c.execute("SELECT count(*) FROM acoes WHERE sigla_unidade = 'PDA'")
print(f"\nTotal de ações da PDA preservadas no banco: {c.fetchone()[0]}")
conn.close()
