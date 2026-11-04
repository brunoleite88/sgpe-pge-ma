# -*- coding: utf-8 -*-
"""
Script de atualização das 7 planilhas impactadas pelas manifestações SEI:
NIRF, PDA, ASJUR, SGRH, SMP, SGT, UGAM.
Mantém estritamente a formatação visual, cores (#1F4E79), fontes, zebra e dimensões.
Salva tanto na pasta setorial quanto em Planilhas_Pos_Comparacao_Consolidadas.
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

UNIT_FOLDERS = {
    "NIRF": "Núcleo de Inteligência e Recuperação Fiscal (NIRF)",
    "PDA": "Procuradoria da Dívida Ativa",
    "ASJUR": "Assessoria Jurídica",
    "SGRH": "Serviço de Gestão de Recursos Humanos",
    "SMP": "Serviço de Material e Patrimônio",
    "SGT": "Serviços Gerais e Transportes",
    "UGAM": "Unidade Gestora de Atividade Meio"
}

# Estilos Institucionais
FONT_TITLE_1 = Font(name="Calibri", size=13, bold=True, color="001F4E79")
FONT_TITLE_2 = Font(name="Calibri", size=10, italic=True, color="00595959")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="00FFFFFF")
FONT_DATA = Font(name="Calibri", size=10, bold=False, color="00000000")
FONT_DATA_BOLD = Font(name="Calibri", size=10, bold=True, color="00000000")

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

def format_sheet(ws, title_1, title_2, rows_data):
    # Limpa linhas antigas
    ws.delete_rows(1, ws.max_row + 10)
    
    # Linha 1: Título Principal
    ws.cell(1, 1, title_1)
    ws.cell(1, 1).font = FONT_TITLE_1
    ws.row_dimensions[1].height = 28.0
    
    # Linha 2: Subtítulo
    ws.cell(2, 1, title_2)
    ws.cell(2, 1).font = FONT_TITLE_2
    ws.row_dimensions[2].height = 18.0
    
    # Linhas 3 e 4: Espaçamento
    ws.row_dimensions[3].height = 10.0
    ws.row_dimensions[4].height = 10.0
    
    # Linha 5: Cabeçalho
    ws.row_dimensions[5].height = 32.0
    for col_idx, h_text in enumerate(HEADERS, start=1):
        cell = ws.cell(5, col_idx, h_text)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_THIN
        
    # Linhas de Dados
    current_row = 6
    for r_idx, row_values in enumerate(rows_data):
        ws.row_dimensions[current_row].height = 42.0
        fill_to_use = FILL_ZEBRA_EVEN if (r_idx % 2 == 1) else FILL_ZEBRA_ODD
        
        for col_idx in range(1, 8):
            val = row_values[col_idx - 1] if col_idx - 1 < len(row_values) else ""
            cell = ws.cell(current_row, col_idx, val)
            cell.font = FONT_DATA
            cell.border = BORDER_THIN
            if fill_to_use.fill_type:
                cell.fill = fill_to_use
            
            # Alinhamento
            if col_idx == 7:
                cell.alignment = ALIGN_DATA_CENTER
            else:
                cell.alignment = ALIGN_DATA_LEFT
                
        current_row += 1
        
    # Largura das Colunas
    for col_letter, width in COL_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

print("Módulo de formatação configurado.")
