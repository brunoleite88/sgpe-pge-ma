# -*- coding: utf-8 -*-
"""
Gera o documento técnico em formato .docx:
'Análise Conclusiva de Atendimento às Manifestações da ASCOM e da Ouvidoria-Geral (SEI 20 e 19/2026) e Matriz de Ausência de Conflitos no SGPE PGE-MA'
"""
import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DOCX = BASE_DIR / "docs" / "exports" / "Analise_Manifestacoes_ASCOM_Ouvidoria_Saneamento.docx"
ROOT_DOCX = BASE_DIR / "Analise_Manifestacoes_ASCOM_Ouvidoria_Saneamento.docx"

def set_cell_background(cell, fill_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx():
    doc = docx.Document()
    
    # Configuração de Margens (2,0 cm = ~0,79 in)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Estilos Padrão
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B) # Slate-800
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # --- CABEÇALHO INSTITUCIONAL ---
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("GOVERNO DO ESTADO DO MARANHÃO\n")
    r_inst1.font.bold = True
    r_inst1.font.size = Pt(10)
    r_inst1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    r_inst2 = p_inst.add_run("PROCURADORIA-GERAL DO ESTADO DO MARANHÃO (PGE-MA)\n")
    r_inst2.font.bold = True
    r_inst2.font.size = Pt(11)
    r_inst2.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Blue-900

    r_inst3 = p_inst.add_run("PLANEJAMENTO ESTRATÉGICO INSTITUCIONAL (CICLO 2027–2030)\n")
    r_inst3.font.bold = True
    r_inst3.font.size = Pt(9.5)
    r_inst3.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    r_div = p_inst.add_run("—" * 45)
    r_div.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    p_inst.paragraph_format.space_after = Pt(12)

    # --- TÍTULO DO DOCUMENTO ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_t1 = p_title.add_run("PARECER TÉCNICO DE SANEAMENTO METODOLÓGICO\n")
    r_t1.font.size = Pt(13)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_t2 = p_title.add_run("Análise Conclusiva de Atendimento às Manifestações da ASCOM e Ouvidoria-Geral (SEI nº 018469339 e 018468827) e Matriz de Ausência de Conflito de Governança")
    r_t2.font.size = Pt(11)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(0x25, 0x63, 0xEB) # Blue-600
    p_title.paragraph_format.space_after = Pt(10)

    # --- METADADOS DO PROCESSO ---
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    meta_widths = [Inches(2.2), Inches(4.7)]
    
    meta_data = [
        ("Processos SEI Vinculados:", "SEI 2026.11103.07178 (ASCOM) e SEI 2026.11103.07187 (Ouvidoria)"),
        ("Documentos Analisados:", "Manifestação nº 20 (018469339) e Manifestação nº 19 (018468827)"),
        ("Autoridade Signatária:", "Dra. Martha Jackson Franco de Sá Monteiro (Chefe da ASCOM e Ouvidoria)"),
        ("Conclusão Técnica:", "Atendimento integral das demandas e ausência total de conflito de competências.")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = tbl_meta.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = meta_widths[0], meta_widths[1]
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9)
        r0.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9)
        if "Atendimento integral" in v:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(0x04, 0x78, 0x57) # Emerald-700
    set_table_borders(tbl_meta, "94A3B8")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- SEÇÃO 1: SÍNTESE EXECUTIVA ---
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. SÍNTESE EXECUTIVA E CONCLUSÃO PRELIMINAR")
    r_h1.font.bold = True
    r_h1.font.size = Pt(12)
    r_h1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "Submetidas à análise técnica da Coordenação do Planejamento Estratégico, constatou-se que "
    )
    r_emp = p_intro.add_run("todas as exigências, observações metodológicas e propostas de adequação ")
    r_emp.font.bold = True
    p_intro.add_run(
        "formuladas pela chefia da Assessoria de Comunicação (ASCOM) e da Ouvidoria-Geral da PGE-MA, "
        "consubstanciadas nas Manifestações SEI nº 20/2026 e nº 19/2026, "
    )
    r_emp2 = p_intro.add_run("foram integralmente contempladas no Sistema de Governança e Planejamento Estratégico (SGPE PGE-MA).")
    r_emp2.font.bold = True

    p_cond = doc.add_paragraph()
    p_cond.add_run(
        "Em estrita observância à diretriz de "
    )
    r_cond = p_cond.add_run("ausência de conflito de competências e de papéis institucionais")
    r_cond.font.bold = True
    p_cond.add_run(
        ", a incorporação dessas manifestações preservou de forma absoluta a autoridade correcional privativa da "
        "Corregedoria-Geral (CG), a governança pedagógica unificada da Escola Superior da Advocacia Pública (ESAP), "
        "a governança de sistemas da Assessoria em TIC da PGAAE/INOVA, a sustentação de infraestrutura da Supervisão de Informática (SI), "
        "a liderança corporativa do Conselho Superior em matéria de honorários e a desoneração operacional das Procuradorias Especializadas contenciosas."
    )

    # --- SEÇÃO 2: DETALHAMENTO DA ASCOM (MANIFESTAÇÃO 20) ---
    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("2. MATRIZ DE INCORPORAÇÃO DAS DEMANDAS DA ASCOM (MANIFESTAÇÃO SEI Nº 20/2026)")
    r_h2.font.bold = True
    r_h2.font.size = Pt(12)
    r_h2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_ascom_desc = doc.add_paragraph()
    p_ascom_desc.add_run(
        "A tabela a seguir discrimina pontualmente cada consideração apresentada na Manifestação nº 20/2026, "
        "identificando o local exato de sua inserção no plano (texto da meta ou colunas da planilha) e o mecanismo de preservação da governança saneada:"
    )

    t_ascom = doc.add_table(rows=1, cols=4)
    t_ascom.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ascom.autofit = False
    set_table_borders(t_ascom)
    
    col_w_ascom = [Inches(1.8), Inches(1.8), Inches(2.2), Inches(1.1)]
    headers_ascom = [
        "Tema / Exigência da Dra. Martha (ASCOM)",
        "Onde foi Incorporado no SGPE",
        "Texto Específico / Coluna da Planilha",
        "Conflito Evitado"
    ]
    hdr_row = t_ascom.rows[0]
    for i, h in enumerate(headers_ascom):
        cell = hdr_row.cells[i]
        cell.width = col_w_ascom[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    itens_ascom = [
        (
            "1. Meta prévia de 20% em Engajamento (E6.O1.KR1):\n"
            "Exigiu não fixar meta percentual cega antes da linha de base de 2025, pois as plataformas têm métricas heterogêneas.",
            "Diretamente no Texto da Meta (Coluna C - OKR / Meta)",
            "Texto ajustado do KR: '[E6.O1.KR1] KR1: Aumentar a taxa de engajamento da PGE nas mídias institucionais até 2029, em percentual a ser definido após a consolidação da linha de base de [E6.O1.KR2] (referência da PGAAE: 20%)'.",
            "Harmonizado:\nNão impõe cobrança inexequível à unidade."
        ),
        (
            "2. Expressão 'Crescimento Contínuo' (E6.O1.KR2):\n"
            "Exigiu trocar por 'crescimento progressivo' e deduzir formalmente os meses de defeso eleitoral e oscilações de algoritmos.",
            "Texto da Meta (Coluna C) e Subação/Metodologia (Coluna E)",
            "Texto do KR: '[E6.O1.KR2] KR2: Alcançar crescimento progressivo do alcance médio mensal nas redes sociais da PGE até 2029, aferido pela comparação entre médias de períodos equivalentes'.\n"
            "Coluna E (Ação 4): Metodologia exclui defeso eleitoral e atipicidades.",
            "Harmonizado:\nAdequação à legislação eleitoral vinculante."
        ),
        (
            "3. Segregação de Canais (Redes Sociais x Extranet):\n"
            "Extranet é comunicação interna; métricas de leitura dependem de TIC e não podem ser cobradas como rede social.",
            "Planilha da ASCOM:\nColuna D (Ação 1) e Coluna E (Subação)",
            "Coluna D: 'Avaliar viabilidade técnica de aprimoramento das métricas da Extranet junto à TIC'.\n"
            "Coluna E: Condicionada à validação de TIC/SI e preservada como canal interno complementar sem prejuízo das redes externas.",
            "Sem Conflito:\nNão invade atribuições de desenvolvimento da TIC."
        ),
        (
            "4. Fluxo de Captação Tempestiva de Êxitos Processuais:\n"
            "Exigiu Portaria do PG para disciplinar corresponsabilidade das Especializadas no envio tempestivo de acórdãos favoráveis.",
            "Planilha da ASCOM (Ação 2) e Ações Espelhadas em 15 Especializadas",
            "Coluna D (ASCOM): 'Propor ato normativo disciplinando o fluxo de captação tempestiva de êxitos processuais' (Prazo: 60 dias).\n"
            "Em 15 Especializadas (Coluna D): Criada ação 'Alimentação sistemática e tempestiva da ASCOM com decisões favoráveis e teses'.",
            "Harmonizado:\nCria fluxo oficial bilateral de insumos."
        ),
        (
            "5. Validação Jurídica x Edição Jornalística:\n"
            "ASCOM faz jornalismo e linguagem cidadã; confirmação de teses, dados e ausência de segredo de justiça é dever das Especializadas.",
            "Planilha da ASCOM (Ação 4, Coluna E) e Planilhas das Especializadas",
            "Coluna E (ASCOM): Especializadas atestam ausência de sigilo e acurácia jurídica.\n"
            "Coluna F (Especializadas): Assumem expressamente a responsabilidade pelo conteúdo técnico-jurídico encaminhado.",
            "Sem Conflito:\nProtege a ASCOM contra riscos de quebra de sigilo."
        ),
        (
            "6. Delimitação Estrita em Eventos:\n"
            "ASCOM cuida apenas de divulgação, imprensa e cobertura; cerimonial, logística e contratos cabem a Gabinete, ESAP e SGA.",
            "Planilha da ASCOM:\nColuna D e Coluna E (Ação 5)",
            "Coluna D: 'Prestar suporte de comunicação e divulgação aos eventos institucionais estratégicos da PGE-MA'.\n"
            "Coluna E: Ressalva expressa de que cerimonial e infraestrutura física pertencem a Gabinete/ESAP/SGA.",
            "Sem Conflito:\nEvita sobrecarga operacional na equipe da ASCOM."
        ),
        (
            "7. Gravações do YouTube dos Tribunais (SGA):\n"
            "Aceitou a proposta do Dr. Beolândio de cortes de sustentações, com a condição de triagem prévia pelas Especializadas.",
            "Planilha da ASCOM:\nColuna D e Coluna E (Ação 10)",
            "Coluna D: 'Aproveitar acervo de sustentações orais gravadas dos Tribunais para divulgação institucional'.\n"
            "Coluna E: Triagem prévia da tese jurídica realizada pela SGA e Especializadas antes da edição final de cortes.",
            "Sem Conflito:\nIntegração fluida entre SGA e ASCOM."
        ),
        (
            "8. Desoneração da Meta de 40% de Capacitação (E9.O2.KR1):\n"
            "ASCOM não pode responder pela meta macro da PGE; seu papel é indicar demandas de cursos ao PAC.",
            "Planilha da ASCOM:\nColuna D, E e F (Ação 12)",
            "Coluna D: 'Levantar necessidades anuais de capacitação da unidade e indicar trilhas técnicas ao PAC'.\n"
            "Coluna F: 'Líder Institucional: ESAP e SGRH; Demandante Setorial no PAC: ASCOM'.",
            "Harmonizado:\nLiderança exclusiva e unificada na ESAP/SGRH."
        ),
        (
            "9. Liderança Exclusiva no Relatório 8 (Metas):\n"
            "ASCOM deve liderar de fato o KR2; unidades contenciosas não devem disputar nem ser cobradas pela meta de redes sociais.",
            "Governança do SGPE e Relatório 8 de Metas",
            "Quadro de Metas (Relatório 8): Apenas a ASCOM figura como Líder de E6.O1.KR2.\n"
            "15 Especializadas reclassificadas para 'Fornecedor de Insumo / Apoio', saindo de seus relatórios de metas.",
            "Harmonizado:\nEnxugamento de relatórios e fim de conflito de papéis."
        )
    ]

    for item in itens_ascom:
        row = t_ascom.add_row()
        for idx, text in enumerate(item):
            c = row.cells[idx]
            c.width = col_w_ascom[idx]
            set_cell_margins(c, 60, 60, 80, 80)
            set_cell_background(c, "F8FAFC" if idx == 0 else "FFFFFF")
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif idx == 3:
                r.font.color.rgb = RGBColor(0x04, 0x78, 0x57) # Green

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SEÇÃO 3: DETALHAMENTO DA OUVIDORIA (MANIFESTAÇÃO 19) ---
    h3 = doc.add_heading(level=1)
    r_h3 = h3.add_run("3. MATRIZ DE INCORPORAÇÃO DAS DEMANDAS DA OUVIDORIA-GERAL (MANIFESTAÇÃO SEI Nº 19/2026)")
    r_h3.font.bold = True
    r_h3.font.size = Pt(12)
    r_h3.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_ouv_desc = doc.add_paragraph()
    p_ouv_desc.add_run(
        "A tabela a seguir discrimina pontualmente as considerações da Manifestação nº 19/2026, com foco na estrita "
        "separação de competências correcionais, transparência ativa e iniciativas da aba 'Inclusões a deliberar':"
    )

    t_ouv = doc.add_table(rows=1, cols=4)
    t_ouv.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ouv.autofit = False
    set_table_borders(t_ouv)
    
    col_w_ouv = [Inches(1.8), Inches(1.8), Inches(2.2), Inches(1.1)]
    headers_ouv = [
        "Tema / Exigência da Dra. Martha (Ouvidoria)",
        "Onde foi Incorporado no SGPE",
        "Texto Específico / Coluna da Planilha",
        "Conflito Evitado"
    ]
    hdr_row_o = t_ouv.rows[0]
    for i, h in enumerate(headers_ouv):
        cell = hdr_row_o.cells[i]
        cell.width = col_w_ouv[i]
        set_cell_background(cell, "0F766E") # Teal-700
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    itens_ouv = [
        (
            "1. Apuração de Denúncias x Encaminhamento (E8.O2.KR1):\n"
            "Ouvidoria não apura desvios funcionais nem tem poder sancionatório (atribuição constitucional privativa da CG e Conselho).",
            "Planilha da Ouvidoria:\nColuna D (Ação 4), Coluna E e Coluna F",
            "Coluna D: 'Assegurar o tratamento e o encaminhamento tempestivo de denúncias para apuração competente'.\n"
            "Coluna E: Evidência mede triagem e encaminhamento conclusivo em 30 dias.\n"
            "Coluna F: 'Líder do Tratamento/Encaminhamento: Ouvidoria; Atribuição Privativa da Apuração e Conclusão: Corregedoria-Geral (CG)'.",
            "Sem Conflito:\nPreserva integralmente a competência da Corregedoria."
        ),
        (
            "2. Meta de Transparência (Nota 9 em E8.O2.KR2):\n"
            "Inviável fixar nota 9 sem metodologia e sem linha de base adaptada às peculiaridades da PGE (sigilo fiscal e judicial).",
            "Diretamente no Texto da Meta (Coluna C - OKR / Meta)",
            "Texto ajustado do KR: '[E8.O2.KR2] KR2: Alcançar nota 9 em escala de transparência interna da PGE até 2030 (meta a ser validada após a fixação da linha de base)'.\n"
            "Coluna D (Ação 9): Prevê 120 dias para desenvolvimento da matriz e linha de base com a TIC.",
            "Harmonizado:\nMetodologia científica prévia sem metas cegas."
        ),
        (
            "3. Manual de Integridade e Canais de Assédio:\n"
            "Não criar canais paralelos aos oficiais do Estado (OESPA/STC); prazo de 180 dias; evidência = entrega da minuta (aprovação compete ao PG).",
            "Planilha da Ouvidoria:\nColuna D, E, F e G (Ações 5, 6 e 7)",
            "Coluna D (Ação 5): 'Contribuir para a elaboração do Manual de Boas Práticas e Integridade' (Prazo: 180 dias; Evidência: Minuta protocolada).\n"
            "Coluna E (Ação 7): Canal oficial OESPA/STC e Decreto 39.054/2024.\n"
            "Coluna F: Coexecutores: CG, Equidade, SGRH e ESAP.",
            "Sem Conflito:\nAtuação em rede com os órgãos legítimos do Estado."
        ),
        (
            "4. Capacitação em Escuta Ativa e CNV (Aba 'Inclusões a Deliberar'):\n"
            "Sugeriu formação periódica em Comunicação Não Violenta e acolhimento humanizado para Ouvidoria e setores de atendimento.",
            "Incorporada na Planilha da ESAP (Ação nº 89 sob E9.O2.KR1)",
            "Coluna D (ESAP): 'Promover oficinas práticas de Oratória Forense, Escuta Ativa/CNV e Media Training para membros e servidores'.\n"
            "Coluna E: '...cursos de acolhimento humanizado, Escuta Ativa e Comunicação Não Violenta - CNV (em parceria com a Ouvidoria e Comitê de Equidade)'.",
            "Harmonizado:\nESAP assume a liderança pedagógica com Ouvidoria parceira."
        ),
        (
            "5. Cartilha da Ouvidoria (Aba 'Inclusões a Deliberar'):\n"
            "Sugeriu material informativo e cartilha didática sobre canais e direitos do usuário com a ASCOM.",
            "Planilha da Ouvidoria (Ação 10 sob E8.O2.KR2) e Ação de ASCOM",
            "Coluna E (Ação 10 da Ouvidoria): Contemplada como produto de transparência ativa e fomento ao controle social.\n"
            "Articulada à ASCOM como campanha de conscientização da cidadania.",
            "Sem Conflito:\nProduto direto de transparência pública."
        ),
        (
            "6. 8ª Coluna de Produtos e Evidências:\n"
            "Dra. Martha restabeleceu uma coluna própria para aferição dos produtos sob sua governabilidade direta.",
            "Preservada Integralmente na Coluna E (Subação / Metodologia - COMO)",
            "Todas as evidências exigidas (relatórios semestrais anonimizados, comprovantes de remessa à CG, minutas entregues e checklists aplicados) foram transpostas para o corpo da Coluna E, mantendo o padrão oficial de 7 colunas.",
            "Harmonizado:\nEvidências mantidas sem romper a estrutura do banco e relatórios."
        )
    ]

    for item in itens_ouv:
        row = t_ouv.add_row()
        for idx, text in enumerate(item):
            c = row.cells[idx]
            c.width = col_w_ouv[idx]
            set_cell_margins(c, 60, 60, 80, 80)
            set_cell_background(c, "F0FDFA" if idx == 0 else "FFFFFF")
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif idx == 3:
                r.font.color.rgb = RGBColor(0x04, 0x78, 0x57) # Green

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SEÇÃO 4: DEMONSTRAÇÃO DE AUSÊNCIA DE CONFLITOS INTERSETORIAIS ---
    h4 = doc.add_heading(level=1)
    r_h4 = h4.add_run("4. MATRIZ DE AUSÊNCIA DE CONFLITOS COM RESPONSABILIDADES SANEADAS")
    r_h4.font.bold = True
    r_h4.font.size = Pt(12)
    r_h4.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_conf_intro = doc.add_paragraph()
    p_conf_intro.add_run(
        "A garantia da eficácia do Planejamento Estratégico reside na inexistência de superposição ou litígios de competência. "
        "A tabela a seguir comprova que cada unidade afetada pelas propostas da ASCOM e da Ouvidoria teve seu papel "
        "delimitado com estrita precisão técnica:"
    )

    t_conf = doc.add_table(rows=1, cols=3)
    t_conf.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_conf.autofit = False
    set_table_borders(t_conf)

    col_w_conf = [Inches(2.0), Inches(2.3), Inches(2.6)]
    headers_conf = [
        "Unidade Correlata",
        "Ponto de Contato com ASCOM / Ouvidoria",
        "Garantia de Não Conflito no SGPE PGE-MA"
    ]
    hdr_row_c = t_conf.rows[0]
    for i, h in enumerate(headers_conf):
        cell = hdr_row_c.cells[i]
        cell.width = col_w_conf[i]
        set_cell_background(cell, "334155") # Slate-700
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    itens_conf = [
        (
            "Corregedoria-Geral (CG)",
            "Tratamento de Denúncias Funcionais (E8.O2.KR1) e Manual de Boas Práticas.",
            "Não há conflito: A CG retém a competência privativa de instaurar sindicâncias e PADs. A Ouvidoria atua estritamente no recebimento e encaminhamento conclusivo (30 dias). No Manual de Boas Práticas, atuam como coexecutoras paritárias."
        ),
        (
            "Procuradorias Especializadas Contenciosas (15 Unidades)",
            "Fornecimento de decisões favoráveis (E6.O1.KR2) e respostas a pedidos da Ouvidoria (E4.O1.KR3).",
            "Não há conflito: As Especializadas não têm metas de alcance de redes sociais nem de ouvidoria em seus relatórios executivos. Atuam como Fornecedoras de Insumo no fluxo oficial disciplinado pela futura Portaria do PG."
        ),
        (
            "Escola Superior (ESAP)",
            "Capacitação institucional (E9.O2.KR1), Media Training, Escuta Ativa/CNV e eventos.",
            "Não há conflito: A ESAP lidera a governança pedagógica e a meta macro de 40% da PGE. A ASCOM e Ouvidoria atuam como demandantes no PAC e parceiras conteudistas em oficinas específicas, sem concorrência."
        ),
        (
            "Assessoria em TIC da PGAAE e Supervisão de Informática (SI)",
            "Extranet (E6.O1.KR1), painéis de BI e caixas no SPA/SEI.",
            "Não há conflito: A ASCOM e Ouvidoria condicionaram suas ações à viabilidade técnica de TIC ('se tecnicamente possível'). A TIC mantém a gestão de sistemas/sítios e a SI a infraestrutura física de hospedagem."
        ),
        (
            "Conselho Superior (CS)",
            "Meta de Honorários Sucumbenciais (E9.O3.KR1).",
            "Não há conflito: O Conselho Superior é o Líder Exclusivo do incremento de 15% de honorários. A Ouvidoria e ASCOM não possuem qualquer interferência nessa frente."
        ),
        (
            "Gabinete do Procurador-Geral",
            "Portaria de fluxo de êxitos, Manual de Integridade e Cerimonial de Eventos.",
            "Não há conflito: A ASCOM e Ouvidoria elaboram as minutas técnicas. A prerrogativa política e jurídica de edição dos atos normativos permanece 100% concentrada no Procurador-Geral do Estado."
        )
    ]

    for item in itens_conf:
        row = t_conf.add_row()
        for idx, text in enumerate(item):
            c = row.cells[idx]
            c.width = col_w_conf[idx]
            set_cell_margins(c, 60, 60, 80, 80)
            set_cell_background(c, "F8FAFC" if idx == 0 else "FFFFFF")
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SEÇÃO 5: CONCLUSÃO E ENCAMINHAMENTOS ---
    h5 = doc.add_heading(level=1)
    r_h5 = h5.add_run("5. CONCLUSÃO E AVALIAÇÃO DE EXEQUIVILIDADE")
    r_h5.font.bold = True
    r_h5.font.size = Pt(12)
    r_h5.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_concl = doc.add_paragraph()
    p_concl.add_run(
        "A análise detida das propostas da Dra. Martha Jackson demonstra elevado rigor técnico e metodológico, "
        "tendo suas ponderações contribuído decisivamente para o aperfeiçoamento da governança da PGE-MA. "
        "A transposição realizada pelo SGPE garantiu que: "
    )
    
    bullets = [
        ("Nenhuma meta cega ou inexequível ", "fosse imputada à ASCOM ou Ouvidoria sem prévia linha de base;"),
        ("As evidências de cumprimento ", "fossem estritamente vinculadas aos atos sob governabilidade da chefia das unidades;"),
        ("A integridade dos fluxos estaduais ", "fosse resguardada, especialmente os canais oficiais de integridade e a competência disciplinar da Corregedoria;"),
        ("A compatibilidade técnica ", "fosse assegurada em 100% dos artefatos: todas as 41 planilhas .xlsx, o banco SQLite estruturado e o portal interativo do GitHub Pages já refletem com exatidão esse modelo saneado.")
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r_bt = bp.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        bp.add_run(b_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Assinatura institucional
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign1 = p_sign.add_run("São Luís (MA), 09 de novembro de 2026.\n\n")
    r_sign1.font.size = Pt(9.5)
    r_sign1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    r_sign2 = p_sign.add_run("COORDENAÇÃO DO PLANEJAMENTO ESTRATÉGICO\n")
    r_sign2.font.bold = True
    r_sign2.font.size = Pt(10)
    r_sign2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_sign3 = p_sign.add_run("Sistema de Governança e Planejamento Estratégico (SGPE PGE-MA)")
    r_sign3.font.size = Pt(9)
    r_sign3.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Salva documento
    OUTPUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_DOCX))
    doc.save(str(ROOT_DOCX))
    print(f"Documento gerado com sucesso em:\n- {OUTPUT_DOCX}\n- {ROOT_DOCX}")

if __name__ == "__main__":
    build_docx()
