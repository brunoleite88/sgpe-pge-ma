# -*- coding: utf-8 -*-
"""
Script de Equalização Completa das 7 Assimetrias e Correlações Intersetoriais:
1. E6.O1.KR2 (Fluxo quinzenal de envio de vitórias/atuações relevantes à ASCOM):
   - Adiciona em: PA, PDA, PEDU, PERJP, PJEFP, PPIMA, PSP, NCIA, NIRF, SGA, ASJUR.
2. E5.O2.KR2 (Aumentar em 20% a taxa de conhecimento de recursos nos Tribunais Superiores):
   - Adiciona em: PJ, PT, PA, PCF, PDA, PERJP, PPIMA, PSP, SGA.
3. E5.O5.KR2 (Reduzir em 50% o tempo de elaboração de peças e documentos jurídicos padronizados):
   - Adiciona em: PJ, PB, ASJUR, NCIA, SGA.
4. E4.O1.KR1 (Responder ao menos 90% das consultas dos órgãos estaduais dentro do prazo regulamentar):
   - Adiciona em: PSAU, PGAAJ.
5. E7.O3.KR3 (Certificar 25% dos servidores da área de tecnologia nas principais competências digitais):
   - Expurga das 7 procuradorias jurídicas (PA, PCF, PDA, PERJP, PRI, PRT, PT), mantendo restrito a SI, PGAAE, ESAP e SGRH.
6. E9.O3.KR1 (Aumentar em 15% a arrecadação de honorários sucumbenciais):
   - Adiciona nas Especializadas/Regionais/Núcleos contenciosos faltantes: PJ, PT, PA, PEDU, PSAU, PSP, PPIMA, PB, PRI, PRT, NCIA, NIRF, SGA.
7. E8.O2.KR1 e E8.O2.KR3 (Integridade/Combate ao Assédio e Redução de 40% da reincidência em correições):
   - E8.O2.KR1: inclui ação espelho em CEQUIDADE e ESAP.
   - E8.O2.KR3: inclui ação espelho de supervisão de recomendações correcionais em SGA e PGAAJ.
8. Sincroniza todas as cópias .xlsx e atualiza Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

from saneamento_ascom_e_ti import (
    UNIT_FOLDERS, load_rows, write_sheet_to_all_targets
)

# 1. E6.O1.KR2 - Fluxo quinzenal de vitórias/atuações relevantes para ASCOM
E6_O1_KR2_ADD = {
    "PA": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com decisões e pareceres relevantes",
        "Instituir rotina setorial quinzenal de envio de relatórios sintéticos e cópias de decisões favoráveis em licitações, concursos e servidores públicos à ASCOM, viabilizando a divulgação institucional da atuação da PGE-MA.",
        "Líder: Procuradoria Administrativa (PA); Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PDA": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com resultados de arrecadação, protesto e transações fiscais",
        "Instituir rotina quinzenal de envio de dados consolidados de recuperação da dívida ativa, editais de transação tributária e grandes bloqueios/execuções fiscais à ASCOM para divulgação institucional.",
        "Líder: Procuradoria da Dívida Ativa (PDA); Coexecutores: NIRF, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PEDU": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com decisões e atuações relevantes na Educação",
        "Instituir rotina setorial quinzenal de envio de decisões favoráveis, acordos e atuações estruturantes em políticas públicas educacionais à ASCOM, fortalecendo a transparência ativa da PGE-MA.",
        "Líder: Procuradoria da Educação (PEDU); Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PERJP": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com resultados de economia ao erário em execuções e precatórios",
        "Instituir rotina quinzenal de envio de resultados de economia gerada em impugnações de cálculos (art. 535 CPC), deságios em acordos de precatórios e prevenção de sequestros judiciais à ASCOM.",
        "Líder: Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP); Coexecutores: Núcleo de Cálculos, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PJEFP": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com vitórias em demandas repetitivas e Turmas Recursais",
        "Instituir rotina quinzenal de envio de acórdãos paradigmáticos das Turmas Recursais e Incidentes de Uniformização favoráveis ao Estado à ASCOM para divulgação institucional.",
        "Líder: Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP); Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PPIMA": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com vitórias na defesa do patrimônio público e meio ambiente",
        "Instituir rotina setorial quinzenal de envio de decisões relevantes de retomada de imóveis públicos, regularização fundiária e tutela ambiental à ASCOM para divulgação institucional.",
        "Líder: Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA); Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "PSP": (
        "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com decisões favoráveis na área de Segurança Pública",
        "Instituir rotina setorial quinzenal de envio de sentenças e acórdãos relevantes em concursos policiais, processos disciplinares e defesa das corporações estaduais à ASCOM.",
        "Líder: Procuradoria da Segurança Pública (PSP); Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "NCIA": (
        "Alimentação sistemática da ASCOM com ações de improbidade, ANPCs e vídeos de sustentações orais",
        "Remeter quinzenalmente à ASCOM sínteses de Acordos de Não Persecução Cível (ANPC), ressarcimentos ao erário, cartilhas de integridade e links/minutagens de sustentações orais no YouTube (observado o sigilo legal quando aplicável).",
        "Líder: Núcleo de Combate à Improbidade Administrativa (NCIA); Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "NIRF": (
        "Alimentação sistemática da ASCOM com resultados de inteligência fiscal e recuperação de ativos ocultos",
        "Encaminhar quinzenalmente à ASCOM, em conjunto com a PDA e resguardado o sigilo fiscal, balanços de operações de recuperação de créditos e combate à fraude fiscal para divulgação institucional.",
        "Líder: Núcleo de Inteligência e Recuperação Fiscal (NIRF); Coexecutores: Procuradoria da Dívida Ativa (PDA), Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "SGA": (
        "Coordenar o fluxo das Especializadas e o envio de links de sustentações orais no YouTube à ASCOM",
        "Supervisionar o envio quinzenal de decisões de impacto pelas Procuradorias Especializadas e encaminhar à ASCOM os links e minutagens das sustentações orais realizadas por procuradores nos canais do YouTube dos Tribunais.",
        "Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: Procuradorias Especializadas, Assessoria de Comunicação (ASCOM)",
        "Fluxo Quinzenal / Contínuo"
    ),
    "ASJUR": (
        "Alimentação sistemática da ASCOM com pareceres referenciais, minutas-padrão e marcos normativos relevantes",
        "Encaminhar quinzenalmente à ASCOM sínteses de pareceres normativos, orientações jurídicas estratégicas e atos governamentais de interesse público validados pela Consultoria-Geral.",
        "Líder: Assessoria Jurídica / Consultoria-Geral; Coexecutores: Assessoria de Comunicação (ASCOM), Gabinete do Procurador-Geral",
        "Fluxo Quinzenal / Contínuo"
    ),
}

# 2. E5.O2.KR2 - Aumentar em 20% a taxa de conhecimento de recursos nos Tribunais Superiores
E5_O2_KR2_ADD = {
    "PJ": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários aplicando o filtro de superação das Súmulas 7/STJ e 279/STF",
        "Aplicar checklist de admissibilidade recursal, prequestionamento explícito e distinção (distinguishing) na redação de REsp e RE no contencioso cível, observando as diretrizes do Relatório Semestral de Superação de Óbices da Procuradoria de Brasília.",
        "Líder: Procuradoria Judicial (PJ); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PT": (
        "Qualificar a interposição de Recursos de Revista e Agravos de Instrumento ao TST superando o óbice da Súmula 126/TST",
        "Aplicar checklist rigoroso de transcendência, prequestionamento fático-probatório no TRT16 e demonstração de violação literal/divergência válida para ampliar o conhecimento de recursos trabalhistas no TST e STF (Tema 246).",
        "Líder: Procuradoria Trabalhista (PT); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PA": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em matéria administrativa e de servidores públicos",
        "Aplicar checklist prévio de admissibilidade e diretrizes do Relatório Semestral da Procuradoria de Brasília para evitar o não conhecimento por óbices formais (Súmulas 7/STJ, 279/STF e 280/STF).",
        "Líder: Procuradoria Administrativa (PA); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PCF": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em matéria tributária e financeira",
        "Padronizar a demonstração de repercussão geral, prequestionamento de dispositivos constitucionais/federais e superação das Súmulas 7/STJ e 279/STF nos recursos fiscais encaminhados ao STJ e STF.",
        "Líder: Procuradoria do Contencioso Fiscal (PCF); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PDA": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em execuções fiscais e embargos à execução",
        "Aplicar checklist de admissibilidade e prequestionamento explícito da Lei 6.830/1980 e CTN, alinhado ao Relatório Semestral de Superação de Óbices da Procuradoria de Brasília.",
        "Líder: Procuradoria da Dívida Ativa (PDA); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PERJP": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em matéria de execuções, precatórios e índices de correção",
        "Aplicar checklist de admissibilidade e demonstração de teses vinculantes (EC 113/2021, Temas 810 e 1170/STF) para garantir o conhecimento de recursos da Fazenda Pública nos Tribunais Superiores.",
        "Líder: Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PPIMA": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em matéria fundiária, dominial e ambiental",
        "Assegurar o prequestionamento na instância ordinária e a correta qualificação jurídica da prova dominial/ambiental para superar os óbices das Súmulas 7/STJ e 279/STF em articulação com a Procuradoria de Brasília.",
        "Líder: Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "PSP": (
        "Qualificar a interposição de Recursos Especiais e Extraordinários em demandas da Segurança Pública e concursos militares",
        "Aplicar checklist de admissibilidade recursal e alinhamento aos precedentes do STF/STJ sobre controle judicial de concursos e PAD militar, em consonância com o Relatório Semestral da Procuradoria de Brasília.",
        "Líder: Procuradoria da Segurança Pública (PSP); Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo até 2028"
    ),
    "SGA": (
        "Coordenar com a Procuradoria de Brasília a metodologia de mensuração de admissibilidade recursal e difusão do Relatório Semestral de Óbices",
        "Estabelecer matriz metodológica conjunta com a PB para aferir a taxa de conhecimento recursal por especializada e difundir semestralmente as diretrizes técnicas de superação das Súmulas 7/STJ, 279/STF e 126/TST.",
        "Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: Procuradoria de Brasília (PB), PGAAJ, Especializadas Contenciosas",
        "Semestral até 2028"
    ),
}

# 3. E5.O5.KR2 - Reduzir em 50% o tempo de elaboração de peças e documentos jurídicos padronizados
E5_O5_KR2_ADD = {
    "PJ": (
        "Sistematizar banco de minutas padronizadas cíveis e modelos assistidos por IA (Minuta IA) no SPA",
        "Catalogar e atualizar modelos parametrizados de contestações, apelações e contrarrazões para as matérias repetitivas dos Grupos 1 e 2 da Procuradoria Judicial, reduzindo em ao menos 50% o tempo de redação.",
        "Líder: Procuradoria Judicial (PJ); Coexecutores: Assessoria em TIC da PGAAE / INOVA, Subprocuradoria-Geral Adjunta (SGA)",
        "180 dias / Contínuo até 2029"
    ),
    "PB": (
        "Estruturar repositório padronizado de minutas de agravos internos, memoriais, cotas de dispensa e contrarrazões nos Tribunais Superiores",
        "Padronizar modelos estruturados e resumos executivos adaptados à triagem de IA do STF (VICTOR) e STJ (SÓCRATES), reduzindo o tempo de elaboração documental na Procuradoria de Brasília.",
        "Líder: Procuradoria de Brasília (PB); Coexecutores: Assessoria em TIC da PGAAE / INOVA, Subprocuradoria-Geral Adjunta (SGA)",
        "180 dias / Contínuo até 2029"
    ),
    "ASJUR": (
        "Consolidar repositório de minutas-padrão de editais, contratos, convênios e pareceres referenciais no SEI/SPA",
        "Manter atualizado banco institucional de minutas padronizadas da Lei nº 14.133/2021 e listas de verificação (checklists), reduzindo em 50% o tempo de análise consultiva repetitiva.",
        "Líder: Assessoria Jurídica / Consultoria-Geral; Coexecutores: Assessoria em TIC da PGAAE / INOVA, Comissão Setorial de Licitação (CSL)",
        "180 dias / Contínuo até 2029"
    ),
    "NCIA": (
        "Padronizar modelos de petições iniciais de improbidade, minutas de ANPC e checklists de instrução patrimonial",
        "Criar biblioteca setorial de peças estruturadas, cláusulas-padrão de Acordos de Não Persecução Cível (ANPC) e roteiros de bloqueio cautelar de ativos com apoio de IA generativa.",
        "Líder: Núcleo de Combate à Improbidade Administrativa (NCIA); Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Assessoria em TIC da PGAAE / INOVA",
        "180 dias / Contínuo até 2029"
    ),
    "SGA": (
        "Supervisionar a padronização e unificação dos bancos de peças, teses e enunciados das Procuradorias Especializadas",
        "Coordenar a revisão periódica dos modelos de peças contenciosas e cotas de dispensa recursal integrados ao Assistente de Petição e à ferramenta Minuta IA no SPA.",
        "Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: PGAAJ, Procuradorias Especializadas, Assessoria em TIC da PGAAE / INOVA",
        "Semestral até 2029"
    ),
}

# 4. E4.O1.KR1 - Responder ao menos 90% das consultas dos órgãos estaduais dentro do prazo regulamentar
E4_O1_KR1_ADD = {
    "PSAU": (
        "Garantir resposta tempestiva a ao menos 90% das consultas e orientações jurídicas da SES e CEMARC dentro do prazo regulamentar",
        "Monitorar no SEI/SPA o cumprimento dos prazos regulamentares nas consultas sobre aquisições de medicamentos, regulação sanitária e cumprimento de decisões, articulado às cartilhas preventivas da saúde.",
        "Líder: Procuradoria da Saúde (PSAU); Coexecutores: PGAAJ, Secretaria de Estado da Saúde (SES)",
        "Contínuo até 2030"
    ),
    "PGAAJ": (
        "Supervisionar o cumprimento do SLA regulamentar de 90% nas respostas a consultas jurídicas pelas unidades vinculadas",
        "Acompanhar mensalmente o painel de tempestividade consultiva das Procuradorias Especializadas e promover a uniformização de entendimentos para destravar expedientes complexos.",
        "Líder: Procurador-Geral Adjunto para Assuntos Jurídicos (PGAAJ); Coexecutores: Assessoria Jurídica, Procuradorias Especializadas",
        "Mensal / Contínuo até 2030"
    ),
}

# 5. E7.O3.KR3 - Unidades jurídicas das quais o KR de certificação de TI deve ser expurgado
E7_O3_KR3_REMOVE_UNITS = {"PA", "PCF", "PDA", "PERJP", "PRI", "PRT", "PT"}

# 6. E9.O3.KR1 - Aumentar em 15% a arrecadação de honorários sucumbenciais até 2029
E9_O3_KR1_ADD_UNITS = [
    ("PJ", "Procuradoria Judicial (PJ)", "ações cíveis e fazendárias ordinárias"),
    ("PT", "Procuradoria Trabalhista (PT)", "reclamações trabalhistas julgadas improcedentes e ações rescisórias"),
    ("PA", "Procuradoria Administrativa (PA)", "ações ordinárias e mandados de segurança com condenação sucumbencial"),
    ("PEDU", "Procuradoria da Educação (PEDU)", "demandas judiciais da área educacional com sucumbência favorável ao Estado"),
    ("PSAU", "Procuradoria da Saúde (PSAU)", "demandas sanitárias julgadas improcedentes ou extintas com sucumbência"),
    ("PSP", "Procuradoria da Segurança Pública (PSP)", "ações ordinárias e anulatórias da área de segurança pública"),
    ("PPIMA", "Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA)", "ações possessórias, dominiais, desapropriações e ambientais"),
    ("PB", "Procuradoria de Brasília (PB)", "acórdãos do STF, STJ e TST com fixação ou majoração de honorários recursais (art. 85, § 11, do CPC)"),
    ("PRI", "Procuradoria Regional de Imperatriz (PRI)", "processos cíveis, fiscais e trabalhistas das comarcas do polo regional de Imperatriz"),
    ("PRT", "Procuradoria Regional de Timon (PRT)", "processos cíveis, fiscais e trabalhistas das comarcas do polo regional de Timon"),
    ("NCIA", "Núcleo de Combate à Improbidade Administrativa (NCIA)", "ações de improbidade, cumprimentos de sentença e cláusulas de ressarcimento/encargos"),
    ("NIRF", "Núcleo de Inteligência e Recuperação Fiscal (NIRF)", "operações de recuperação de ativos, execuções fiscais de grandes devedores e transações tributárias"),
    ("SGA", "Subprocuradoria-Geral Adjunta (SGA)", "todas as unidades contenciosas, padronizando o fluxo de remessa de certidões de honorários à PDA/PERJP"),
]

# 7. E8.O2.KR1 e E8.O2.KR3 - Integridade/Assédio e Recomendações Correcionais
E8_O2_KR1_ADD = {
    "CEQUIDADE": (
        "Coexecutar no mínimo 2 ações institucionais anuais de conscientização e enfrentamento ao assédio moral, sexual e à discriminação",
        "Atuar em parceria direta com a Ouvidoria-Geral, Corregedoria-Geral, SGRH e ESAP no planejamento e execução de campanhas, cartilhas e rodas de conversa sobre prevenção ao assédio (Decreto Estadual nº 39.054/2024).",
        "Líder: Ouvidoria-Geral e Comitê de Equidade; Coexecutores: Corregedoria-Geral, SGRH, ESAP, ASCOM",
        "Anual (mínimo de 2 ações/ano)"
    ),
    "ESAP": (
        "Ofertar suporte pedagógico e certificar as 2 ações institucionais anuais de letramento e prevenção ao assédio moral e sexual",
        "Incluir no calendário anual da ESAP os eventos, palestras e oficinas de ética, integridade e enfrentamento ao assédio moral e sexual demandados pela Ouvidoria-Geral, Corregedoria-Geral e Comitê de Equidade.",
        "Líder Pedagógico: Escola Superior da Advocacia Pública (ESAP); Coexecutores: Ouvidoria-Geral, Corregedoria-Geral, Comitê de Equidade, SGRH",
        "Anual (mínimo de 2 ações/ano)"
    ),
}

E8_O2_KR3_ADD = {
    "SGA": (
        "Acompanhar e cobrar o saneamento das recomendações correcionais nas Procuradorias Especializadas em até 90 dias",
        "Atuar em articulação com a Corregedoria-Geral para apoiar as chefias contenciosas na correção de fluxos e eliminação da reincidência de não conformidades apontadas em correições ordinárias.",
        "Líder: Corregedoria-Geral; Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Chefias das Especializadas",
        "Semestral (90 dias pós-correição)"
    ),
    "PGAAJ": (
        "Supervisionar a implementação dos planos corretivos pós-correição nas unidades jurídicas e consultivas vinculadas",
        "Monitorar junto às chefias setoriais o cumprimento tempestivo das recomendações da Corregedoria-Geral, prevenindo a reincidência de achados de auditoria correcional.",
        "Líder: Corregedoria-Geral; Coexecutores: Procurador-Geral Adjunto para Assuntos Jurídicos (PGAAJ), Unidades Correcionadas",
        "Semestral (90 dias pós-correição)"
    ),
}


def apply_all_correlations():
    md_additions = {
        "E6.O1.KR2": [],
        "E5.O2.KR2": [],
        "E5.O5.KR2": [],
        "E4.O1.KR1": [],
        "E9.O3.KR1": [],
        "E8.O2.KR1": [],
        "E8.O2.KR3": [],
    }
    e9_o3_dict = {u: (nome, escopo) for u, nome, escopo in E9_O3_KR1_ADD_UNITS}

    for sigla, folder_name in sorted(UNIT_FOLDERS.items()):
        cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
        rows, t1, t2 = load_rows(cons_path)

        # Item 5: Expurgar E7.O3.KR3 das 7 procuradorias jurídicas
        if sigla in E7_O3_KR3_REMOVE_UNITS:
            rows = [r for r in rows if "[E7.O3.KR3]" not in str(r[2] or "")]

        # Item 1: E6.O1.KR2
        if sigla in E6_O1_KR2_ADD and not any("[E6.O1.KR2]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E6_O1_KR2_ADD[sigla]
            rows.append([
                "Eixo Estratégico 6 – Fortalecer a imagem institucional e a comunicação com a sociedade",
                "O1: Fortalecer a imagem e o reconhecimento da PGE como referência de excelência",
                "[E6.O1.KR2] KR2: Alcançar crescimento contínuo do alcance médio mensal nas redes sociais da PGE até 2029",
                acao, como, quem, prazo
            ])
            md_additions["E6.O1.KR2"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 2: E5.O2.KR2
        if sigla in E5_O2_KR2_ADD and not any("[E5.O2.KR2]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E5_O2_KR2_ADD[sigla]
            rows.append([
                "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
                "O2: Assegurar a defesa jurídica do Estado e a conformidade legal",
                "[E5.O2.KR2] KR2: Aumentar em 20% a taxa de conhecimento de recursos da PGE nos Tribunais Superiores até 2028",
                acao, como, quem, prazo
            ])
            md_additions["E5.O2.KR2"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 3: E5.O5.KR2
        if sigla in E5_O5_KR2_ADD and not any("[E5.O5.KR2]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E5_O5_KR2_ADD[sigla]
            rows.append([
                "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
                "O5: Otimizar os fluxos de trabalho e aumentar a produtividade",
                "[E5.O5.KR2] KR2: Reduzir em 50% o tempo de elaboração de peças e documentos jurídicos padronizados até 2029",
                acao, como, quem, prazo
            ])
            md_additions["E5.O5.KR2"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 4: E4.O1.KR1
        if sigla in E4_O1_KR1_ADD and not any("[E4.O1.KR1]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E4_O1_KR1_ADD[sigla]
            rows.append([
                "Eixo Estratégico 4 – Melhorar a experiência do usuário dos serviços da PGE",
                "O1: Melhorar a experiência do usuário dos serviços da PGE",
                "[E4.O1.KR1] KR1: Responder ao menos 90% das consultas dos órgãos estaduais dentro do prazo regulamentar até 2030",
                acao, como, quem, prazo
            ])
            md_additions["E4.O1.KR1"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 6: E9.O3.KR1
        if sigla in e9_o3_dict and not any("[E9.O3.KR1]" in str(r[2] or "") for r in rows):
            nome_setor, escopo = e9_o3_dict[sigla]
            acao = "Requerer sistematicamente a fixação/majoração de honorários sucumbenciais e remeter certidões para cobrança/execução"
            como = (
                f"Formular pedidos expressos de fixação e majoração de honorários sucumbenciais (inclusive recursais, art. 85, § 11, do CPC) "
                f"em {escopo}, apurando o trânsito em julgado e encaminhando tempestivamente os dados/certidões à PDA e PERJP para cobrança, protesto ou compensação em favor do FUNPGE."
            )
            quem = f"Líder: {nome_setor}; Coexecutores: Procuradoria da Dívida Ativa (PDA), PERJP, Subprocuradoria-Geral Adjunta (SGA)"
            prazo = "Contínuo até 2029"
            rows.append([
                "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
                "O3: Ampliar a arrecadação de honorários sucumbenciais",
                "[E9.O3.KR1] KR1: Aumentar em 15% a arrecadação de honorários sucumbenciais até 2029",
                acao, como, quem, prazo
            ])
            md_additions["E9.O3.KR1"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 7a: E8.O2.KR1
        if sigla in E8_O2_KR1_ADD and not any("[E8.O2.KR1]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E8_O2_KR1_ADD[sigla]
            rows.append([
                "Eixo Estratégico 8 – Fomentar a sustentabilidade, a integridade e a responsabilidade social",
                "O2: Fortalecer a Governança e a Integridade Institucional",
                "[E8.O2.KR1] KR1: Garantir a apuração de 100% das denúncias e manifestações dentro do prazo legal até 2030",
                acao, como, quem, prazo
            ])
            md_additions["E8.O2.KR1"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        # Item 7b: E8.O2.KR3
        if sigla in E8_O2_KR3_ADD and not any("[E8.O2.KR3]" in str(r[2] or "") for r in rows):
            acao, como, quem, prazo = E8_O2_KR3_ADD[sigla]
            rows.append([
                "Eixo Estratégico 8 – Fomentar a sustentabilidade, a integridade e a responsabilidade social",
                "O2: Fortalecer a Governança e a Integridade Institucional",
                "[E8.O2.KR3] KR3: Reduzir em 40% a reincidência de não conformidades apontadas em correições ordinárias até 2030",
                acao, como, quem, prazo
            ])
            md_additions["E8.O2.KR3"].append(f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |")

        write_sheet_to_all_targets(sigla, t1, t2, rows)

    for k, v in md_additions.items():
        print(f"[{k}] Novas linhas adicionadas: {len(v)}")
    return md_additions


def update_cotejamento_markdown(md_additions):
    cot_path = os.path.join(BASE_DIR, "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md")
    with open(cot_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Remove the 7 legal units from E7.O3.KR3 table in Cotejamento
    lines = text.splitlines()
    filtered_lines = []
    in_e7_o3_kr3 = False
    removed_kr3_rows = 0
    legal_prefixes = (
        "| **Procuradoria Administrativa** |",
        "| **Procuradoria Regional de Imperatriz** |",
        "| **Procuradoria Regional de Timon** |",
        "| **Procuradoria Trabalhista** |",
        "| **Procuradoria da Dívida Ativa** |",
        "| **Procuradoria de Execuções e Requisições Judiciais de Pagamento** |",
        "| **Procuradoria do Contencioso Fiscal** |",
    )
    for line in lines:
        if "Código na Lista Mestre:** `E7.O3.KR3`" in line:
            in_e7_o3_kr3 = True
        elif in_e7_o3_kr3 and line.startswith("----------------------------------------"):
            in_e7_o3_kr3 = False

        if in_e7_o3_kr3 and line.startswith(legal_prefixes):
            removed_kr3_rows += 1
            continue
        filtered_lines.append(line)

    text = "\n".join(filtered_lines) + "\n"
    print(f"[E7.O3.KR3] Linhas de procuradorias jurídicas expurgadas do Cotejamento: {removed_kr3_rows}")

    # Update E7.O3.KR3 header metadata
    text = text.replace(
        "- **Unidades com Ações Mapeadas (11):** Escola Superior da Advocacia Pública (ESAP), Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE), Procuradoria Administrativa, Procuradoria Regional de Imperatriz, Procuradoria Regional de Timon, Procuradoria Trabalhista, Procuradoria da Dívida Ativa, Procuradoria de Execuções e Requisições Judiciais de Pagamento, Procuradoria do Contencioso Fiscal, Serviço de Gestão de Recursos Humanos, Supervisão de Informática\n- **Volume de Ações Setoriais:** 14 iniciativas",
        "- **Unidades com Ações Mapeadas (4):** Escola Superior da Advocacia Pública (ESAP), Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE), Serviço de Gestão de Recursos Humanos, Supervisão de Informática *(expurgadas as 7 procuradorias jurídicas por se tratar de certificação estrita para servidores da área de TIC)*\n- **Volume de Ações Setoriais:** 7 iniciativas"
    )

    # Helper to append rows at the end of a specific KR table (right before '> [!TIP]')
    def insert_rows_into_kr_section(full_text, kr_code, new_rows):
        if not new_rows:
            return full_text
        pattern = re.compile(
            rf"(- \*\*Código na Lista Mestre:\*\* `{re.escape(kr_code)}`.*?)(> \[!TIP\])",
            re.DOTALL
        )
        m = pattern.search(full_text)
        if not m:
            print(f"AVISO: Seção {kr_code} não localizada por regex.")
            return full_text
        section_body = m.group(1)
        to_add = [r for r in new_rows if r not in section_body]
        if not to_add:
            return full_text
        updated_body = section_body.rstrip() + "\n" + "\n".join(to_add) + "\n\n"
        return full_text[:m.start(1)] + updated_body + full_text[m.start(2):]

    for kr_code, rows_list in md_additions.items():
        text = insert_rows_into_kr_section(text, kr_code, rows_list)

    with open(cot_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md atualizado com todas as 7 simetrias.")


if __name__ == "__main__":
    additions = apply_all_correlations()
    update_cotejamento_markdown(additions)

