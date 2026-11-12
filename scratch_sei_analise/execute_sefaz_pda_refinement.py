import sqlite3
import sys
sys.path.insert(0, '.')
from sgpe_app.backend import sync_unit_to_xlsx, exportar_relatorio
from scratch_sei_analise.preparar_github_pages import build_github_pages_bundle

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# 1. Atualizar textos dos KRs no banco
novos_textos = {
    'E1.O2.KR1': '[E1.O2.KR1] KR1: Operacionalizar a política de Transação Tributária e recuperação qualificada em 100% das carteiras elegíveis da Dívida Ativa até 2028',
    'E1.O3.KR1': '[E1.O3.KR1] KR1: Integrar os serviços de cobrança e negociação fiscal aos canais digitais de atendimento com 80% de resolutividade até 2027',
    'E1.O3.KR2': '[E1.O3.KR2] KR2: Atingir 85% de satisfação dos contribuintes nos canais oficiais de atendimento e negociação fiscal da PGE até 2028',
    'E1.O4.KR1': '[E1.O4.KR1] KR1: Mapear blindagem patrimonial e grupos econômicos em 100% dos grandes devedores fiscais prioritários até 2028',
    'E1.O4.KR2': '[E1.O4.KR2] KR2: Realizar saneamento cadastral e cruzamento de dados com a SEFAZ em 100% dos lotes de grandes devedores até 2028'
}

for krc, txt in novos_textos.items():
    c.execute("UPDATE acoes SET kr_texto_completo = ? WHERE kr_codigo = ?", (txt, krc))
    print(f"[OK] KR {krc} atualizado: {c.rowcount} acoes afetadas")

# 2. Atualizar subação do canal oficial de atendimento da PDA (Ação 12882)
c.execute("""
    UPDATE acoes 
    SET subacao = 'Estruturar o canal oficial de atendimento e negociação fiscal da Dívida Ativa, com formalização de rito procedimental e provimento de infraestrutura material (aparelho, linha telefônica institucional e conectividade custeados pela PGE-MA via UGAM) para cessar o custeio pessoal pelos procuradores.'
    WHERE id = 12882
""")
print(f"[OK] Ação 12882 (Canal Oficial PDA) atualizada (afetadas: {c.rowcount})")

conn.commit()
conn.close()

# 3. Sincronizar planilhas XLSX das unidades afetadas
unidades_afetadas = ['PDA', 'PCF', 'NIRF', 'PGAAE']
print(f"\nSincronizando planilhas XLSX de {unidades_afetadas}...")
for sigla in unidades_afetadas:
    sync_unit_to_xlsx(sigla)
    print(f"  [OK] Planilha {sigla} sincronizada com sucesso")

# 4. Regenerar exportações de Quadro de Metas das 4 unidades e Consolidado Geral
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

print("E1.O2.KR1 atualizado no Quadro da PDA?", "Operacionalizar a política de Transação Tributária" in text_pda)
print("E1.O3.KR1 atualizado no Quadro da PDA?", "Integrar os serviços de cobrança e negociação fiscal" in text_pda)
print("E1.O4.KR1 atualizado no Quadro da PDA?", "Mapear blindagem patrimonial e grupos econômicos" in text_pda)
print("E1.O4.KR2 atualizado no Quadro da PDA?", "Realizar saneamento cadastral e cruzamento de dados com a SEFAZ" in text_pda)
