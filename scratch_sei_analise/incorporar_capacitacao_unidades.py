# -*- coding: utf-8 -*-
"""
Script de Equalização da Meta de Capacitação (Opção A):
1. E7.O3.KR2 ("Capacitar 25% do corpo funcional em Direito Digital e Inteligência Artificial até 2027"):
   - Incorpora ação de trilha de IA / Direito Digital nas unidades jurídicas/consultivas que estavam sem ela:
     ASJUR, NCIA, NIRF, PEDU, PSP, PPIMA, SGA, PGAAJ.
2. E9.O2.KR1 ("Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029"):
   - Incorpora ação simples e de governabilidade direta (levantar demandas anuais de capacitação da rotina do setor, encaminhar sugestões de cursos/trilhas à ESAP e SGRH para o PAC e viabilizar a participação de ao menos 40% da equipe) em todas as unidades operacionais e finalísticas que ainda não possuíam o E9.O2.KR1.
3. Sincroniza todas as cópias das planilhas (.xlsx) e atualiza o Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md.
"""
import os
import re
import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

from saneamento_ascom_e_ti import (
    UNIT_FOLDERS, load_rows, write_sheet_to_all_targets
)

# 1. Unidades jurídicas/consultivas que faltavam no E7.O3.KR2 (Direito Digital e IA):
E7_O3_KR2_MISSING = {
    "ASJUR": (
        "Propor e integrar trilhas de capacitação em Direito Digital, IA Generativa e Consultoria Pública Contemporânea",
        "Sugerir temas práticos à ESAP e inscrever procuradores e assessores da Consultoria/Assessoria Especial em oficinas sobre uso ético de Inteligência Artificial na redação de pareceres, engenharia de prompts jurídicos e análise de impacto regulatório.",
        "Líder: Assessoria Jurídica / Consultoria-Geral; Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "NCIA": (
        "Participar de trilhas de capacitação em Direito Digital, Inteligência Artificial e Investigação Patrimonial Tecnológica",
        "Indicar demandas formativas à ESAP e viabilizar a participação da equipe do NCIA em cursos sobre ferramentas de IA generativa, cruzamento de dados públicos, rastreamento de ativos e jurimetria aplicada à probidade administrativa.",
        "Líder: Núcleo de Combate à Improbidade Administrativa (NCIA); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "NIRF": (
        "Capacitar a equipe em Inteligência Artificial, Ciência de Dados Fiscais e Investigação Patrimonial Digital",
        "Encaminhar demandas formativas à ESAP e garantir a participação dos integrantes do NIRF em treinamentos de ferramentas analíticas, IA aplicada à recuperação de créditos, cruzamento de bancos de dados e automação fiscal.",
        "Líder: Núcleo de Inteligência e Recuperação Fiscal (NIRF); Coexecutores: ESAP, Procuradoria da Dívida Ativa (PDA), Assessoria em TIC da PGAAE / INOVA"
    ),
    "PEDU": (
        "Incluir a equipe da PEDU em trilhas continuadas de Direito Digital e Inteligência Artificial aplicada ao contencioso e consultivo educacional",
        "Sugerir módulos práticos à ESAP/EGMA e inscrever procuradores e assessores em oficinas de IA generativa (Minuta IA), gestão de fluxos no SPA/PJe e automação de peças padronizadas da área de educação pública.",
        "Líder: Procuradoria da Educação (PEDU); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "PSP": (
        "Incluir a equipe da PSP em trilhas continuadas de Direito Digital e Inteligência Artificial aplicada à Segurança Pública",
        "Sugerir módulos práticos à ESAP/EGMA e inscrever procuradores e assessores em oficinas de IA generativa, automação de contestações e pareceres repetitivos (PAD/concursos militares) e gestão eletrônica no SPA.",
        "Líder: Procuradoria da Segurança Pública (PSP); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "PPIMA": (
        "Capacitar a equipe da PPIMA em Direito Digital, Inteligência Artificial e Geotecnologias aplicadas ao Patrimônio e Meio Ambiente",
        "Sugerir cursos específicos à ESAP e viabilizar a participação da equipe em treinamentos de IA generativa para análise documental fundiária, sistemas de georreferenciamento (SIG/CAR) e gestão eletrônica de processos estruturais.",
        "Líder: Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "SGA": (
        "Fomentar e indicar trilhas de capacitação em Direito Digital, IA e Jurimetria para as unidades contenciosas",
        "Articular junto à ESAP e ao Laboratório INOVA a oferta de oficinas práticas de IA generativa, biblioteca de prompts e jurimetria estratégica para procuradores e assessores vinculados à Subprocuradoria-Geral de Assuntos Jurídicos.",
        "Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
    "PGAAJ": (
        "Articular demandas de capacitação em Direito Digital e Inteligência Artificial para as unidades jurídicas coordenadas",
        "Consolidar sugestões temáticas junto às Procuradorias Especializadas e propor à ESAP trilhas práticas de automação jurídica, uso seguro de IA generativa e gestão digital de acervo.",
        "Líder: Procurador-Geral Adjunto para Assuntos Jurídicos (PGAAJ); Coexecutores: ESAP, Assessoria em TIC da PGAAE / INOVA"
    ),
}

# 2. Customização temática de E9.O2.KR1 ("Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029")
# para todas as unidades (exceto ESAP e SGRH, que já possuem as ações estruturantes de E9.O2.KR1):
E9_O2_KR1_THEMES = {
    "ASCOM": ("comunicação pública digital, linguagem simples, produção audiovisual, redes sociais no setor público e assessoria de imprensa jurídica", "Assessoria de Comunicação (ASCOM)"),
    "ASJUR": ("direito administrativo contemporâneo, técnica legislativa, nova Lei de Licitações (Lei 14.133/2021) e redação de pareceres referenciais", "Assessoria Jurídica / Consultoria-Geral"),
    "CEQUIDADE": ("letramento racial e de gênero, direitos humanos, acessibilidade, inclusão e prevenção ao assédio e à discriminação no serviço público", "Comitê de Equidade"),
    "CG": ("direito administrativo disciplinar, auditoria correcional, sindicâncias, processo ético, LGPD e gestão de riscos", "Corregedoria-Geral (CG)"),
    "CS": ("governança colegiada, processo administrativo disciplinar e regulação da carreira da Advocacia Pública", "Conselho Superior da PGE"),
    "CSL": ("Nova Lei de Licitações e Contratos (Lei 14.133/2021), formação de pregoeiros/agentes de contratação, pesquisa de preços, ETP e gestão de riscos nas contratações", "Comissão Setorial de Licitação (CSL)"),
    "GAB": ("governança pública, gestão estratégica, assessoramento executivo, cerimonial institucional e tramitação avançada no SEI", "Gabinete do Procurador-Geral"),
    "NC": ("cálculos judiciais complexos da Fazenda Pública, atualização monetária/juros (EC 113/2021), PJe-Calc, perícias contábeis e liquidação de sentenças", "Núcleo de Cálculos (NC)"),
    "NCIA": ("tutela da probidade administrativa (Lei 8.429/1992 reformada), Acordos de Não Persecução Cível (ANPC), recuperação de ativos e processo estrutural", "Núcleo de Combate à Improbidade Administrativa (NCIA)"),
    "NIRF": ("inteligência fiscal, investigação patrimonial avançada, fraude à execução fiscal, responsabilidade tributária de grupos econômicos e transação tributária", "Núcleo de Inteligência e Recuperação Fiscal (NIRF)"),
    "OUV": ("gestão de ouvidorias públicas (Lei 13.460/2017), atendimento humanizado, mediação de conflitos, Lei de Acesso à Informação (LAI), LGPD e acolhimento de denúncias de assédio", "Ouvidoria-Geral da PGE"),
    "PA": ("Direito Administrativo, regime jurídico de servidores públicos, licitações e contratos administrativos (Lei 14.133/2021) e responsabilidade civil do Estado", "Procuradoria Administrativa (PA)"),
    "PB": ("técnica recursal avançada perante o STF e o STJ, repercussão geral, recursos repetitivos, superação de óbices sumulares e sustentação oral nas Cortes Superiores", "Procuradoria de Brasília (PB)"),
    "PCF": ("Direito Tributário Constitucional, Reforma Tributária (EC 132/2023 - IBS/CBS), contencioso fiscal de grande porte e teses vinculantes em matéria tributária", "Procuradoria do Contencioso Fiscal (PCF)"),
    "PDA": ("cobrança estratégica da Dívida Ativa, transação tributária, protesto extrajudicial, penhora de ativos e execução fiscal eficiente (Tema 1184/STF)", "Procuradoria da Dívida Ativa (PDA)"),
    "PEDU": ("Direito à Educação, financiamento educacional (FUNDEB), contratações temporárias de magistério, estatuto do magistério e controle judicial de políticas educacionais", "Procuradoria da Educação (PEDU)"),
    "PERJP": ("execução contra a Fazenda Pública (art. 535 do CPC), regime constitucional de Precatórios e RPVs, impugnação de cálculos e acordos diretos", "Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP)"),
    "PGA": ("gestão pública contemporânea, governança administrativa, planejamento orçamentário e liderança no setor público", "Procurador-Geral Adjunto para Assuntos Administrativos (PGA)"),
    "PGAAE": ("gestão estratégica orientada a resultados (OKRs), gerenciamento de projetos públicos (PMBOK/Ágil), captação de recursos (BID/Profisco) e transformação digital", "Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE)"),
    "PGAAJ": ("coordenação jurídica estratégica, gestão de precedentes qualificados, uniformização de jurisprudência administrativa e eficiência contenciosa", "Procurador-Geral Adjunto para Assuntos Jurídicos (PGAAJ)"),
    "PGARI": ("articulação interinstitucional, relações governamentais e federativas (CONPEG/FONACRI), autocomposição e mediação de conflitos socioambientais e fundiários", "Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI)"),
    "PJ": ("processo civil estratégico da Fazenda Pública, tutelas provisórias, ações coletivas e estruturais, recursos cíveis e precedentes vinculantes", "Procuradoria Judicial (PJ)"),
    "PJEFP": ("rito dos Juizados Especiais da Fazenda Pública (Lei 12.153/2009), Turmas Recursais, Incidentes de Uniformização de Jurisprudência e gestão de contencioso de massa", "Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP)"),
    "PPIMA": ("Direito Ambiental, regularização fundiária, patrimônio imobiliário público, desapropriações, licenciamento ambiental e litígios estruturais possessórios", "Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA)"),
    "PRI": ("atuação contenciosa regionalizada, processo civil da Fazenda Pública, execução fiscal, Direito do Trabalho público e sustentação oral", "Procuradoria Regional de Imperatriz (PRI)"),
    "PRT": ("atuação contenciosa regionalizada, processo civil da Fazenda Pública, execução fiscal, Direito do Trabalho público e sustentação oral", "Procuradoria Regional de Timon (PRT)"),
    "PSAU": ("Direito Sanitário, judicialização da saúde pública (Temas 793 e 1234 do STF), regulação do SUS/RENAME, NATJus e compras públicas de medicamentos", "Procuradoria da Saúde (PSAU)"),
    "PSP": ("Direito Administrativo Militar, processos disciplinares da Segurança Pública, concursos policiais e responsabilidade civil em operações policiais", "Procuradoria da Segurança Pública (PSP)"),
    "PT": ("Direito e Processo do Trabalho aplicados à Administração Pública, terceirização e responsabilidade subsidiária (Tema 246/STF), recursos ao TST e cálculos no PJe-Calc", "Procuradoria Trabalhista (PT)"),
    "SCC": ("gestão e fiscalização de contratos administrativos (Lei 14.133/2021), reequilíbrio econômico-financeiro, repactuação, aditivos e sanções contratuais", "Serviço de Controle de Contratos (SCC)"),
    "SCCF": ("contabilidade pública aplicada, conformidade financeira e contratual, retenções tributárias na fonte, SIAFE e controle de pagamentos de RPVs/dativos", "Serviço de Controle Contábil-Financeiro (SCCF)"),
    "SDD": ("gestão documental, protocolo eletrônico (SEI e SPA), triagem e classificação processual, digitalização com OCR e tabela de temporalidade de arquivos", "Serviço de Digitalização e Distribuição (SDD)"),
    "SEO": ("orçamento público (PPA, LDO e LOA), execução orçamentária e financeira no SIAFE, empenho, liquidação, Restos a Pagar e gestão de fundos especiais (FUNPGE)", "Serviço de Execução Orçamentária (SEO)"),
    "SGA": ("gestão de contencioso estratégico, sistema de precedentes (IRDR/IAC/Repetitivos), admissibilidade recursal e governança das Procuradorias Especializadas", "Subprocuradoria-Geral Adjunta (SGA)"),
    "SGT": ("logística administrativa, gestão de frotas e manutenção predial sustentável, segurança do trabalho, direção defensiva e fiscalização de serviços terceirizados", "Serviços Gerais e Transportes (SGT)"),
    "SI": ("infraestrutura de redes, segurança da informação, administração de servidores, virtualização (Nutanix/VMware), backup corporativo (Veeam) e governança de TIC (PDTIC)", "Supervisão de Informática (SI)"),
    "SMP": ("gestão patrimonial e de almoxarifado no setor público, inventário de bens móveis e imóveis, depreciação contábil, desfazimento de inservíveis e compras sustentáveis", "Serviço de Material e Patrimônio (SMP)"),
    "UGAM": ("planejamento de contratações anuais (PCA), governança administrativa, execução orçamentária, gestão de compras e logística pública integrada", "Unidade Gestora de Atividade Meio (UGAM)"),
    "USF": ("gestão financeira e orçamentária pública, conformidade contábil no SIAFE, prestação de contas ao TCE-MA, controle de RPVs e execução do FUNPGE", "Unidade Setorial de Finanças (USF)"),
}

def update_all_sheets():
    added_e7 = []
    added_e9 = []
    new_e7_md_rows = []
    new_e9_md_rows = []

    for sigla, folder_name in sorted(UNIT_FOLDERS.items()):
        cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
        rows, t1, t2 = load_rows(cons_path)

        # 1. Check E7.O3.KR2
        if sigla in E7_O3_KR2_MISSING:
            has_e7 = any("[E7.O3.KR2]" in str(r[2] or "") for r in rows)
            if not has_e7:
                acao, como, quem = E7_O3_KR2_MISSING[sigla]
                new_row = [
                    "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica",
                    "O3: Fomentar uma cultura de inovação institucional",
                    "[E7.O3.KR2] KR2: Capacitar 25% do corpo funcional em Direito Digital e Inteligência Artificial até 2027",
                    acao,
                    como,
                    quem,
                    "Anual até 2027"
                ]
                rows.append(new_row)
                added_e7.append(sigla)
                new_e7_md_rows.append(
                    f"| **{folder_name}** | {acao} | {como} | {quem} | Anual até 2027 |"
                )

        # 2. Check E9.O2.KR1
        if sigla in E9_O2_KR1_THEMES:
            has_e9 = any("[E9.O2.KR1]" in str(r[2] or "") for r in rows)
            if not has_e9:
                temas, nome_setor = E9_O2_KR1_THEMES[sigla]
                acao = "Levantar necessidades anuais de capacitação da unidade e indicar trilhas técnicas ao Plano Anual de Capacitação (PAC)"
                como = (
                    f"Mapear anualmente as demandas prioritárias de qualificação técnica da equipe (com foco em {temas}), "
                    f"encaminhar sugestões de cursos e oficinas práticas à ESAP e ao SGRH para composição do Plano Anual de Capacitação (PAC) "
                    f"e viabilizar a participação ativa de ao menos 40% dos integrantes do setor."
                )
                quem = f"Líder: {nome_setor}; Coexecutores: Escola Superior da Advocacia Pública (ESAP), Serviço de Gestão de Recursos Humanos (SGRH)"
                prazo = "Ciclo Anual até 2029"
                new_row = [
                    "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
                    "O2: Ampliar a capacitação contínua",
                    "[E9.O2.KR1] KR1: Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029",
                    acao,
                    como,
                    quem,
                    prazo
                ]
                rows.append(new_row)
                added_e9.append(sigla)
                new_e9_md_rows.append(
                    f"| **{folder_name}** | {acao} | {como} | {quem} | {prazo} |"
                )

        write_sheet_to_all_targets(sigla, t1, t2, rows)

    print(f"Planilhas atualizadas com E7.O3.KR2 ({len(added_e7)}): {added_e7}")
    print(f"Planilhas atualizadas com E9.O2.KR1 ({len(added_e9)}): {added_e9}")
    return new_e7_md_rows, new_e9_md_rows

def update_cotejamento_md(new_e7_md_rows, new_e9_md_rows):
    cot_path = os.path.join(BASE_DIR, "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md")
    with open(cot_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Insert new E7.O3.KR2 rows right after Supervisão de Informática row in E7.O3.KR2
    anchor_e7 = "| **Supervisão de Informática** | Dar suporte técnico à ESAP e EGMA na oferta de trilhas continuadas de capacitação digital |"
    if anchor_e7 in text and new_e7_md_rows:
        lines = text.splitlines()
        out_lines = []
        for line in lines:
            out_lines.append(line)
            if line.startswith(anchor_e7):
                for r in new_e7_md_rows:
                    if r not in text:
                        out_lines.append(r)
        text = "\n".join(out_lines) + "\n"
        # Update count header in E7.O3.KR2
        text = re.sub(
            r"(- \*\*Unidades com Ações Mapeadas \()\d+(\):\*\* ESAP.*)",
            r"\g<1>23\g<2>",
            text
        )
        text = text.replace(
            "- **Volume de Ações Setoriais:** 25 iniciativas",
            "- **Volume de Ações Setoriais:** 33 iniciativas"
        )

    # 2. Insert new E9.O2.KR1 rows right after the last SGRH row in E9.O2.KR1
    anchor_e9 = "| **Serviço de Gestão de Recursos Humanos** | Integrar a capacitação contínua à política de valorização profissional do eixo 9 |"
    if anchor_e9 in text and new_e9_md_rows:
        lines = text.splitlines()
        out_lines = []
        for line in lines:
            out_lines.append(line)
            if line.startswith(anchor_e9):
                for r in new_e9_md_rows:
                    if r not in text:
                        out_lines.append(r)
        text = "\n".join(out_lines) + "\n"
        text = text.replace(
            "- **Unidades com Ações Mapeadas (2):** Escola Superior da Advocacia Pública (ESAP), Serviço de Gestão de Recursos Humanos",
            "- **Unidades com Ações Mapeadas (41):** Todas as 41 Unidades Setoriais da PGE-MA (ESAP e SGRH na coordenação pedagógica e gestão do PAC; 39 unidades jurídicas, consultivas e administrativas no levantamento anual de demandas formativas e liberação/engajamento de ao menos 40% das respectivas equipes)"
        )
        text = text.replace(
            "- **Volume de Ações Setoriais:** 21 iniciativas",
            "- **Volume de Ações Setoriais:** 60 iniciativas"
        )

    with open(cot_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md atualizado com sucesso.")

if __name__ == "__main__":
    e7_rows, e9_rows = update_all_sheets()
    update_cotejamento_md(e7_rows, e9_rows)

