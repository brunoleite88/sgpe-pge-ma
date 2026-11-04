# -*- coding: utf-8 -*-
"""
Script completo de atualização das 7 planilhas impactadas pelas manifestações SEI:
NIRF, PDA, ASJUR, SGRH, SMP, SGT, UGAM.
Mantém estritamente a formatação visual (#1F4E79), fontes, zebra, larguras e alturas.
Salva tanto na pasta setorial quanto em Planilhas_Pos_Comparacao_Consolidadas.
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

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

def load_existing_rows(filepath):
    """Carrega dados da planilha a partir da linha 6."""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    rows = []
    for r in range(6, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 8)]
        if any(vals):  # Se houver qualquer conteúdo
            rows.append(vals)
    return rows

def write_formatted_sheet(filepath, title_1, title_2, rows_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plano de Ação - Saneado"
    ws.views.sheetView[0].showGridLines = True
    
    # Linha 1: Título Principal
    ws.cell(1, 1, title_1)
    ws.cell(1, 1).font = FONT_TITLE_1
    ws.row_dimensions[1].height = 28.0
    
    # Linha 2: Subtítulo
    ws.cell(2, 1, title_2)
    ws.cell(2, 1).font = FONT_TITLE_2
    ws.row_dimensions[2].height = 18.0
    
    # Linhas 3 e 4
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
        
    # Dados
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
            
            if col_idx == 7:
                cell.alignment = ALIGN_DATA_CENTER
            else:
                cell.alignment = ALIGN_DATA_LEFT
                
        current_row += 1
        
    for col_letter, width in COL_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width
        
    wb.save(filepath)
    print(f"Salvo: {filepath} ({len(rows_data)} linhas)")

def save_dual(sigla, title_1, title_2, rows_data):
    # 1. Salva em Planilhas_Pos_Comparacao_Consolidadas
    cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    write_formatted_sheet(cons_path, title_1, title_2, rows_data)
    
    # 2. Salva na pasta setorial
    folder_name = UNIT_FOLDERS[sigla]
    local_path = os.path.join(BASE_DIR, folder_name, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    write_formatted_sheet(local_path, title_1, title_2, rows_data)

# -------------------------------------------------------------------------
# 1. NIRF
# -------------------------------------------------------------------------
def adjust_nirf():
    sigla = "NIRF"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – NIRF"
    title_2 = "[UNIDADE DISPENSADA DE PLANILHA AUTÔNOMA – CONSOLIDADA NA PLANILHA DA PDA (DESPACHO Nº 50/2026 - SEI 2026.11103.07215)]"
    
    new_rows = []
    # Linha formal de dispensa no topo
    new_rows.append([
        "Eixo Estratégico 1 – Incrementar a arrecadação e otimizar a cobrança da dívida ativa",
        "O2: Aumentar a arrecadação da dívida ativa",
        "[E1.O2.KR1] KR1: Aumentar em 10% a arrecadação direta da Dívida Ativa (tributária e não tributária) até 2030",
        "Dispensa formal de planilha autônoma e unificação com o plano da Procuradoria da Dívida Ativa (PDA)",
        "Conforme Despacho nº 50/2026 (Processo SEI nº 2026.11103.07215), as ações e subações do NIRF passam a integrar o Plano Consolidado da PDA, atuando o Núcleo no suporte técnico de inteligência fiscal, cruzamento de bases patrimoniais e saneamento de CDAs.",
        "Líder Homologado: Procuradoria da Dívida Ativa (PDA); Execução Técnica e Inteligência de Dados: NIRF (Ato SEI nº 50/2026)",
        "Imediato / Pleno"
    ])
    
    # Atualiza as linhas originais referenciando a PDA como líder
    for r in orig_rows:
        r_copy = list(r)
        r_copy[5] = "Líder Homologado: Procuradoria da Dívida Ativa (PDA); Execução Técnica / Inteligência Fiscal: NIRF (Despacho SEI nº 50/2026)"
        new_rows.append(r_copy)
        
    save_dual(sigla, title_1, title_2, new_rows)

# -------------------------------------------------------------------------
# 2. PDA
# -------------------------------------------------------------------------
def adjust_pda():
    sigla = "PDA"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – PDA (PROCURADORIA DA DÍVIDA ATIVA)"
    title_2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Incorporando inteligência fiscal do NIRF - SEI 2026.11103.07215)"
    
    new_rows = []
    for r in orig_rows:
        r_copy = list(r)
        kr = str(r_copy[2])
        # Se for meta de cobrança/patrimônio onde o NIRF atua, explicita a coexecução do NIRF
        if any(k in kr for k in ["E1.O2.KR1", "E1.O2.KR2", "E1.O2.KR3", "E1.O4.KR1", "E1.O4.KR2", "E1.O5.KR1", "E1.O5.KR2"]):
            r_copy[5] = "Líder Institucional: Procuradoria da Dívida Ativa (PDA); Coexecutor Técnico / Inteligência Fiscal: NIRF"
        new_rows.append(r_copy)
        
    # Adiciona ação expressa de mineração de dados patrimoniais do NIRF sob liderança da PDA
    new_rows.append([
        "Eixo Estratégico 1 – Incrementar a arrecadação e otimizar a cobrança da dívida ativa",
        "O4: Fortalecer a Identificação e Recuperação de Ativos Fiscais",
        "[E1.O4.KR1] KR1: Identificar R$ 1 milhão em créditos tributários ocultos ou subestimados até 2027",
        "Mineração de dados e cruzamento de bases cadastrais e patrimoniais de grandes devedores (Inteligência NIRF)",
        "Operacionalizar cruzamento automatizado de bases da PGE, SEFAZ, Receita Federal, JUCEMA, CENSEC e Cartórios de Imóveis para identificação de sócios ocultos, fraudes societárias e patrimônio expropriável.",
        "Líder Institucional: Procuradoria da Dívida Ativa (PDA); Coexecutor Técnico / Inteligência Fiscal: NIRF",
        "Contínuo / Trimestral"
    ])
    
    save_dual(sigla, title_1, title_2, new_rows)

# -------------------------------------------------------------------------
# 3. ASJUR (Assessoria Especial / Consultoria-Geral)
# -------------------------------------------------------------------------
def adjust_asjur():
    sigla = "ASJUR"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – ASSESSORIA ESPECIAL / ASJUR"
    title_2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Diretrizes do Memorando nº 38/2026 - SEI 2025.11103.05165)"
    
    new_rows = []
    for r in orig_rows:
        r_copy = list(r)
        kr = str(r_copy[2])
        # Ajusta KR1 do Eixo 4 para tempestividade qualificada
        if "E4.O1.KR1" in kr:
            r_copy[3] = "Aprimorar a tempestividade da atuação consultiva complexa e estratégica da Assessoria Especial"
            r_copy[4] = "Implantar protocolo de triagem por grau de complexidade e impacto fiscal/institucional, garantindo tempo hábil para exames jurídicos aprofundados de teses inéditas sem comprometer o fluxo de prazos regulamentares (Memorando nº 38/2026)."
            r_copy[5] = "Líder: Assessoria Especial / Consultoria-Geral; Coexecutores: PGAAE, Secretarias de Estado"
        # Ajusta KR2 do Eixo 4 para qualidade e segurança jurídica
        elif "E4.O1.KR2" in kr:
            r_copy[3] = "Fortalecer a segurança jurídica, clareza e previsibilidade técnica das orientações aos órgãos consulentes"
            r_copy[4] = "Mensurar a qualidade das manifestações sob a ótica da blindagem jurídica e conformidade da administração estadual, realizando reuniões prévias de alinhamento técnico institucional para dirimir dúvidas e prevenir nulidades."
            r_copy[5] = "Líder: Assessoria Especial / Consultoria-Geral; Coexecutores: PGAAE, Ouvidoria"
        new_rows.append(r_copy)
        
    save_dual(sigla, title_1, title_2, new_rows)

# -------------------------------------------------------------------------
# 4. SGRH
# -------------------------------------------------------------------------
def adjust_sgrh():
    sigla = "SGRH"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – SGRH (SERVIÇO DE GESTÃO DE RECURSOS HUMANOS)"
    title_2 = "Classificação formal e Estruturação Executiva em 5 Eixos (Despacho SEI nº 018120848 - Processo 2026.11103.07207)"
    
    # 5 Eixos estruturantes do Despacho nº 018120848
    sei_axes_rows = [
        [
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O7: Reestruturar o quadro de pessoal",
            "[E5.O7.KR1] KR1: Nomear 25 servidores aprovados em concurso até 2028",
            "Auditoria prévia de lotação e dimensionamento da força de trabalho da PGE-MA (Eixo I - Despacho SEI 018120848)",
            "Realizar levantamento detalhado de cargos, lotações e demandas setoriais antes de qualquer nova contratação; revisar critérios de gratificações/adicionais vinculando-os a metas mensuráveis de produtividade.",
            "Líder: Serviço de Gestão de Recursos Humanos (SGRH); Coexecutores: UGAM, Procurador-Geral",
            "180 dias / Anual"
        ],
        [
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O5: Otimizar e automatizar rotinas e processos",
            "[E5.O5.KR3] KR3: Aumentar em 25% a produtividade processual das equipes setoriais até 2030",
            "Mapeamento BPMN e definição de SLAs para rotinas de gestão de pessoas (Eixo II - Despacho SEI 018120848)",
            "Modelar e padronizar os fluxos internos de férias, licenças, afastamentos e aposentadorias em BPMN, estabelecendo SLAs rígidos para eliminação de filas e retrabalho operacional.",
            "Líder: SGRH; Coexecutores: UGAM, Supervisão de Informática",
            "12 meses"
        ],
        [
            "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
            "O2: Capacitar continuamente os servidores e procuradores",
            "[E9.O2.KR1] KR1: Capacitar anualmente ao menos 40% dos procuradores e servidores até 2030",
            "Instituir Avaliação de Desempenho por Competências e Plano Anual de Capacitação - PACD (Eixo III - Despacho SEI 018120848)",
            "Implantar metodologia de avaliação por competências técnicas e comportamentais, publicar a Carta de Serviços do Servidor e executar trilhas de capacitação continuada em parceria com a ESAP.",
            "Líder: SGRH; Coexecutores: ESAP, UGAM",
            "Ciclo Anual até 2030"
        ],
        [
            "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica",
            "O3: Fomentar uma cultura de inovação institucional",
            "[E7.O3.KR1] KR1: Implementar 5 projetos estratégicos de inovação e modernização voltados a desafios prioritários da PGE até 2030",
            "Implantar o Assentamento Funcional Digital (AFD) e Painel de BI de Gestão de Pessoas (Eixo IV - Despacho SEI 018120848)",
            "Digitalizar 100% dos prontuários e pastas funcionais físicas (PGE sem papel); implantar Chatbot/Portal do Servidor para autoatendimento e painel de BI com indicadores de absenteísmo, turnover e banco de horas.",
            "Líder: SGRH; Coexecutores: Supervisão de Informática, PGAAE/INOVA",
            "Até 2027"
        ],
        [
            "Eixo Estratégico 8 – Fomentar a sustentabilidade, a integridade e a responsabilidade social",
            "O2: Fortalecer a Governança e a Integridade Institucional",
            "[E8.O2.KR1] KR1: Garantir a apuração de 100% das denúncias e manifestações dentro do prazo legal até 2030",
            "Atualizar o Código de Ética e instituir canal seguro de combate ao assédio e discriminação (Eixo V - Despacho SEI 018120848)",
            "Revisar normas de conduta, instituir protocolo seguro e sigiloso de denúncias contra assédio moral e sexual em cooperação com a Ouvidoria e Corregedoria, e implantar programa permanente de saúde mental, ergonomia e acolhimento funcional.",
            "Líder: SGRH; Coexecutores: Ouvidoria, Corregedoria-Geral, UGAM",
            "180 dias / Contínuo"
        ]
    ]
    
    # Une os 5 eixos maduros no topo com as demais ações existentes
    all_rows = sei_axes_rows + orig_rows
    save_dual(sigla, title_1, title_2, all_rows)

# -------------------------------------------------------------------------
# 5. SMP
# -------------------------------------------------------------------------
def adjust_smp():
    sigla = "SMP"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – SMP (SERVIÇO DE MATERIAL E PATRIMÔNIO)"
    title_2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Diretrizes do Despacho nº 057/2026 - SEI 2026.11103.07208)"
    
    new_rows = [
        [
            "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
            "O1: Reduzir custos operacionais",
            "[E2.O1.KR1] KR1: Reduzir em 10% os custos operacionais de custeio e contratos continuados até 2026",
            "Triagem técnica e filtro restritivo das requisições de compras dos setores da PGE-MA (Despacho SEI nº 057/2026)",
            "Implementar protocolo obrigatório de auditoria de consumo histórico para indeferir pedidos de compra excessivos ou redundantes, impedindo formação de estoques ociosos nos gabinetes e desperdício de material de consumo.",
            "Líder: Serviço de Material e Patrimônio (SMP); Coexecutores: UGAM, Todas as Unidades da PGE-MA",
            "Imediato / Contínuo até 2026"
        ],
        [
            "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
            "O1: Reduzir custos operacionais",
            "[E2.O1.KR1] KR1: Reduzir em 10% os custos operacionais de custeio e contratos continuados até 2026",
            "Modernização e informatização do controle de estoque do almoxarifado central (Despacho SEI nº 057/2026)",
            "Implantar inventário digital com parametrização de estoque mínimo e ponto de ressuprimento automático; repactuar contratos contínuos de fornecimento para redução de 10% de despesas de custeio.",
            "Líder: SMP; Coexecutores: UGAM, Supervisão de Informática",
            "180 dias"
        ]
    ] + orig_rows
    
    save_dual(sigla, title_1, title_2, new_rows)

# -------------------------------------------------------------------------
# 6. SGT
# -------------------------------------------------------------------------
def adjust_sgt():
    sigla = "SGT"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – SGT (SERVIÇOS GERAIS E TRANSPORTES)"
    title_2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Diretrizes do Despacho nº 56/2026 - SEI 2026.11103.07209)"
    
    new_rows = [
        [
            "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
            "O1: Reduzir custos operacionais",
            "[E2.O1.KR1] KR1: Reduzir em 10% os custos operacionais de custeio e contratos continuados até 2026",
            "Gestão e fiscalização integrada de contratos de mão de obra terceirizada e apoio predial (Despacho SEI nº 56/2026)",
            "Auditar postos terceirizados de apoio administrativo, recepção, vigilância e motoristas, aplicando glosas a postos vagos ou desnecessários para assegurar a meta de 10% de economia de custeio.",
            "Líder: Serviços Gerais e Transportes (SGT); Coexecutores: UGAM",
            "Contínuo até 2026"
        ],
        [
            "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
            "O1: Reduzir custos operacionais",
            "[E2.O1.KR1] KR1: Reduzir em 10% os custos operacionais de custeio e contratos continuados até 2026",
            "Racionalização da distribuição de insumos e conservação predial (Despacho SEI nº 56/2026)",
            "Implantar cronograma programado (quinzenal/mensal) de remessa parametrizada de materiais de limpeza às unidades da capital e regionais, controlando consumo per capita.",
            "Líder: SGT; Coexecutores: UGAM, Regionais",
            "60 dias / Rotina Permanente"
        ],
        [
            "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
            "O1: Reduzir custos operacionais",
            "[E2.O1.KR1] KR1: Reduzir em 10% os custos operacionais de custeio e contratos continuados até 2026",
            "Colaboração institucional para eliminação de impressões e papel físico",
            "Atuar junto à Supervisão de Informática e UGAM na transição para rotinas 100% digitais no SEI/SPA, reduzindo despesas com locação de impressoras e papel.",
            "Líder: SGT; Coexecutores: Supervisão de Informática, UGAM",
            "Até 2027"
        ]
    ] + orig_rows
    
    save_dual(sigla, title_1, title_2, new_rows)

# -------------------------------------------------------------------------
# 7. UGAM
# -------------------------------------------------------------------------
def adjust_ugam():
    sigla = "UGAM"
    orig_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    orig_rows = load_existing_rows(orig_path)
    
    title_1 = "PLANO DE AÇÃO ESTRATÉGICO 2026–2030 (PÓS-COMPARAÇÃO) – UGAM (UNIDADE GESTORA DE ATIVIDADE MEIO)"
    title_2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Coordenação Integrada de Custeio, Patrimônio e Pessoas)"
    
    new_rows = []
    for r in orig_rows:
        r_copy = list(r)
        kr = str(r_copy[2])
        if any(k in kr for k in ["E2.O1.KR1", "E2.O1.KR2", "E5.O7.KR1", "E8.O1.KR1"]):
            r_copy[5] = "Líder Coordenador: Unidade Gestora de Atividade Meio (UGAM); Setores Executores: SMP, SGT, SGRH"
        new_rows.append(r_copy)
        
    save_dual(sigla, title_1, title_2, new_rows)

if __name__ == "__main__":
    print("Iniciando ajustes nas 7 planilhas...")
    adjust_nirf()
    adjust_pda()
    adjust_asjur()
    adjust_sgrh()
    adjust_smp()
    adjust_sgt()
    adjust_ugam()
    print("Ajustes concluídos com sucesso em todas as unidades!")
