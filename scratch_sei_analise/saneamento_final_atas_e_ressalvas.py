# -*- coding: utf-8 -*-
"""
Script de Saneamento Final Pós-Auditoria das Atas de Reunião e Ressalvas do Usuário:
1. PGARI (Chefiada pelo Dr. Daniel Blume - Papel estritamente articulador, não executivo):
   - Restaura as 6 ações de E3.O1.KR1 (Captação de R$ 2M) com redação de articulação institucional;
   - Mantém E5.O4.KR1 (2 ações) e E5.O4.KR2 (3 ações) com foco em articulação institucional preventiva (deixando a análise técnico-jurídica formal para ASJUR);
   - Mantém E9.O2.KR1 (PAC).
2. PSAU (Reunião realizada com corpo de assessores; E4.O1.KR1 mantida por decisão do Dr. Marcus Bacellar, Adjunto para Assuntos Estratégicos):
   - Mantém E4.O1.KR1 (90% consultas SES/CEMARC no prazo);
   - Expurga apenas E9.O3.KR1 (Honorários sucumbenciais), inaplicável a tutelas de urgência de saúde.
3. SGA e NCIA (Dr. Francisco Beolândio):
   - SGA: Sem relatório de transição. Expurga E5.O2.KR2, E6.O1.KR2 autônomo e E9.O3.KR1; embute a coordenação de sustentações orais gravadas no YouTube (ASCOM), o revezamento virtual de sustentações com Brasília e a interlocução metodológica sobre admissibilidade recursal dentro de E5.O1.KR2.
   - NCIA: Expurga acréscimos genéricos de simetria (E6.O1.KR2, E5.O5.KR2, E9.O3.KR1), mantendo o plano enxuto de 4 ações de E5.O6.KR1 + capacitação (E7.O3.KR2 e E9.O2.KR1).
4. PB (Procuradoria de Brasília - Dr. Ricardo Séllos):
   - Mantém a diretriz do Dr. Marcus Bacellar (vedação de devolução de agravos à origem para evitar retrabalho), mas registra na subação de E5.O2.KR2 que a proposta de fluxo didático de retorno de agravos poderá ser avaliada e discutida futuramente como ideia interna no plano de ação/oficinas com a ESAP;
   - Expurga E9.O3.KR1 de PB.
5. Corregedoria-Geral (Dr. Gustavo Saboia) e PGAAJ:
   - Substitui qualquer menção a "Rogério Murad" ou "Rodrigo Maia" por "Dr. Gustavo Saboia" nos documentos .md;
   - Em PGAAJ (E5.O6.KR1), expurga o "fluxo de alerta escalonado para intimações em risco crítico" e a métrica de "perdas evitadas", alinhando à diretriz do Corregedor-Geral Dr. Gustavo Saboia (gestão descentralizada pelas chefias no painel nativo do SPA e auditoria mensal de causas-raiz de prazos peremptórios efetivamente perdidos).
6. Remoção integral do termo "Oscar do Basquete" (e variações):
   - Nas planilhas de PJ e em todos os arquivos .md do workspace, mantendo apenas a descrição técnica (oficinas práticas de oratória forense e simulação de tribuna em parceria com a ESAP).
7. Integração do Fórum José Sarney (PJEFP) e Correlações entre Unidades:
   - Em PJEFP (linha 15): explicita que o acesso e melhorias na Extranet são de responsabilidade da Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI), e o canal direto de avisos via WhatsApp é atribuição do SGRH (em parceria com ASCOM);
   - Espelha em PGAAE (E5.O5.KR1): viabilizar acesso pleno à Extranet para unidades descentralizadas (Fórum José Sarney - PJEFP) e harmonizar numeração Extranet x SEI no ciclo 2027 (demanda PJ);
   - Espelha em SGRH (E9.O1.KR1): instituir canal direto de avisos funcionais e informes da sede/ESAP via WhatsApp para servidores descentralizados (Fórum José Sarney - PJEFP);
   - Espelha em ESAP (E9.O2.KR1): oficinas práticas de oratória forense e simulação de tribuna (demanda PJ/PB), capacitação em Escuta Ativa e Comunicação Não Violenta - CNV (demanda OUV) e Media Training para porta-vozes (demanda ASCOM);
   - Espelha em PGAAJ (E5.O1.KR2): coordenar sistema de revezamento virtual de sustentações orais nos Tribunais Superiores com procuradores de base e Procuradoria de Brasília;
   - Espelha em SCC e SMP: alimentar e integrar o Painel Compartilhado de Visibilidade Intersetorial (CSL, Contratos, Patrimônio e TI).
8. Saneamento dos códigos de fallback ([E5.O1.KR1] e [E6.O1.KR1]) nas planilhas de PGA, PGAAE, SGRH, ESAP, SMP, PDA, NIRF, PA, PCF, PERJP, PRI, PRT, PT e remoção da linha duplicada de certificação de TI em PEDU e PSP.
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

def apply_fixes_to_unit(sigla, rows):
    new_rows = []

    # 1. PGARI: Dr. Daniel Blume - Papel Articulador (não executivo)
    if sigla == "PGARI":
        pgari_e3_rows = [
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Articular a instituição de Programa Permanente de Captação de Recursos Externos",
                "Atuar de forma consultiva e articuladora na proposição de fluxo institucional de cooperação com o Escritório de Representação em Brasília, PGAAE e Gabinete para prospecção de recursos externos, sem ônus de execução orçamentária direta.",
                "Articulador: PGARI; Coexecutores: PGAAE, Procuradoria de Brasília, Gabinete",
                "120 dias"
            ),
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Articular o mapeamento e a revisão de convênios e parcerias institucionais ativas",
                "Promover a interlocução interinstitucional para acompanhamento estratégico de convênios e termos de cooperação vigentes junto às secretarias parceiras e à PGAAE.",
                "Articulador: PGARI; Coexecutores: PGAAE, PGA, Serviço de Controle de Contratos",
                "Semestral"
            ),
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Prospectar parcerias estratégicas junto a organismos multilaterais e instituições de fomento",
                "Realizar interlocução institucional proativa com organismos nacionais e internacionais (como o BID e agências de fomento) para identificar oportunidades de financiamento a projetos estratégicos da PGE-MA.",
                "Articulador: PGARI; Coexecutores: PGAAE, ESAP, Gabinete",
                "Contínuo"
            ),
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Articular diretrizes institucionais para captação de emendas parlamentares",
                "Atuar na ponte de relacionamento institucional com o Parlamento e o Gabinete para apresentação da carteira de projetos estratégicos da PGE-MA aptos à recepção de emendas.",
                "Articulador: PGARI; Coexecutores: Gabinete, PGAAE, PGA",
                "180 dias"
            ),
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Apoiar a estruturação de Painel/Dashboard BI de acompanhamento de parcerias e captações",
                "Fornecer subsídios de relacionamento institucional à Assessoria em TIC da PGAAE / INOVA para visualização das frentes de cooperação e recursos prospectados.",
                "Articulador: PGARI; Coexecutores: Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI)",
                "Até 2027"
            ),
            (
                "Eixo Estratégico 3 – Incrementar e executar integralmente o orçamento institucional",
                "O1: Ampliar fontes de receita e otimizar a execução orçamentária",
                "[E3.O1.KR1] KR1: Captar R$ 2 milhões em recursos externos (emendas, parcerias, editais) para projetos estratégicos até 2029",
                "Articular o alinhamento entre fontes externas prospectadas e o planejamento estratégico",
                "Participar de forma consultiva e articuladora do alinhamento entre as oportunidades de captação externa e as prioridades estratégicas definidas pela PGAAE e PGA.",
                "Articulador: PGARI; Coexecutores: PGAAE, PGA",
                "Anual"
            ),
        ]
        new_rows.extend(pgari_e3_rows)
        for r in rows:
            kr = r[2] or ""
            acao = r[3] or ""
            sub = r[4] or ""
            resp = r[5] or ""
            if "[E5.O4.KR1]" in kr:
                if "Comitê de Riscos" in acao:
                    sub = "Atuar em caráter estritamente articulador na interlocução prévia com a Casa Civil, CPARI e Gabinete para sinalização antecipada de proposições estratégicas, cabendo a análise técnico-jurídica formal de constitucionalidade e legalidade exclusivamente à Assessoria Jurídica (ASJUR)."
                    resp = "Articulador: PGARI; Execução Técnico-Jurídica: Assessoria Jurídica (ASJUR); Coexecutores: CPARI, Gabinete"
                else:
                    sub = "Promover o relacionamento institucional preventivo e o diálogo intersetorial sobre temas normativos de alto impacto governamental junto ao CPARI e Gabinete, resguardada a competência consultiva exclusiva da ASJUR."
                    resp = "Articulador: PGARI; Execução Técnico-Jurídica: Assessoria Jurídica (ASJUR); Coexecutores: CPARI, Gabinete"
            elif "[E5.O4.KR2]" in kr:
                resp = resp.replace("Líder: PGARI", "Articulador: PGARI")
            new_rows.append((r[0], r[1], kr, acao, sub, resp, r[6]))
        return new_rows

    # 2. PSAU: Manter E4.O1.KR1 (mantida pelo Dr. Marcus Bacellar), expurgar apenas E9.O3.KR1
    if sigla == "PSAU":
        for r in rows:
            kr = r[2] or ""
            if "[E9.O3.KR1]" in kr:
                continue
            new_rows.append(r)
        return new_rows

    # 3. NCIA: Manter enxuto (4 ações E5.O6.KR1 + capacitação E7.O3.KR2 e E9.O2.KR1)
    if sigla == "NCIA":
        for r in rows:
            kr = r[2] or ""
            if any(k in kr for k in ["[E6.O1.KR2]", "[E5.O5.KR2]", "[E9.O3.KR1]"]):
                continue
            new_rows.append(r)
        return new_rows

    # 4. SGA: Sem relatório de transição; expurgar E5.O2.KR2, E6.O1.KR2 autônomo e E9.O3.KR1; embutir em E5.O1.KR2
    if sigla == "SGA":
        for r in rows:
            kr = r[2] or ""
            acao = r[3] or ""
            sub = r[4] or ""
            resp = r[5] or ""
            if any(k in kr for k in ["[E6.O1.KR2]", "[E5.O2.KR2]", "[E9.O3.KR1]"]):
                continue
            if "[E5.O1.KR2]" in kr and "pautas de 2º Grau" in acao:
                acao = "Articular atuação coordenada em pautas de 2º Grau, revezamento virtual de sustentações com Brasília e difusão no YouTube junto à ASCOM"
                sub = "Coordenar o fluxo de pautas perante o TJMA e TRF1, apoiar o sistema de revezamento virtual de sustentações orais nos Tribunais Superiores com a Procuradoria de Brasília (bem como a interlocução metodológica sobre óbices recursais) e remeter à ASCOM os links e minutagens de sustentações orais gravadas no YouTube dos Tribunais para divulgação institucional."
                resp = "Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: Procuradorias Especializadas, Procuradoria de Brasília (PB), PGAAJ, Assessoria de Comunicação (ASCOM)"
            new_rows.append((r[0], r[1], kr, acao, sub, resp, r[6]))
        return new_rows

    # 5. PB: Ajustar subação de E5.O2.KR2 sobre fluxo de agravos e remover E9.O3.KR1
    if sigla == "PB":
        for r in rows:
            kr = r[2] or ""
            acao = r[3] or ""
            sub = r[4] or ""
            if "[E9.O3.KR1]" in kr:
                continue
            if "[E5.O2.KR2]" in kr and "Relatório Semestral de Superação de Óbices" in acao:
                sub = "Elaborar e remeter semestralmente à PGAAJ, SGA e Especializadas relatório técnico mapeando os principais óbices de inadmissão no STJ e STF (Súmulas 7/STJ e 279/STF, ausência de prequestionamento e comprovação de feriado local), sem devolução operacional de processos à origem (evitando retrabalho), mas mantendo a proposta de fluxo didático de análise de agravos como iniciativa pedagógica a ser discutida e amadurecida em conjunto com a ESAP e a PGAAJ."
            new_rows.append((r[0], r[1], kr, acao, sub, r[5], r[6]))
        return new_rows

    # Loop geral para as demais unidades (incluindo correções específicas e mapeamento de códigos fallback)
    for r in rows:
        eixo, obj, kr, acao, sub, resp, prazo = r[0], r[1], r[2] or "", r[3] or "", r[4] or "", r[5] or "", r[6] or ""

        # Remover "Oscar do Basquete" em qualquer unidade (especialmente PJ)
        if "oscar do basquete" in acao.lower() or "oscar do basquete" in sub.lower():
            acao = re.sub(r"\s*\(['\"]?Oscar do Basquete.*?['\"]?\)", "", acao, flags=re.IGNORECASE)
            sub = re.sub(r"\s*\(['\"]?Oscar do Basquete.*?['\"]?\)", "", sub, flags=re.IGNORECASE)
            sub = sub.replace("treinamentos práticos de oratória jurídica para superar", "treinamentos práticos e contínuos de oratória jurídica e técnica de tribuna para superar")

        # Remover linha residual duplicada de certificação tecnológica em PEDU e PSP
        if sigla in ("PEDU", "PSP") and "[E7.O3.KR1]" in kr and "certifica" in acao.lower():
            continue

        # PGAAJ: Sanear linhas 25 e 26 (E5.O6.KR1) conforme diretriz do Corregedor-Geral Dr. Gustavo Saboia
        if sigla == "PGAAJ" and "[E5.O6.KR1]" in kr:
            if "alerta escalonado" in acao.lower():
                acao = "Apoiar a gestão descentralizada de prazos pelas chefias imediatas no painel nativo do SPA"
                sub = "Fortalecer o acompanhamento preventivo de prazos processuais diretamente pelas chefias imediatas das Especializadas por meio das ferramentas nativas do SPA, sem adoção de regimes intrusivos de alertas paralelos."
                resp = "Líder: PGAAJ; Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Chefias das Especializadas"
            elif "perdas evitadas" in acao.lower():
                acao = "Acompanhar relatório mensal de causas-raiz de prazos peremptórios efetivamente perdidos e falhas sistêmicas"
                sub = "Analisar mensalmente, em articulação com a Corregedoria-Geral e a SGA, os relatórios consolidados de prazos peremptórios/preclusivos efetivamente perdidos e eventuais falhas técnicas de captura no SPA, promovendo o saneamento preventivo das causas-raiz."
                resp = "Líder: PGAAJ; Coexecutores: Corregedoria-Geral (CG), Subprocuradoria-Geral Adjunta (SGA), Assessoria em TIC da PGAAE / INOVA"

        # PJEFP: Ajustar linha 15 (Integração Digital do Fórum José Sarney: Extranet = Assessoria em TIC da PGAAE; Avisos = SGRH)
        if sigla == "PJEFP" and "Fórum José Sarney" in acao:
            sub = "Articular junto à Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI) a habilitação plena da Extranet nas estações de trabalho do Fórum Des. José Sarney, e junto ao Serviço de Gestão de Recursos Humanos (SGRH) a inclusão dos servidores descentralizados em canal direto de avisos funcionais e informes da sede/ESAP via WhatsApp."
            resp = "Líder: PJEFP; Coexecutores: Assessoria em TIC da PGAAE / INOVA (Extranet), Serviço de Gestão de Recursos Humanos - SGRH (Canal de Avisos), ASCOM e SI (Infraestrutura)"

        # Saneamento dos códigos de fallback [E5.O1.KR1] e [E6.O1.KR1]
        al = acao.lower()
        if "[E5.O1.KR1]" in kr:
            if any(w in al for w in ["calendário editorial", "conteúdo editorial", "produção audiovisual", "eventos institucionais", "ativos reputacionais", "porta-vozes"]):
                eixo = "Eixo Estratégico 6 – Fortalecer a imagem institucional e a comunicação com a sociedade"
                obj = "O1: Fortalecer a imagem e o reconhecimento da PGE como referência de excelência"
                kr = "[E6.O1.KR1] KR1: Aumentar em 20% a taxa de engajamento da PGE nas mídias institucionais até 2029"
            elif any(w in al for w in ["benchmarking", "fonace"]):
                eixo = "Eixo Estratégico 6 – Fortalecer a imagem institucional e a comunicação com a sociedade"
                obj = "O2: Ampliar o impacto institucional e a cooperação interinstitucional"
                kr = "[E6.O2.KR1] KR1: Desenvolver 10 projetos interinstitucionais com universidades, órgãos públicos e Procuradorias até 2030"
            elif any(w in al for w in ["implantação de ia", "casos de uso prioritários de ia", "plataforma local de ia", "uso responsável da ia", "ferramentas novas às soluções", "usuários das novas ferramentas", "pesquisa jurídica"]):
                eixo = "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica"
                obj = "O1: Adotar ferramentas de Inteligência Artificial e automação"
                kr = "[E7.O1.KR1] KR1: Automatizar 30% da elaboração de pareceres padronizados com inteligência artificial até 2028"
            elif any(w in al for w in ["inventário tecnológico", "renovação do parque", "renovação tecnológica", "substituição tecnológica", "modernização tecnológica", "modernização do parque"]):
                eixo = "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica"
                obj = "O2: Modernizar a infraestrutura tecnológica e segurança de dados"
                kr = "[E7.O2.KR1] KR1: Substituir 100% dos equipamentos de TI obsoletos até 2027"
            elif any(w in al for w in ["satisfação", "experiência do contribuinte", "padrão de atendimento tributário"]):
                eixo = "Eixo Estratégico 4 – Aprimorar o relacionamento institucional e a entrega de valor"
                obj = "O1: Melhorar a experiência do usuário dos serviços da PGE"
                kr = "[E4.O1.KR2] KR2: Alcançar índice de satisfação do usuário externo igual ou superior a 90% até 2030"
            elif any(w in al for w in ["higienização de dados", "saneamento cadastral", "inteligência recuperatória", "inteligência fiscal"]):
                eixo = "Eixo Estratégico 1 – Incrementar a recuperação de créditos e a defesa do erário"
                obj = "O4: Aprimorar a inteligência fiscal e a recuperação de ativos"
                kr = "[E1.O4.KR2] KR2: Aumentar em 20% ao ano a recuperação de créditos decorrentes de saneamento cadastral até 2030"
            elif any(w in al for w in ["grandes devedores"]):
                eixo = "Eixo Estratégico 1 – Incrementar a recuperação de créditos e a defesa do erário"
                obj = "O5: Fortalecer a cobrança administrativa e a execução fiscal estratégica"
                kr = "[E1.O5.KR2] KR2: Aumentar em 70% o montante de bens bloqueados ou arrolados de grandes devedores até 2027"
            elif any(w in al for w in ["conceito de “êxito”", "conceito de 'êxito'", "higidez das cdas e procedência", "expurgo de excesso de execução"]):
                kr = "[E5.O1.KR3] KR3: Atingir taxa de êxito de 80% nos processos judiciais estratégicos até 2027"
            elif any(w in al for w in ["presença institucional em julgamentos", "qualificação técnica das contestações", "assistência pericial contábil"]):
                kr = "[E5.O1.KR2] KR2: Garantir atuação processual estratégica qualificada em 100% dos processos prioritários monitorados até 2030"

        elif "[E6.O1.KR1]" in kr and sigla in ("PGA", "SGRH", "ESAP"):
            if any(w in al for w in ["saúde mental", "ergonomia"]):
                eixo = "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores"
                obj = "O1: Promover a valorização, o bem-estar e a retenção de talentos"
                kr = "[E9.O1.KR3] KR3: Reduzir em 30% os afastamentos de saúde decorrentes de fatores ergonômicos ou estresse ocupacional até 2029"
            elif any(w in al for w in ["equidade e inclusão"]):
                eixo = "Eixo Estratégico 8 – Fomentar a sustentabilidade, a integridade e a responsabilidade social"
                obj = "O1: Promover a sustentabilidade ambiental, a equidade e a inclusão"
                kr = "[E8.O1.KR2] KR2: Atingir 30% de participação de grupos sub-representados em cargos de liderança até 2028"
            elif any(w in al for w in ["valorização", "clima organizacional", "escuta institucional"]):
                eixo = "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores"
                obj = "O1: Promover a valorização, o bem-estar e a retenção de talentos"
                kr = "[E9.O1.KR1] KR1: Alcançar e manter índice de satisfação do clima organizacional igual ou superior a 80% até 2030"

        new_rows.append((eixo, obj, kr, acao, sub, resp, prazo))

    # Adição de ações espelho (correlações intersetoriais das reuniões)
    existing_actions = " ".join([r[3].lower() for r in new_rows])

    if sigla == "PJ" and "harmonizar a numeração" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O5: Otimizar os fluxos de trabalho e aumentar a produtividade",
            "[E5.O5.KR1] KR1: Reduzir em 20% o tempo dedicado a tarefas manuais e repetitivas até 2028",
            "Harmonizar a numeração de expedientes e pareceres entre Extranet e SEI a partir do ciclo 2027",
            "Articular junto à Assessoria em TIC da PGAAE / INOVA o alinhamento técnico para zerar e sincronizar a numeração de ofícios, despachos e pareceres entre a Extranet PGE e o sistema SEI na virada do exercício de 2027, eliminando controles paralelos.",
            "Líder: Procuradoria Judicial (PJ); Coexecutores: Assessoria em TIC da PGAAE / INOVA",
            "Ciclo 2027"
        ))

    if sigla == "PGAAE" and "fórum josé sarney" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O5: Otimizar os fluxos de trabalho e aumentar a produtividade",
            "[E5.O5.KR1] KR1: Reduzir em 20% o tempo dedicado a tarefas manuais e repetitivas até 2028",
            "Garantir o acesso pleno à Extranet para unidades descentralizadas (Fórum José Sarney) e harmonizar numeração Extranet x SEI",
            "Prover, por meio da Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI), a habilitação e o aprimoramento da Extranet para os servidores da PJEFP no Fórum Des. José Sarney, bem como a sincronização anual de numeração de atos entre Extranet e SEI solicitada pela Procuradoria Judicial.",
            "Líder: Assessoria em TIC da PGAAE / INOVA; Coexecutores: PJEFP, Procuradoria Judicial (PJ), ASCOM, Supervisão de Informática (Suporte de Infraestrutura)",
            "90 dias / Ciclo 2027"
        ))

    if sigla == "SGRH" and "fórum josé sarney" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
            "O1: Promover a valorização, o bem-estar e a retenção de talentos",
            "[E9.O1.KR1] KR1: Alcançar e manter índice de satisfação do clima organizacional igual ou superior a 80% até 2030",
            "Instituir canal direto de avisos funcionais para servidores lotados em unidades descentralizadas (Fórum José Sarney e Regionais)",
            "Criar e manter grupo/lista de transmissão oficial no WhatsApp gerido pelo SGRH para envio tempestivo de comunicados de recursos humanos, feriados, ponto eletrônico e cursos da ESAP aos servidores lotados fora da sede (como a PJEFP no Fórum Des. José Sarney).",
            "Líder: Serviço de Gestão de Recursos Humanos (SGRH); Coexecutores: PJEFP, Procuradorias Regionais (PRI/PRT), ASCOM, ESAP",
            "60 dias / Contínuo"
        ))

    if sigla == "PGAAJ" and "revezamento virtual" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O1: Aprimorar a gestão de processos estratégicos",
            "[E5.O1.KR2] KR2: Garantir atuação processual estratégica qualificada em 100% dos processos prioritários monitorados até 2030",
            "Coordenar o sistema de revezamento virtual de sustentações orais nos Tribunais Superiores com os procuradores de base",
            "Articular entre a Procuradoria de Brasília (PB), a SGA e as Procuradorias Especializadas escala de revezamento virtual permitindo que o procurador de origem que instruiu a causa no 1º/2º grau realize a sustentação oral por videoconferência no STJ/STF, concentrando a atuação presencial de Brasília nos despachos estratégicos com Ministros.",
            "Líder: PGAAJ; Coexecutores: Procuradoria de Brasília (PB), Subprocuradoria-Geral Adjunta (SGA), Procuradorias Especializadas",
            "Contínuo"
        ))

    if sigla == "ESAP" and "oratória forense" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
            "O2: Ampliar a capacitação contínua",
            "[E9.O2.KR1] KR1: Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029",
            "Promover oficinas práticas de Oratória Forense, Escuta Ativa/CNV e Media Training para membros e servidores",
            "Realizar semestralmente oficinas práticas de sustentação oral e simulação de tribuna (em parceria com a PJ e PB), cursos de acolhimento humanizado, Escuta Ativa e Comunicação Não Violenta - CNV (em parceria com a Ouvidoria e Comitê de Equidade) e oficinas de Media Training para porta-vozes institucionais (em parceria com a ASCOM).",
            "Líder: Escola Superior da Advocacia Pública (ESAP); Coexecutores: Procuradoria Judicial (PJ), Procuradoria de Brasília (PB), Ouvidoria (OUV), Assessoria de Comunicação (ASCOM), Comitê de Equidade",
            "Semestral"
        ))

    if sigla == "SCC" and "painel compartilhado" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 2 – Otimizar a gestão administrativa, logística e de contratações",
            "O2: Aperfeiçoar os processos de compras, licitações e gestão contratual",
            "[E2.O2.KR1] KR1: Reduzir em 30% o tempo médio dos processos licitatórios até 2028",
            "Integrar e alimentar o Painel Compartilhado de Visibilidade Intersetorial (CSL, Contratos, Patrimônio e TI)",
            "Alimentar continuamente o dashboard compartilhado com a Comissão Setorial de Licitação (CSL), o Serviço de Material e Patrimônio (SMP) e a área de TIC, disponibilizando o status atualizado de vigências, saldos contratuais e renovações para eliminar diligências físicas entre setores.",
            "Líder: Serviço de Controle de Contratos (SCC); Coexecutores: Comissão Setorial de Licitação (CSL), Serviço de Material e Patrimônio (SMP), Assessoria em TIC da PGAAE / INOVA",
            "90 dias / Contínuo"
        ))

    if sigla == "SMP" and "painel compartilhado" not in existing_actions:
        new_rows.append((
            "Eixo Estratégico 2 – Otimizar a gestão administrativa, logística e de contratações",
            "O2: Aperfeiçoar os processos de compras, licitações e gestão contratual",
            "[E2.O2.KR1] KR1: Reduzir em 30% o tempo médio dos processos licitatórios até 2028",
            "Integrar e alimentar o Painel Compartilhado de Visibilidade Intersetorial (CSL, Contratos, Patrimônio e TI)",
            "Compartilhar em painel integrado com a CSL, o Serviço de Controle de Contratos (SCC) e a TIC os dados atualizados de inventário patrimonial, demandas de materiais e baixa de equipamentos obsoletos, agilizando a instrução da fase preparatória das contratações.",
            "Líder: Serviço de Material e Patrimônio (SMP); Coexecutores: Comissão Setorial de Licitação (CSL), Serviço de Controle de Contratos (SCC), Assessoria em TIC da PGAAE / INOVA",
            "90 dias / Contínuo"
        ))

    return new_rows

def main():
    updated = 0
    for sigla in sorted(UNIT_FOLDERS.keys()):
        cons_path = os.path.join(CONS_DIR, f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
        if not os.path.exists(cons_path):
            continue
        rows, t1, t2 = load_rows(cons_path)
        if sigla == "PGARI":
            t2 = "Classificação formal de Eixos, Objetivos e KRs da PGE-MA (Papel Articulador em Captação Externa e Riscos Governamentais/Socioambientais)"
        new_rows = apply_fixes_to_unit(sigla, rows)
        if new_rows != rows or sigla == "PGARI":
            write_sheet_to_all_targets(sigla, t1, t2, new_rows)
            updated += 1
            print(f"[{sigla}] atualizado: {len(rows)} -> {len(new_rows)} ações")
    print(f"\nTotal de unidades atualizadas: {updated}")

if __name__ == "__main__":
    main()
