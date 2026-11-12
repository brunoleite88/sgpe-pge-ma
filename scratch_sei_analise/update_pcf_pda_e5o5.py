import sqlite3
import sys
from pathlib import Path
sys.path.insert(0, '.')
from sgpe_app.backend import sync_unit_to_xlsx, exportar_relatorio, BASE_DIR, APP_DIR

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# 1. Update PCF actions
pcf_updates = [
    (12852, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA; Execução Setorial: Procuradoria do Contencioso Fiscal (PCF); Apoio de Infraestrutura: SI'),
    (12853, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA; Execução Setorial: Procuradoria do Contencioso Fiscal (PCF); Apoio Metodológico: Assessoria de Gestão Estratégica'),
    (12857, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA (Governança Processual: SGA/PGAAJ); Execução Setorial: Procuradoria do Contencioso Fiscal (PCF); Apoio: Assessoria de Gestão Estratégica')
]

for aid, papel, resp in pcf_updates:
    c.execute("UPDATE acoes SET papel_unidade = ?, responsaveis = ? WHERE id = ?", (papel, resp, aid))
    print(f"[OK] PCF Ação {aid} atualizada para {papel}")

# 2. Update PDA actions
pda_updates = [
    (12909, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA; Execução Cartorária e Mapeamento: Procuradoria da Dívida Ativa (PDA); Apoio Técnico: NIRF, SI'),
    (12910, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA; Execução Setorial: Procuradoria da Dívida Ativa (PDA); Apoio de Infraestrutura: SI'),
    (12912, 'Apoio Operacional', 'Líder Institucional: PGAAE / INOVA (Governança Processual: SGA/PGAAJ); Execução Setorial: Procuradoria da Dívida Ativa (PDA)')
]

for aid, papel, resp in pda_updates:
    c.execute("UPDATE acoes SET papel_unidade = ?, responsaveis = ? WHERE id = ?", (papel, resp, aid))
    print(f"[OK] PDA Ação {aid} atualizada para {papel}")

conn.commit()
conn.close()

# 3. Sincronizar planilhas XLSX das duas unidades
print("\nSincronizando planilhas XLSX...")
sync_unit_to_xlsx('PCF')
print("  [OK] PCF sincronizada")
sync_unit_to_xlsx('PDA')
print("  [OK] PDA sincronizada")

# 4. Regenerar exportações de Quadro de Metas para PCF e PDA
print("\nRegenerando arquivos de Quadro de Metas...")
for sigla in ['PCF', 'PDA']:
    for fmt in ['md', 'docx', 'xlsx']:
        res = exportar_relatorio(tipo='quadro-metas-unidade', fmt=fmt, sigla=sigla)
        print(f"  [OK] Quadro_Eixos_Objetivos_Metas_{sigla}.{fmt} gerado")

print("\nProcesso concluído com sucesso!")
