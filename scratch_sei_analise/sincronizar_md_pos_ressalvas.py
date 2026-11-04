# -*- coding: utf-8 -*-
"""
Script de Sincronização Completa dos Documentos Markdown (.md) e Word (.docx)
após as Ressalvas Finais do Usuário:
1. PGARI: Chefiada pelo Dr. Daniel Blume (papel estritamente articulador, não executivo; restauradas 6 ações de E3.O1.KR1 + E5.O4.KR1 e E5.O4.KR2 articuladoras).
2. PSAU: Reunião com corpo de assessores; E4.O1.KR1 mantida por decisão do Dr. Marcus Bacellar (Adjunto para Assuntos Estratégicos); E9.O3.KR1 expurgada.
3. SGA e NCIA: Sem relatório de transição na SGA; expurgadas E6.O1.KR2, E5.O5.KR2 e E9.O3.KR1 do NCIA e E5.O2.KR2, E6.O1.KR2 autônoma e E9.O3.KR1 da SGA.
4. PB: Diretriz do Dr. Marcus Bacellar mantendo vedação de devolução operacional de agravos (para evitar retrabalho), mas registrando que a sugestão de fluxo didático de retorno de agravos pode ser discutida como ideia pedagógica no plano de ação com ESAP/PGAAJ; expurgada E9.O3.KR1 de PB.
5. Corregedoria-Geral: Nome correto do Corregedor-Geral é Dr. Gustavo Saboia (substituindo "Rogério Murad" e "Rodrigo Maia" em todos os .md); expurgado o fluxo de alerta escalonado e a métrica de perdas evitadas também na PGAAJ.
6. Ocultação total do termo "Oscar do Basquete" em todos os arquivos .md.
7. Fórum José Sarney (PJEFP): Extranet sob responsabilidade da Assessoria em TIC da PGAAE / INOVA; Canal de avisos sob responsabilidade do SGRH.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"

def clean_oscar_and_names(text):
    # 1. Substituir Rogério Murad e Rodrigo Maia por Gustavo Saboia
    text = text.replace("Dr. Rogério Murad", "Dr. Gustavo Saboia")
    text = text.replace("ROGÉRIO MURAD", "GUSTAVO SABOIA")
    text = text.replace("Rogério Murad", "Gustavo Saboia")
    text = text.replace("Dr. Rodrigo Maia / Dra. Fabiana Silva Pinho Carvalhal", "Dr. Gustavo Saboia (Corregedor-Geral)")
    text = text.replace("Dr. Rodrigo Maia", "Dr. Gustavo Saboia")

    # 2. Substituir Dr. Rennan Fonseca Reis na PGARI por Dr. Daniel Blume
    text = text.replace("Dr. Rennan Fonseca Reis (PGARI)", "Dr. Daniel Blume (Procurador-Geral Adjunto de Relacionamento Institucional - PGARI)")
    text = text.replace("Olá, Dr. Rennan!", "Olá, Dr. Daniel!")

    # 3. Ocultar todas as menções a "Oscar do Basquete" e variações
    text = text.replace(' e a Analogia do "Oscar do Basquete"', "")
    text = text.replace(" e a Analogia 'Oscar do Basquete'", "")
    text = text.replace(' ("Oscar do Basquete")', "")
    text = text.replace(" ('Oscar do Basquete')", "")
    text = text.replace(" ('Oscar do Basquete: tudo é repetição')", "")
    text = text.replace(' (referenciado como projeto \'Oscar do Basquete\' para perda de receio de falar em público e atuação nas Câmaras do TJMA)', ' (focado no desenvolvimento da fluência na tribuna e atuação nas Câmaras do TJMA)')
    text = text.replace(' ("Projeto Oscar do Basquete")', "")
    text = re.sub(r"\s*\(['\"]?[Pp]rojeto\s+Oscar\s+do\s+Basquete['\"]?\)", "", text)
    text = re.sub(r"\s*\(['\"]?Oscar\s+do\s+Basquete.*?['\"]?\)", "", text)
    text = re.sub(r"Metáfora do [\"']Oscar do Basquete[\"']:", "Diretriz de Prática Contínua de Oratória:", text)
    text = re.sub(r"Analogia Pedagógica\s*\([\"']Oscar do Basquete[\"']\):", "Diretriz Pedagógica de Treinamento Contínuo:", text)
    text = re.sub(r"utilizou a célebre frase do treinador/jogador Oscar Schmidt — \*\"Tudo é repetição\"\* — para exemplificar", "destacou a premissa de que *\"tudo é repetição\"* para exemplificar", text)
    text = re.sub(r"Adoção da máxima de Oscar Schmidt \(\"Tudo é repetição\"\), prevendo", "Adoção da diretriz de treinamento prático contínuo, prevendo", text)
    text = re.sub(r"Alusão ao atleta Oscar Schmidt para destacar que a excelência técnica e a oratória resultam", "Destaque ao princípio de que a excelência técnica e a oratória forense resultam", text)

    return text

def update_all_md_files():
    modified_files = []
    for root, _, files in os.walk(BASE_DIR):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                orig = f.read()
            updated = clean_oscar_and_names(orig)
            if updated != orig:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(updated)
                modified_files.append(os.path.relpath(fpath, BASE_DIR))
    print("Arquivos .md limpos (Gustavo Saboia, Daniel Blume, ocultação Oscar):", modified_files)

def update_specific_syntheses_and_kits():
    # 1. Atualizar Relatório Sintético da PGARI
    pgari_sint = os.path.join(BASE_DIR, "Procuradoria-Geral Adjunta de Relacionamento Institucional", "Documentos Ajustados Após Reunião", "Relatório Sintético - Ajustes Pós-Reunião.md")
    if os.path.exists(pgari_sint):
        with open(pgari_sint, "r", encoding="utf-8") as f:
            t = f.read()
        t = t.replace(
            "**Coordenação / Chefia:** Procurador-Geral Adjunto de Relacionamento Institucional",
            "**Coordenação / Chefia:** Dr. Daniel Blume (Procurador-Geral Adjunto de Relacionamento Institucional)"
        )
        t = t.replace(
            "* **Vocação Articuladora:** A tese central assentou-se na consolidação da PGARI como articuladora institucional proativa",
            "* **Vocação Estritamente Articuladora (Não Executiva):** Sob a chefia do Dr. Daniel Blume, a tese central assentou-se na consolidação da PGARI como unidade de articulação institucional proativa (e não de execução operacional direta)"
        )
        with open(pgari_sint, "w", encoding="utf-8") as f:
            f.write(t)

    # 2. Atualizar Relatório Sintético da PSAU
    psau_sint = os.path.join(BASE_DIR, "Procuradoria da Saúde", "Documentos Ajustados Após Reunião", "Relatório Sintético - Ajustes Pós-Reunião.md")
    if os.path.exists(psau_sint):
        with open(psau_sint, "r", encoding="utf-8") as f:
            t = f.read()
        t = t.replace(
            "**Interlocutores:** Dr. Carlos Santana (Procurador-Chefe) e equipe da Procuradoria da Saúde; Bruno Gomes (Assessor da Adjuntoria de Assuntos Estratégicos).",
            "**Interlocutores:** Corpo de Assessores da Procuradoria da Saúde (em razão da impossibilidade de presença da chefia na ocasião) e posterior deliberação com o Dr. Marcus Bacellar (Procurador-Geral Adjunto para Assuntos Estratégicos); Bruno Gomes."
        )
        t = t.replace(
            "### 2.1 Supressão Integral do Eixo 4 (Atendimento e Consultas)\n* A unidade esclareceu que o volume de consultas jurídicas formais recebidas é estatisticamente irrisório (praticamente zero no ano), visto que consultas administrativas, licitações e contratos da SES e EMSERH são absorvidos pela Consultoria Geral / Assessoria Jurídica da PGE.\n* Em razão da ausência de demanda direta, **o Eixo 4 foi integralmente suprimido do plano setorial**.",
            "### 2.1 Manutenção do Eixo 4 (`E4.O1.KR1` — Tempestividade em Consultas da SES)\n* Na reunião técnica, o corpo de assessores informou que a demanda de consultas formais da SES na unidade é reduzida, o que dificultaria a mensuração isolada.\n* Contudo, em reunião de deliberação com o Procurador-Geral Adjunto para Assuntos Estratégicos, **Dr. Marcus Bacellar**, decidiu-se **manter a meta `E4.O1.KR1`** (responder ao menos 90% das consultas e orientações jurídicas da SES e CEMARC dentro do prazo regulamentar), assegurando o alinhamento institucional com a atuação preventiva."
        )
        with open(psau_sint, "w", encoding="utf-8") as f:
            f.write(t)

    # 3. Atualizar Relatório Sintético de Brasília (PB)
    pb_sint = os.path.join(BASE_DIR, "Procuradoria de Brasília", "Documentos Ajustados Após Reunião", "Relatório Sintético - Ajustes Pós-Reunião.md")
    if os.path.exists(pb_sint):
        with open(pb_sint, "r", encoding="utf-8") as f:
            t = f.read()
        t = t.replace(
            "| **6** | Fluxo Didático de Agravos | Retorno de agravos aos redatores da base para assimilação de óbices sumulares e unificação de teses. | Brasília, Especializadas, ESAP | Semestral |",
            "| **6** | Relatório Semestral de Superação de Óbices (e avaliação de Fluxo Didático) | Mapeamento semestral dos óbices (Súmulas 7/STJ e 279/STF) sem devolução operacional de agravos à origem (evitando retrabalho, conforme diretriz da Adjuntoria Estratégica), mantendo-se a ideia de fluxo didático como proposta a ser discutida com ESAP e PGAAJ. | Brasília, PGAAJ, SGA, ESAP | Semestral |"
        )
        with open(pb_sint, "w", encoding="utf-8") as f:
            f.write(t)

    # 4. Atualizar Relatório Sintético da PJEFP
    pjefp_sint = os.path.join(BASE_DIR, "Procuradoria dos Juizados Especiais da Fazenda Pública", "Documentos Ajustados Após Reunião", "Relatório Sintético - Ajustes Pós-Reunião.md")
    if os.path.exists(pjefp_sint):
        with open(pjefp_sint, "r", encoding="utf-8") as f:
            t = f.read()
        t = t.replace(
            "| **10** | Integração Digital do Fórum Sarney | Acesso à Extranet nas máquinas do fórum e canal direto de avisos via WhatsApp do RH/Comunicação. | PJEFP, TI, SGRH, ASCOM | 90 dias / Contínuo |",
            "| **10** | Integração Digital do Fórum Sarney | Acesso pleno à Extranet nas máquinas do fórum (sob responsabilidade da Assessoria em TIC da PGAAE) e canal direto de avisos funcionais via WhatsApp (sob responsabilidade do SGRH). | PJEFP, Assessoria em TIC da PGAAE, SGRH, ASCOM, SI | 90 dias / Contínuo |"
        )
        with open(pjefp_sint, "w", encoding="utf-8") as f:
            f.write(t)

    # 5. Atualizar Kit_Despachos_SEI_e_Mensagens_WhatsApp.md
    kit_path = os.path.join(BASE_DIR, "Kit_Despachos_SEI_e_Mensagens_WhatsApp.md")
    if os.path.exists(kit_path):
        with open(kit_path, "r", encoding="utf-8") as f:
            t = f.read()
        # Ajustar bloco 2.3 (PB)
        t = t.replace(
            "já com a diretriz do Relatório Semestral de Superação de Óbices (Súmulas 7/STJ e 279/STF) sem devolução de processos à origem, o alinhamento da metodologia de admissibilidade recursal com a SGA e o fluxo quinzenal com a ASCOM.",
            "já com a diretriz do Relatório Semestral de Superação de Óbices (Súmulas 7/STJ e 279/STF) — sem devolução operacional de agravos à origem para evitar retrabalho, mas preservando a ideia do fluxo didático para discussão em oficina com a ESAP/PGAAJ —, o revezamento virtual de sustentações orais e o fluxo quinzenal com a ASCOM."
        )
        t = t.replace(
            "elaboração do Relatório Semestral de Superação de Óbices (Súmulas 7/STJ e 279/STF) sem devolução de processos às especializadas de origem, alinhamento da metodologia de mensuração de admissibilidade recursal junto à SGA, atuação seletiva de alto impacto e fluxo quinzenal de divulgação institucional junto à ASCOM.",
            "elaboração do Relatório Semestral de Superação de Óbices (Súmulas 7/STJ e 279/STF) sem devolução operacional de processos às especializadas de origem (evitando retrabalho, sem prejuízo da discussão pedagógica da ideia junto à ESAP/PGAAJ), sistema de revezamento virtual de sustentações orais, alinhamento com a SGA e fluxo quinzenal junto à ASCOM."
        )
        # Ajustar bloco 2.5 (PGARI - Dr. Daniel Blume)
        old_pgari_block = """### 2.5. Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI)
- **Interlocutor:** Dr. Daniel Blume (Procurador-Geral Adjunto de Relacionamento Institucional - PGARI)
- **Arquivo para Anexar no SEI:** [Plano_Acao_Pos_Comparacao_PGARI.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PGARI.xlsx)
- **Mensagem WhatsApp:**
  ```text
  Olá, Dr. Daniel! Tudo bem?
  A planilha final da PGARI (Plano_Acao_Pos_Comparacao_PGARI.xlsx) já foi atualizada e anexada ao SEI, com o expurgo integral das metas de execução orçamentária/captação (remanejadas para PGA/USF) e de análise prévia de PLs (remetida à Consultoria/ASJUR), mantendo o foco estrito na articulação institucional e nas iniciativas de mediação e risco socioambiental (`E5.O4.KR1` e `E5.O4.KR2`).
  Basta lançar no SEI o despacho padrão: "Com reunião presencial e documento anexado, valido os dados e o processo." Obrigado!
  ```
- **Despacho SEI (Assessoria de Planejamento -> PGARI):**
  ```text
  À Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI),
  Anexamos aos autos a matriz saneada do Plano de Ação da PGARI (Plano_Acao_Pos_Comparacao_PGARI.xlsx), após o expurgo das metas orçamentárias (reorientadas à PGA/USF) e de controle prévio legislativo (afetas à Consultoria), consolidando as iniciativas de articulação interinstitucional e gerenciamento de conflitos socioambientais.
  Solicita-se o despacho padrão de validação para encerramento da instrução setorial.
  ```"""
        new_pgari_block = """### 2.5. Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI)
- **Interlocutor:** Dr. Daniel Blume (Procurador-Geral Adjunto de Relacionamento Institucional)
- **Arquivo para Anexar no SEI:** [Plano_Acao_Pos_Comparacao_PGARI.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PGARI.xlsx)
- **Mensagem WhatsApp:**
  ```text
  Olá, Dr. Daniel! Tudo bem?
  A planilha final da PGARI (Plano_Acao_Pos_Comparacao_PGARI.xlsx) já foi atualizada e anexada ao SEI, delimitando a atuação da PGARI em caráter estritamente articulador (não executivo) nas frentes de prospecção/parcerias externas (`E3.O1.KR1`) e de prevenção de riscos normativos e socioambientais (`E5.O4.KR1` e `E5.O4.KR2`), expurgadas as metas de execução orçamentária direta e Profisco.
  Basta lançar no SEI o despacho padrão: "Com reunião presencial e documento anexado, valido os dados e o processo." Obrigado!
  ```
- **Despacho SEI (Assessoria de Planejamento -> PGARI):**
  ```text
  À Procuradoria-Geral Adjunta de Relacionamento Institucional (PGARI),
  Anexamos aos autos a matriz saneada do Plano de Ação da PGARI (Plano_Acao_Pos_Comparacao_PGARI.xlsx), estruturada segundo a vocação estritamente articuladora e consultiva da unidade (sem ônus de execução orçamentária direta ou gestão do Profisco, afetas à PGA/USF/SEFAZ, e resguardada a análise técnico-jurídica formal de PLs pela ASJUR), consolidando as ações de articulação institucional para captação/parcerias (`E3.O1.KR1`) e mitigação preventiva de riscos governamentais e socioambientais (`E5.O4.KR1` e `E5.O4.KR2`).
  Solicita-se o despacho padrão de validação para encerramento da instrução setorial.
  ```"""
        if old_pgari_block in t:
            t = t.replace(old_pgari_block, new_pgari_block)
        with open(kit_path, "w", encoding="utf-8") as f:
            f.write(t)

    # 6. Atualizar Comunicacoes_Intersetoriais_SEI_TIC_ASCOM_Brasilia.md
    com_path = os.path.join(BASE_DIR, "Comunicacoes_Intersetoriais_SEI_TIC_ASCOM_Brasilia.md")
    if os.path.exists(com_path):
        with open(com_path, "r", encoding="utf-8") as f:
            t = f.read()
        t = t.replace(
            "As chefias da Procuradoria Judicial (Dr. Daniel Blume), Procuradoria da Saúde (Dr. Zacarias) e Procuradoria de Brasília (Dr. Gabriel)",
            "As equipes e chefias da Procuradoria dos Juizados Especiais da Fazenda Pública (Dr. Lucas Leite), Procuradoria da Saúde (corpo de assessoria) e Procuradoria de Brasília (Dr. Ricardo Séllos)"
        )
        t = t.replace(
            "Procuradoria de Brasília (`PB`) — Dr. Gabriel (Chefe da Procuradoria de Brasília)",
            "Procuradoria de Brasília (`PB`) — Dr. Ricardo Séllos (Procurador-Chefe da Procuradoria de Brasília)"
        )
        t = t.replace(
            "Fica ratificada a diretriz institucional de que a atuação da Procuradoria de Brasília **não envolve a devolução de processos às Especializadas de origem** após a interposição recursal na instância ordinária.",
            "Conforme deliberação da Procuradoria-Geral Adjunta para Assuntos Estratégicos (Dr. Marcus Bacellar), visando evitar retrabalho e sobrecarga de prazos, a atuação da Procuradoria de Brasília **não envolve a devolução operacional de agravos às Especializadas de origem** após a interposição recursal (sem prejuízo de que a ideia de análise didática de casos concretos seja discutida e amadurecida em oficinas pedagógicas conjuntas com a `ESAP` e a `PGAAJ`)."
        )
        with open(com_path, "w", encoding="utf-8") as f:
            f.write(t)

    # 7. Atualizar Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md para refletir PGARI, PSAU, SGA, NCIA, PB, PGAAJ, PJEFP, SGRH, ESAP
    cot_path = os.path.join(BASE_DIR, "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md")
    if os.path.exists(cot_path):
        with open(cot_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        new_lines = []
        current_kr = None
        for line in lines:
            m = re.search(r"Código na Lista Mestre:\*\*\s*`(E\d+\.O\d+\.KR\d+)`", line)
            if m:
                current_kr = m.group(1)

            # Remover linhas expurgadas do Cotejamento:
            # - PSAU, NCIA, SGA, PB de E9.O3.KR1
            if current_kr == "E9.O3.KR1" and any(u in line for u in ["| **Procuradoria da Saúde** |", "| **Núcleo de Combate à Improbidade Administrativa** |", "| **Subprocuradoria-Geral Adjunta** |", "| **Procuradoria de Brasília** |"]):
                continue
            # - NCIA de E6.O1.KR2 e E5.O5.KR2
            if current_kr in ("E6.O1.KR2", "E5.O5.KR2") and "| **Núcleo de Combate à Improbidade Administrativa** |" in line:
                continue
            # - SGA de E6.O1.KR2 e E5.O2.KR2
            if current_kr in ("E6.O1.KR2", "E5.O2.KR2") and "| **Subprocuradoria-Geral Adjunta** |" in line:
                continue
            # - PEDU e PSP: linha duplicada de certificação tecnológica em E7.O3.KR1
            if current_kr == "E7.O3.KR1" and ("| **Procuradoria da Educação** | Certificar a equipe" in line or "| **Procuradoria da Segurança Pública** | Acompanhar certificações tecnológicas" in line):
                continue

            # Atualizar linha de PGAAJ em E5.O6.KR1 (alerta escalonado e perdas evitadas)
            if current_kr == "E5.O6.KR1" and "| **Procuradoria-Geral Adjunta para Assuntos Jurídicos** |" in line:
                if "alerta escalonado" in line.lower():
                    line = "| **Procuradoria-Geral Adjunta para Assuntos Jurídicos** | Apoiar a gestão descentralizada de prazos pelas chefias imediatas no painel nativo do SPA | Fortalecer o acompanhamento preventivo de prazos processuais diretamente pelas chefias imediatas das Especializadas por meio das ferramentas nativas do SPA, sem adoção de regimes intrusivos de alertas paralelos. | Líder: PGAAJ; Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Chefias das Especializadas | 120 dias |"
                elif "perdas evitadas" in line.lower():
                    line = "| **Procuradoria-Geral Adjunta para Assuntos Jurídicos** | Acompanhar relatório mensal de causas-raiz de prazos peremptórios efetivamente perdidos e falhas sistêmicas | Analisar mensalmente, em articulação com a Corregedoria-Geral e a SGA, os relatórios consolidados de prazos peremptórios/preclusivos efetivamente perdidos e eventuais falhas técnicas de captura no SPA, promovendo o saneamento preventivo das causas-raiz. | Líder: PGAAJ; Coexecutores: Corregedoria-Geral (CG), Subprocuradoria-Geral Adjunta (SGA), Assessoria em TIC da PGAAE / INOVA | Mensal |"

            # Atualizar linha de PJEFP sobre Fórum José Sarney
            if "| **Procuradoria dos Juizados Especiais da Fazenda Pública** |" in line and "Fórum José Sarney" in line:
                line = "| **Procuradoria dos Juizados Especiais da Fazenda Pública** | Viabilizar a plena integração digital e comunicacional da unidade descentralizada no Fórum José Sarney com a sede da PGE | Articular junto à Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI) a habilitação plena da Extranet nas estações de trabalho do Fórum Des. José Sarney, e junto ao Serviço de Gestão de Recursos Humanos (SGRH) a inclusão dos servidores descentralizados em canal direto de avisos funcionais e informes da sede/ESAP via WhatsApp. | Líder: PJEFP; Coexecutores: Assessoria em TIC da PGAAE / INOVA (Extranet), Serviço de Gestão de Recursos Humanos - SGRH (Canal de Avisos), ASCOM e SI (Infraestrutura) | 90 dias / Contínuo |"

            # Atualizar linha de SGA em E5.O1.KR2
            if current_kr == "E5.O1.KR2" and "| **Subprocuradoria-Geral Adjunta** | Articular atuação coordenada em pautas de 2º Grau" in line:
                line = "| **Subprocuradoria-Geral Adjunta** | Articular atuação coordenada em pautas de 2º Grau, revezamento virtual de sustentações com Brasília e difusão no YouTube junto à ASCOM | Coordenar o fluxo de pautas perante o TJMA e TRF1, apoiar o sistema de revezamento virtual de sustentações orais nos Tribunais Superiores com a Procuradoria de Brasília (bem como a interlocução metodológica sobre óbices recursais) e remeter à ASCOM os links e minutagens de sustentações orais gravadas no YouTube dos Tribunais para divulgação institucional. | Líder: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: Procuradorias Especializadas, Procuradoria de Brasília (PB), PGAAJ, Assessoria de Comunicação (ASCOM) | Contínuo |"

            new_lines.append(line)

        cot_text = "\n".join(new_lines) + "\n"
        with open(cot_path, "w", encoding="utf-8") as f:
            f.write(cot_text)
        print("Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md atualizado com sucesso.")

if __name__ == "__main__":
    update_all_md_files()
    update_specific_syntheses_and_kits()

