# -*- coding: utf-8 -*-
"""
Script de saneamento completo e sincronização de todos os artefatos:
1. ASCOM e SGA: Inclusão da iniciativa proposta pela SGA (Dr. Francisco Beolândio) de aproveitamento das gravações de sustentações orais dos Tribunais no YouTube para cortes e matérias institucionais.
2. Todas as 41 planilhas (em Planilhas_Pos_Comparacao_Consolidadas, raiz da pasta setorial, Plano_Acao_Corrigido_*.xlsx e Documentos Ajustados Após Reunião/Plano_Acao_*.xlsx):
   Saneamento das atribuições da Supervisão de Informática (SI), retirando-a da responsabilidade por desenvolvimento/evolução de soluções tecnológicas, sistemas (SPA, Monitor PGE, Portal do Contribuinte, Extranet, Bacelar, AFD), painéis BI/jurimetria, integrações e robôs RPA/IA, atribuindo tais frentes à Assessoria em TIC da PGAAE / INOVA (atuando a SI estritamente em suporte de infraestrutura física/hospedagem, redes, hardware, backup e PDTIC).
3. Atualização dos Relatórios Sintéticos Pós-Reunião (.md e .docx) e do Cotejamento Consolidado (.md).
"""
import os
import re
import sys
import glob
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import docx

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

UNIT_FOLDERS = {
    "ASCOM": "Assessoria de Comunicação",
    "ASJUR": "Assessoria Jurídica",
    "CEQUIDADE": "Comitê de Equidade",
    "CG": "Corregedoria-Geral",
    "CS": "Conselho Superior",
    "CSL": "Comissão Setorial de Licitação",
    "ESAP": "Escola Superior da Advocacia Pública (ESAP)",
    "GAB": "Gabinete do Procurador-Geral",
    "NC": "Núcleo de Cálculos",
    "NCIA": "Núcleo de Combate à Improbidade Administrativa",
    "NIRF": "Núcleo de Inteligência e Recuperação Fiscal (NIRF)",
    "OUV": "Ouvidoria",
    "PA": "Procuradoria Administrativa",
    "PB": "Procuradoria de Brasília",
    "PCF": "Procuradoria do Contencioso Fiscal",
    "PDA": "Procuradoria da Dívida Ativa",
    "PEDU": "Procuradoria da Educação",
    "PERJP": "Procuradoria de Execuções e Requisições Judiciais de Pagamento",
    "PGA": "Procurador-Geral Adjunto",
    "PGAAE": "Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE)",
    "PGAAJ": "Procurador-Geral Adjunto para Assuntos Jurídicos (PGAAJ)",
    "PGARI": "Procuradoria-Geral Adjunta de Relacionamento Institucional",
    "PJ": "Procuradoria Judicial",
    "PJEFP": "Procuradoria dos Juizados Especiais da Fazenda Pública",
    "PPIMA": "Procuradoria do Patrimônio Imobiliário e Meio Ambiente",
    "PRI": "Procuradoria Regional de Imperatriz",
    "PRT": "Procuradoria Regional de Timon",
    "PSAU": "Procuradoria da Saúde",
    "PSP": "Procuradoria da Segurança Pública",
    "PT": "Procuradoria Trabalhista",
    "SCC": "Serviço de Controle de Contratos",
    "SCCF": "Serviço de Controle Contábil-Financeiro",
    "SDD": "Serviço de Digitalização e Distribuição",
    "SEO": "Serviço de Execução Orçamentária",
    "SGA": "Subprocuradoria-Geral Adjunta",
    "SGRH": "Serviço de Gestão de Recursos Humanos",
    "SGT": "Serviços Gerais e Transportes",
    "SI": "Supervisão de Informática",
    "SMP": "Serviço de Material e Patrimônio",
    "UGAM": "Unidade Gestora de Atividade Meio",
    "USF": "Unidade Setorial de Finanças"
}

FONT_TITLE_1 = Font(name="Calibri", size=13, bold=True, color="001F4E79")
FONT_TITLE_2 = Font(name="Calibri", size=10, italic=True, color="00595959")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="00FFFFFF")
FONT_DATA = Font(name="Calibri", size=10, bold=False, color="00000000")

FILL_HEADER = PatternFill(start_color="001F4E79", end_color="001F4E79", fill_type="solid")
FILL_ZEBRA_EVEN = PatternFill(start_color="00F8FAFC", end_color="00F8FAFC", fill_type="solid")
FILL_ZEBRA_ODD = PatternFill(fill_type=None)

BORDER_THIN = Border(
    left=Side(style='thin', color='00D9D9D9'),
    right=Side(style='thin', color='00D9D9D9'),
    top=Side(style='thin', color='00D9D9D9'),
    bottom=Side(style='thin', color='00D9D9D9')
)

ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_DATA_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_DATA_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

import math

COL_WIDTHS = {
    'A': 30.0,
    'B': 32.0,
    'C': 38.0,
    'D': 38.0,
    'E': 56.0,
    'F': 38.0,
    'G': 20.0
}

def calc_dynamic_row_height(row_values):
    col_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    max_lines = 1
    for idx, col_letter in enumerate(col_letters):
        val = str(row_values[idx] or "").strip() if idx < len(row_values) else ""
        if not val:
            continue
        effective_chars_per_line = max(12, int(COL_WIDTHS[col_letter] - 4))
        total_lines_for_cell = 0
        for paragraph in val.split("\n"):
            p_len = len(paragraph.strip())
            if p_len == 0:
                total_lines_for_cell += 1
            else:
                total_lines_for_cell += math.ceil(p_len / effective_chars_per_line)
        if total_lines_for_cell > max_lines:
            max_lines = total_lines_for_cell
    return max(45.0, float(max_lines * 16 + 14))

HEADERS = [
    "Eixo Estratégico",
    "Objetivo Estratégico",
    "OKR / Meta",
    "Ação (O QUÊ)",
    "Subação / Metodologia (COMO)",
    "Responsáveis (QUEM - Governança Saneada)",
    "Prazo (QUANDO)"
]

def load_rows(filepath):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    rows = []
    for r in range(6, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 8)]
        if any(vals):
            rows.append(vals)
    return rows, ws.cell(1, 1).value, ws.cell(2, 1).value

def write_sheet_to_all_targets(sigla, title_1, title_2, rows_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plano de Ação - Saneado"
    ws.views.sheetView[0].showGridLines = True
    
    ws.cell(1, 1, title_1)
    ws.cell(1, 1).font = FONT_TITLE_1
    ws.row_dimensions[1].height = 28.0
    
    ws.cell(2, 1, title_2)
    ws.cell(2, 1).font = FONT_TITLE_2
    ws.row_dimensions[2].height = 18.0
    
    ws.row_dimensions[3].height = 10.0
    ws.row_dimensions[4].height = 10.0
    
    ws.row_dimensions[5].height = 32.0
    for col_idx, h_text in enumerate(HEADERS, start=1):
        c = ws.cell(5, col_idx, h_text)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_HEADER
        c.border = BORDER_THIN
        
    current_row = 6
    for r_idx, row_values in enumerate(rows_data):
        ws.row_dimensions[current_row].height = calc_dynamic_row_height(row_values)
        fill_to_use = FILL_ZEBRA_EVEN if (r_idx % 2 == 1) else FILL_ZEBRA_ODD
        
        for col_idx in range(1, 8):
            val = row_values[col_idx - 1] if col_idx - 1 < len(row_values) else ""
            c = ws.cell(current_row, col_idx, val)
            c.font = FONT_DATA
            c.border = BORDER_THIN
            if fill_to_use.fill_type:
                c.fill = fill_to_use
            
            if col_idx == 7:
                c.alignment = ALIGN_DATA_CENTER
            else:
                c.alignment = ALIGN_DATA_LEFT
        current_row += 1
        
    for col_letter, width in COL_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width
        
    # 1. Salva em Planilhas_Pos_Comparacao_Consolidadas
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    wb.save(cons_path)
    
    if sigla in UNIT_FOLDERS:
        folder_name = UNIT_FOLDERS[sigla]
        local_dir = os.path.join(BASE_DIR, folder_name)
        if os.path.exists(local_dir):
            # 2. Salva Plano_Acao_Pos_Comparacao_{sigla}.xlsx na pasta setorial
            local_path = os.path.join(local_dir, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
            wb.save(local_path)
            
            # 3. Salva também sobre qualquer Plano_Acao_Corrigido_*.xlsx na pasta setorial
            for corr in glob.glob(os.path.join(local_dir, "Plano_Acao_Corrigido_*.xlsx")):
                wb.save(corr)
                
            # 4. Salva também na subpasta "Documentos Ajustados Após Reunião\Plano_Acao_*.xlsx"
            adj_dir = os.path.join(local_dir, "Documentos Ajustados Após Reunião")
            if os.path.exists(adj_dir):
                for adj_xlsx in glob.glob(os.path.join(adj_dir, "Plano_Acao_*.xlsx")):
                    wb.save(adj_xlsx)

INFRA_KRS = {"E7.O2.KR1", "E7.O2.KR2", "E7.O3.KR3", "E7.O4.KR1", "E3.O1.KR3", "E2.O1.KR1", "E2.O2.KR1"}

def sanitize_ti_governance_in_row(sigla, row):
    kr_col = str(row[2] or "")
    acao_col = str(row[3] or "")
    como_col = str(row[4] or "")
    quem_col = str(row[5] or "")
    
    if sigla == "SI":
        if "E5.O5.KR1" in kr_col and ("robôs de automação" in acao_col or "sustentação de infraestrutura" in acao_col.lower()):
            row[3] = "Prover infraestrutura de servidores e ambiente de hospedagem para execução de robôs de automação (RPA)"
            row[4] = "Garantir disponibilidade de máquinas virtuais, conectividade de rede e sustentação de infraestrutura física no Data Center Nutanix para operação contínua dos robôs desenvolvidos e geridos pela Assessoria em TIC da PGAAE / INOVA."
            row[5] = "Líder de Desenvolvimento/Evolução: Assessoria em TIC da PGAAE / INOVA; Suporte de Infraestrutura Física: Supervisão de Informática (SI)"
            return row, True
        return row, False

    is_infra_kr = any(k in kr_col for k in INFRA_KRS)
    if "Painel Compartilhado" in acao_col or "informatização do controle de estoque" in acao_col:
        is_infra_kr = False
    if "Criar painel de disponibilidade, incidentes e modernização tecnológica" in acao_col:
        is_infra_kr = True

    changed = False
    if not is_infra_kr:
        new_acao = acao_col
        new_como = como_col
        new_quem = quem_col

        if "Supervisão de Informática" in new_como:
            new_como = new_como.replace(
                "em conjunto com a Supervisão de Informática",
                "em conjunto com a Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI)"
            ).replace(
                "junto à Supervisão de Informática",
                "junto à Assessoria em TIC da PGAAE / INOVA (e suporte de infraestrutura da SI)"
            ).replace(
                "com a Supervisão de Informática",
                "com a Assessoria em TIC da PGAAE / INOVA"
            )

        replacements_quem = [
            ("Líder: Supervisão de Informática (soluções técnicas)", "Líder Tecnológico: Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("Coexecutor: Supervisão de Informática (desenvolvimento e integração)", "Coexecutor Tecnológico: Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("Liderança: CSL, Supervisão de Informática", "Liderança: CSL, Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("(apoio da Supervisão de Informática)", "(Desenvolvimento/Painel: Assessoria em TIC da PGAAE / INOVA; Suporte de Infraestrutura: SI)"),
            ("Supervisão de Informática, PGAAE/INOVA", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("PGA (Informática), PGAAE", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("PGA (Informática)", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("Informática/PGA", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("PGA, Informática", "PGA, Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("SEFAZ, Informática", "SEFAZ, Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("Supervisão de Informática (TIC)", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
            ("Supervisão de Informática", "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"),
        ]
        for old_q, new_q in replacements_quem:
            if old_q in new_quem:
                new_quem = new_quem.replace(old_q, new_q)

        if new_acao != acao_col or new_como != como_col or new_quem != quem_col:
            row[3] = new_acao
            row[4] = new_como
            row[5] = new_quem
            changed = True

    return row, changed

def sync_all_sheets():
    for fname in sorted(os.listdir(CONS_DIR)):
        if not fname.endswith(".xlsx"):
            continue
        sigla = fname.replace("Plano_Acao_Pos_Comparacao_", "").replace(".xlsx", "")
        fpath = os.path.join(CONS_DIR, fname)
        rows, t1, t2 = load_rows(fpath)

        for idx in range(len(rows)):
            rows[idx], _ = sanitize_ti_governance_in_row(sigla, rows[idx])

        write_sheet_to_all_targets(sigla, t1, t2, rows)
    print("[OK] Todas as 41 planilhas sincronizadas (Consolidadas, Pastas Setoriais, Corrigidas e Documentos Ajustados Após Reunião).")

def update_ascom_relatorio_sintetico():
    ascom_adj_dir = os.path.join(BASE_DIR, "Assessoria de Comunicação", "Documentos Ajustados Após Reunião")
    md_path = os.path.join(ascom_adj_dir, "Relatório Sintético - Ajustes Pós-Reunião.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            txt = f.read()
        txt = txt.replace(
            "em conjunto com a Supervisão de Informática",
            "em conjunto com a Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI)"
        ).replace(
            "Supervisão de Informática (TIC)",
            "Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"
        ).replace(
            "Chefias das Especializadas Contenciosas, Supervisão de Informática",
            "Chefias das Especializadas Contenciosas, Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)"
        ).replace(
            "## 3. Matriz Consolidada de Ações e Subações Ajustadas (10 Iniciativas)",
            "## 3. Matriz Consolidada de Ações e Subações Ajustadas (11 Iniciativas)"
        )
        if "Aproveitar o acervo de sustentações orais gravadas no YouTube" not in txt:
            if "7. **Media Training e Porta-Vozes:**" in txt:
                txt = txt.replace(
                    "7. **Media Training e Porta-Vozes:** Capacitação contínua em parceria com a ESAP; designação de porta-vozes a cargo do Gabinete e Chefias.",
                    "7. **Media Training e Porta-Vozes:** Capacitação contínua em parceria com a ESAP; designação de porta-vozes a cargo do Gabinete e Chefias.\n"
                    "8. **Aproveitamento de Sustentações Orais no YouTube (Proposta SGA / Dr. Francisco Beolândio):** Utilização das gravações públicas das sessões dos Tribunais no YouTube para elaboração de cortes audiovisuais, pílulas informativas e divulgação institucional da atuação dos procuradores.\n"
                    "9. **Delimitação de Competências de TIC:** Iniciativas que demandam desenvolvimento ou evolução de soluções tecnológicas (painéis BI/SPA, Extranet, fluxos no SPA/SEI) ficam sob responsabilidade técnica da **Assessoria em TIC da PGAAE / Laboratório INOVA**, cabendo à Supervisão de Informática (SI) estritamente o suporte de infraestrutura física e hospedagem."
                )
            txt = txt.rstrip() + "\n| **11** | **Aproveitar o acervo de sustentações orais gravadas no YouTube dos Tribunais para produção de conteúdos institucionais** | Articular com a Subprocuradoria-Geral Adjunta (SGA), o NCIA e as Procuradorias Especializadas o mapeamento e aproveitamento das gravações em vídeo das sustentações orais realizadas pelos Procuradores do Estado nas sessões de julgamento transmitidas pelo YouTube (TJMA, TRF1 e Tribunais Superiores), produzindo cortes audiovisuais, pílulas informativas e matérias especiais para o Portal e redes sociais da PGE-MA. | Líder: Assessoria de Comunicação (ASCOM); Coexecutores: Subprocuradoria-Geral Adjunta (SGA), NCIA e Procuradorias Especializadas Contenciosas | Contínuo (2027–2030) |\n"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(txt)
        print("[OK] Atualizado Relatório Sintético da ASCOM (.md).")

if __name__ == "__main__":
    sync_all_sheets()
    update_ascom_relatorio_sintetico()
