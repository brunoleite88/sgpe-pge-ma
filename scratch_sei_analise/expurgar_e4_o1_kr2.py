# -*- coding: utf-8 -*-
"""
Script de expurgo das linhas de E4.O1.KR2 nas 13 planilhas interligadas à meta da Ouvidoria:
ASJUR, GAB, OUV, PA, PCF, PEDU, PGA, PGAAE, PPIMA, PRI, PRT, PSP, PT.
Mantém rigorosamente o padrão visual (#1F4E79), fontes, zebra, alturas e larguras.
Salva em duplicidade: na pasta setorial e em Planilhas_Pos_Comparacao_Consolidadas.
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

UNIT_FOLDERS = {
    "ASJUR": "Assessoria Jurídica",
    "GAB": "Gabinete do Procurador-Geral",
    "OUV": "Ouvidoria",
    "PA": "Procuradoria Administrativa",
    "PCF": "Procuradoria do Contencioso Fiscal",
    "PEDU": "Procuradoria da Educação",
    "PGA": "Procurador-Geral Adjunto",
    "PGAAE": "Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE)",
    "PPIMA": "Procuradoria do Patrimônio Imobiliário e Meio Ambiente",
    "PRI": "Procuradoria Regional de Imperatriz",
    "PRT": "Procuradoria Regional de Timon",
    "PSP": "Procuradoria da Segurança Pública",
    "PT": "Procuradoria Trabalhista"
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

COL_WIDTHS = {
    'A': 28.0,
    'B': 30.0,
    'C': 35.0,
    'D': 35.0,
    'E': 45.0,
    'F': 32.0,
    'G': 18.0
}

HEADERS = [
    "Eixo Estratégico",
    "Objetivo Estratégico",
    "OKR / Meta",
    "Ação (O QUÊ)",
    "Subação / Metodologia (COMO)",
    "Responsáveis (QUEM - Governança Saneada)",
    "Prazo (QUANDO)"
]

def clean_and_save(sigla):
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    wb_orig = openpyxl.load_workbook(cons_path)
    ws_orig = wb_orig.active
    
    title_1 = ws_orig.cell(1, 1).value or f"PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – {sigla}"
    title_2 = ws_orig.cell(2, 1).value or "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Ciclo 2027–2030)"
    
    cleaned_rows = []
    removed_count = 0
    for r in range(6, ws_orig.max_row + 1):
        vals = [ws_orig.cell(r, c).value for c in range(1, 8)]
        if not any(vals):
            continue
        kr_text = str(vals[2] or '')
        # Se for a meta E4.O1.KR2, expurga!
        if 'E4.O1.KR2' in kr_text or 'E4_O1_KR2' in kr_text:
            removed_count += 1
            continue
        cleaned_rows.append(vals)
        
    print(f"[{sigla}] Removidas {removed_count} linhas de E4.O1.KR2. Restam {len(cleaned_rows)} linhas.")
    
    # Gera nova planilha formatada
    wb_new = openpyxl.Workbook()
    ws_new = wb_new.active
    ws_new.title = "Plano de Ação - Saneado"
    ws_new.views.sheetView[0].showGridLines = True
    
    # Títulos
    ws_new.cell(1, 1, title_1)
    ws_new.cell(1, 1).font = FONT_TITLE_1
    ws_new.row_dimensions[1].height = 28.0
    
    ws_new.cell(2, 1, title_2)
    ws_new.cell(2, 1).font = FONT_TITLE_2
    ws_new.row_dimensions[2].height = 18.0
    
    ws_new.row_dimensions[3].height = 10.0
    ws_new.row_dimensions[4].height = 10.0
    
    # Cabeçalho
    ws_new.row_dimensions[5].height = 32.0
    for col_idx, h_text in enumerate(HEADERS, start=1):
        c = ws_new.cell(5, col_idx, h_text)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_HEADER
        c.border = BORDER_THIN
        
    # Dados
    current_row = 6
    for r_idx, row_values in enumerate(cleaned_rows):
        ws_new.row_dimensions[current_row].height = 42.0
        fill_to_use = FILL_ZEBRA_EVEN if (r_idx % 2 == 1) else FILL_ZEBRA_ODD
        
        for col_idx in range(1, 8):
            val = row_values[col_idx - 1] if col_idx - 1 < len(row_values) else ""
            c = ws_new.cell(current_row, col_idx, val)
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
        ws_new.column_dimensions[col_letter].width = width
        
    # Salva no consolidado
    wb_new.save(cons_path)
    
    # Salva na pasta setorial
    folder_name = UNIT_FOLDERS[sigla]
    local_path = os.path.join(BASE_DIR, folder_name, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    wb_new.save(local_path)
    print(f"[{sigla}] Arquivos atualizados em consolidado e pasta local.")

if __name__ == "__main__":
    for sigla in UNIT_FOLDERS.keys():
        clean_and_save(sigla)
    print("Expurgo de E4.O1.KR2 finalizado com sucesso em todas as 13 planilhas!")
