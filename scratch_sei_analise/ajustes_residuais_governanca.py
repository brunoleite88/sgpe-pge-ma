# -*- coding: utf-8 -*-
"""
Script de aplicação dos ajustes residuais de governança:
1. PGARI: Expurgo das 6 linhas de E3.O1.KR1 (captação externa/orçamento pertencente à PGA/USF).
2. Contenciosas (PJ, PT, PCF, PRI, PRT, PB): Inclusão da subação obrigatória de repasse quinzenal de vitórias processuais para a ASCOM (E6.O1.KR2).
3. Preservação estrita dos estilos (#1F4E79), fontes, zebra, alturas e larguras.
4. Salva em duplicidade: pasta setorial e Planilhas_Pos_Comparacao_Consolidadas.
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

UNIT_FOLDERS = {
    "PGARI": "Procuradoria-Geral Adjunta de Relacionamento Institucional",
    "ASCOM": "Assessoria de Comunicação",
    "PJ": "Procuradoria Judicial",
    "PT": "Procuradoria Trabalhista",
    "PCF": "Procuradoria do Contencioso Fiscal",
    "PRI": "Procuradoria Regional de Imperatriz",
    "PRT": "Procuradoria Regional de Timon",
    "PB": "Procuradoria de Brasília"
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

def load_rows(filepath):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    rows = []
    for r in range(6, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 8)]
        if any(vals):
            rows.append(vals)
    return rows, ws.cell(1, 1).value, ws.cell(2, 1).value

def write_sheet(sigla, title_1, title_2, rows_data):
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
        ws.row_dimensions[current_row].height = 42.0
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
        
    # Salva no consolidado
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    wb.save(cons_path)
    
    # Salva na pasta setorial
    folder_name = UNIT_FOLDERS[sigla]
    local_path = os.path.join(BASE_DIR, folder_name, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    wb.save(local_path)
    print(f"[{sigla}] Salvo com sucesso ({len(rows_data)} linhas).")

# 1. Ajuste PGARI
def adjust_pgari():
    sigla = "PGARI"
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    rows, t1, t2 = load_rows(cons_path)
    
    # Filtra as linhas de E3.O1.KR1
    filtered = []
    removed = 0
    for r in rows:
        kr = str(r[2] or '')
        if "E3.O1.KR1" in kr or "E3" in str(r[0] or ''):
            removed += 1
            continue
        filtered.append(r)
    print(f"[PGARI] Removidas {removed} linhas de E3.O1.KR1. Restam {len(filtered)} linhas.")
    
    t2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Foco em Relações Institucionais e Riscos Socioambientais)"
    write_sheet(sigla, t1, t2, filtered)

# 2. Ajuste Contenciosas (PJ, PT, PCF, PRI, PRT, PB)
def add_ascom_feed_to_contenciosa(sigla, unit_name):
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    rows, t1, t2 = load_rows(cons_path)
    
    # Verifica se já tem a ação
    has_feed = any("Alimentação sistemática e tempestiva da Assessoria de Comunicação" in str(r[3] or '') for r in rows)
    if not has_feed:
        new_row = [
            "Eixo Estratégico 6 – Fortalecer a imagem institucional e a comunicação com a sociedade",
            "O1: Fortalecer a imagem e o reconhecimento da PGE como referência de excelência",
            "[E6.O1.KR2] KR2: Alcançar crescimento contínuo do alcance médio mensal nas redes sociais da PGE até 2029",
            "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com decisões judiciais favoráveis",
            f"Instituir rotina setorial quinzenal de envio de relatórios e cópias de sentenças, acórdãos e tutelas de urgência de alta relevância à ASCOM, viabilizando a divulgação institucional e transparência da atuação da PGE-MA.",
            f"Líder: {unit_name}; Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
            "Fluxo Quinzenal / Contínuo"
        ]
        rows.append(new_row)
        print(f"[{sigla}] Inserida linha de fluxo obrigatório para ASCOM.")
        
    write_sheet(sigla, t1, t2, rows)

if __name__ == "__main__":
    adjust_pgari()
    add_ascom_feed_to_contenciosa("PJ", "Procuradoria Judicial (PJ)")
    add_ascom_feed_to_contenciosa("PT", "Procuradoria Trabalhista (PT)")
    add_ascom_feed_to_contenciosa("PCF", "Procuradoria do Contencioso Fiscal (PCF)")
    add_ascom_feed_to_contenciosa("PRI", "Procuradoria Regional de Imperatriz (PRI)")
    add_ascom_feed_to_contenciosa("PRT", "Procuradoria Regional de Timon (PRT)")
    add_ascom_feed_to_contenciosa("PB", "Procuradoria de Brasília (PB)")
    print("Ajustes residuais concluídos com sucesso!")
