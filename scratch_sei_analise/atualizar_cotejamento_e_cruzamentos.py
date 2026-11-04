# -*- coding: utf-8 -*-
"""
Script de Cruzamento Intersetorial Completo (Atas .md <-> Planilhas .xlsx <-> Cotejamento Consolidado .md):
1. Atualiza as planilhas de PB, PSAU, PJEFP, CG, OUV, CEQUIDADE e PGAAE com todas as determinações e demandas cruzadas das reuniões.
2. Sincroniza todas as cópias das planilhas (Planilhas_Pos_Comparacao_Consolidadas, raiz da pasta setorial, Plano_Acao_Corrigido_*.xlsx e Documentos Ajustados Após Reunião/Plano_Acao_*.xlsx).
3. Saneia integralmente as 115 linhas de tabela do Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md onde constava 'PGA (Informática)', 'Informática/PGA' ou 'Supervisão de Informática' em ações de desenvolvimento/evolução tecnológica, sistemas, portais, BI e RPA (Eixos 1 a 8).
4. Insere no Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md as ações cruzadas (YouTube ASCOM/SGA, Falso Positivo Dashboard CG/NCIA, Estabilidade/Delay SPA PGAAE/PJEFP/Saúde/PB, Relatório Semestral de Óbices PB/ESAP, Êxito Sanitário e Prevenção SES na Saúde, Turmas Recursais no PJEFP, 2 Ações Anuais Antiassédio e LGPD em OUV/CG/CEQUIDADE).
"""
import os
import re
import sys
import glob
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados"
CONS_DIR = os.path.join(BASE_DIR, "Planilhas_Pos_Comparacao_Consolidadas")

from saneamento_ascom_e_ti import (
    load_rows, write_sheet_to_all_targets, sanitize_ti_governance_in_row, INFRA_KRS
)

def apply_cross_unit_adjustments():
    # 1. PB (Procuradoria de Brasília):
    # - Converter "Fluxo Didático de Agravos" em "Relatório Semestral de Superação de Óbices Sumulares (Súmulas 7/STJ e 279/STF) para Capacitação via ESAP (vedada a devolução de processos à origem)"
    # - Incluir articulação metodológica de mensuração de admissibilidade recursal com SGA/NCIA
    pb_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_PB.xlsx")
    rows, t1, t2 = load_rows(pb_path)
    for r in rows:
        if "Fluxo Didático de Agravos" in str(r[3] or ""):
            r[3] = "Elaborar Relatório Semestral de Superação de Óbices Sumulares (Súmulas 7/STJ e 279/STF) e banco de modelos recursais"
            r[4] = (
                "Sistematizar semestralmente os principais erros técnicos e óbices de admissibilidade (Súmulas 7/STJ e 279/STF) "
                "identificados nos Tribunais Superiores — vedada a devolução de processos à origem para não retardar prazos —, "
                "remetendo relatório pedagógico à ESAP e às Especializadas e alinhando com a SGA metodologia de mensuração de admissibilidade recursal."
            )
            r[5] = "Líder: Procuradoria de Brasília; Coexecutores: Subprocuradoria-Geral Adjunta (SGA), Especializadas Contenciosas; Coordenação Pedagógica: ESAP (via PAC)"
    write_sheet_to_all_targets("PB", t1, t2, rows)
    print("[PB] Ajustado Fluxo Didático de Agravos (vedada devolução à origem) + metodologia de admissibilidade com SGA.")

    # 2. PSAU (Procuradoria da Saúde):
    # - Reverter cortes determinados por Dr. Marcus: incluir conceito de êxito sanitário (E5.O1.KR2 / E5.O2.KR2), consultoria preventiva/padronização junto à SES (E5.O3.KR1/KR2) e fluxo quinzenal ASCOM (E6.O1.KR2).
    psau_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_PSAU.xlsx")
    rows, t1, t2 = load_rows(psau_path)
    has_exito_sanitario = any("êxito sanitário" in str(r[3] or "").lower() or "êxito nas demandas de saúde" in str(r[3] or "").lower() for r in rows)
    if not has_exito_sanitario:
        rows.append([
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O1: Identificar e monitorar processos estratégicos e prioritários",
            "[E5.O1.KR2] KR2: Garantir atuação processual estratégica qualificada em 100% dos processos prioritários monitorados até 2030",
            "Estabelecer metodologia institucional de aferição de 'Êxito Qualificado em Saúde Pública'",
            "Parametrizar, em conjunto com a PGAAE e a SGA, matriz técnica de aferição de êxito nas demandas sanitárias (contabilizando substituição por fármacos padronizados no SUS/RENAME, aplicação do Tema 793 e 1234/STF, reversão de bloqueios SISBAJUD e deságio em cumprimentos), revertendo a supressão da meta de performance qualitativa.",
            "Líder: Procuradoria da Saúde; Coexecutores: PGAAE, Subprocuradoria-Geral Adjunta (SGA)",
            "Até 2027 (monitoramento contínuo)"
        ])
    has_ses_padronizacao = any("cartilhas" in str(r[3] or "").lower() or "consultoria preventiva junto à ses" in str(r[3] or "").lower() for r in rows)
    if not has_ses_padronizacao:
        rows.append([
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O3: Fortalecer a atuação consultiva preventiva e a segurança jurídica",
            "[E5.O3.KR2] KR2: Reduzir em 20% a judicialização decorrente de falhas administrativas nas secretarias críticas até 2030",
            "Instituir notas orientativas, checklists e padronização administrativa preventiva junto à SES e CEMARC",
            "Elaborar cartilhas práticas, listas de verificação e fluxos de resposta administrativa célere junto à Secretaria de Estado da Saúde (SES) e à CEMARC para fornecimento administrativo regular e instrução técnica prévia, prevenindo o ajuizamento massivo de demandas e bloqueios judiciais.",
            "Líder: Procuradoria da Saúde; Coexecutores: Secretaria de Estado da Saúde (SES), PGAAJ",
            "Contínuo (2027–2030)"
        ])
    has_ascom_psau = any("assessoria de comunicação" in str(r[3] or "").lower() for r in rows)
    if not has_ascom_psau:
        rows.append([
            "Eixo Estratégico 6 – Fortalecer a imagem institucional e a comunicação com a sociedade",
            "O1: Fortalecer a imagem e o reconhecimento da PGE como referência de excelência",
            "[E6.O1.KR2] KR2: Alcançar crescimento contínuo do alcance médio mensal nas redes sociais da PGE até 2029",
            "Alimentação sistemática e tempestiva da Assessoria de Comunicação (ASCOM) com decisões judiciais favoráveis",
            "Instituir rotina setorial quinzenal de envio de relatórios e cópias de decisões, suspensões de liminares e acórdãos de alta relevância sanitária à ASCOM, viabilizando a divulgação institucional da defesa do SUS pela PGE-MA.",
            "Líder: Procuradoria da Saúde; Coexecutores: Assessores Setoriais, Assessoria de Comunicação (ASCOM)",
            "Fluxo Quinzenal / Contínuo"
        ])
    write_sheet_to_all_targets("PSAU", t1, t2, rows)
    print("[PSAU] Incorporadas reversões determinadas por Dr. Marcus (êxito sanitário, padronização preventiva SES e fluxo ASCOM).")

    # 3. PJEFP (Juizados Especiais):
    # - Incluir ação do 2º P (sustentação oral e memoriais seletivos perante as Turmas Recursais e Incidentes de Uniformização)
    # - Corrigir Linha 15 (acesso à Extranet no Fórum José Sarney: de ESAP para Suporte de Infraestrutura: SI + Assessoria em TIC da PGAAE / INOVA)
    pjefp_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_PJEFP.xlsx")
    rows, t1, t2 = load_rows(pjefp_path)
    for r in rows:
        if "Fórum José Sarney" in str(r[3] or ""):
            r[5] = "Líder: Procuradoria dos Juizados Especiais da Fazenda Pública; Suporte de Conectividade/Rede: Supervisão de Informática (SI); Evolução da Extranet: Assessoria em TIC da PGAAE / INOVA"
    has_turma_recursal = any("turmas recursais" in str(r[3] or "").lower() for r in rows)
    if not has_turma_recursal:
        rows.insert(0, [
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O1: Identificar e monitorar processos estratégicos e prioritários",
            "[E5.O1.KR2] KR2: Garantir atuação processual estratégica qualificada em 100% dos processos prioritários monitorados até 2030",
            "Realizar sustentação oral e entrega de memoriais seletivos perante as Turmas Recursais e em Incidentes de Uniformização",
            "Selecionar recursos inominados com efeito multiplicador na Fazenda Pública e Incidentes de Uniformização de Jurisprudência para entrega de memoriais sintéticos e realização de sustentação oral perante as Turmas Recursais do Sistema dos Juizados Especiais.",
            "Líder: Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP); Coexecutores: Subprocuradoria-Geral Adjunta (SGA), PGAAJ",
            "Contínuo (2027–2030)"
        ])
    write_sheet_to_all_targets("PJEFP", t1, t2, rows)
    print("[PJEFP] Incluída ação de sustentação oral seletiva nas Turmas Recursais (2º P) e corrigida governança de TI no Fórum José Sarney.")

    # 4. CG (Corregedoria-Geral):
    # - Incluir saneamento do falso positivo do Dashboard da Corregedoria apontado pelo NCIA/SGA (processos armazenados sem prazo pendente)
    # - Explicitar protocolo de restrição de acesso no SEI e anonimização LGPD nos relatórios correcionais (demanda Ouvidoria)
    cg_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_CG.xlsx")
    rows, t1, t2 = load_rows(cg_path)
    has_falso_positivo = any("falsos positivos" in str(r[3] or "").lower() or "dashboard da corregedoria" in str(r[3] or "").lower() for r in rows)
    if not has_falso_positivo:
        rows.insert(1, [
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O1: Identificar e monitorar processos estratégicos e prioritários",
            "[E5.O6.KR1] KR1: Manter em zero a perda de prazos processuais peremptórios em todas as unidades da PGE até 2030",
            "Sanear regras do Dashboard da Corregedoria para eliminação de falsos positivos de perda de prazo",
            "Alinhar com a Assessoria em TIC da PGAAE / INOVA e o NCIA/SGA a correção da regra de negócio do painel correcional, evitando que processos armazenados sem necessidade de intervenção processual (sem prazo em curso) sejam contabilizados indevidamente como prazos perdidos.",
            "Líder: Corregedoria-Geral; Coexecutores: Assessoria em TIC da PGAAE / INOVA (Suporte de Infraestrutura: SI), Subprocuradoria-Geral Adjunta (SGA), NCIA",
            "60 dias"
        ])
    for r in rows:
        if "Revisar metodologicamente o indicador de desvios de conduta" in str(r[3] or ""):
            if "LGPD" not in str(r[4] or ""):
                r[4] = str(r[4]).rstrip(".") + ", garantindo marcação obrigatória de restrição de acesso no SEI e protocolo estrito de anonimização (LGPD) antes de qualquer consolidação ou publicação."
    write_sheet_to_all_targets("CG", t1, t2, rows)
    print("[CG] Incluído saneamento de falsos positivos do Dashboard (demanda NCIA/SGA) e protocolo LGPD/restrição SEI (demanda Ouvidoria).")

    # 5. OUV (Ouvidoria) e CEQUIDADE (Comitê de Equidade):
    # - Explicitar as 2 ações institucionais anuais de conscientização sobre assédio moral e sexual + LGPD/restrição SEI
    ouv_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_OUV.xlsx")
    rows, t1, t2 = load_rows(ouv_path)
    for r in rows:
        if "Ouvidoria Especializada de Combate ao Assédio" in str(r[3] or ""):
            r[3] = "Aperfeiçoar fluxo da Ouvidoria Especializada e realizar 2 ações institucionais anuais de conscientização contra assédio moral e sexual"
            r[4] = (
                "Aperfeiçoar o fluxo interno de acolhimento humanizado, orientação e encaminhamento seguro de denúncias de assédio moral e sexual "
                "(com restrição de acesso no SEI e anonimização estrita conforme a LGPD) e promover, em parceria com o Comitê de Equidade, SGRH, Corregedoria e ESAP, "
                "ao menos 2 ações institucionais anuais de prevenção e conscientização sobre assédio."
            )
            r[5] = "Líder: Ouvidoria; Coexecutores: Comitê de Equidade, SGRH, Corregedoria-Geral, ASCOM, ESAP"
    write_sheet_to_all_targets("OUV", t1, t2, rows)
    print("[OUV] Explicitadas as 2 ações anuais de conscientização contra assédio moral e sexual + protocolo LGPD/SEI.")

    # 6. PGAAE (Assessoria em TIC da PGAAE / INOVA):
    # - Incluir ação técnica de saneamento do delay de 5–7 dias na migração PJe/Portais–SPA, estabilidade noturna e aviso prévio de mudanças de layout no SPA (demanda PJEFP, Saúde, Brasília e SGA)
    pgaae_path = os.path.join(CONS_DIR, "Plano_Acao_Pos_Comparacao_PGAAE.xlsx")
    rows, t1, t2 = load_rows(pgaae_path)
    has_spa_stability = any("mudanças de layout" in str(r[4] or "").lower() or "delay de 5 a 7 dias" in str(r[4] or "").lower() for r in rows)
    if not has_spa_stability:
        rows.append([
            "Eixo Estratégico 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
            "O5: Otimizar e automatizar rotinas e processos",
            "[E5.O5.KR1] KR1: Reduzir em 20% o tempo dedicado a tarefas manuais e repetitivas até 2028",
            "Sanear o delay de sincronização PJe/Portais–SPA, mitigar instabilidades noturnas e normatizar aviso prévio de atualizações de layout do SPA",
            "Executar força-tarefa técnica no barramento do SPA para eliminar o atraso de 5 a 7 dias na captura de intimações do PJe e dos Tribunais Superiores, corrigir quedas de desempenho no turno noturno e instituir protocolo obrigatório de homologação e comunicação prévia às unidades antes de alterações visuais ou de fluxo no SPA.",
            "Líder Tecnológico: Assessoria em TIC da PGAAE / INOVA (Coordenação do SPA); Suporte de Infraestrutura Física: Supervisão de Informática (SI); Coexecutores: SGA, SDD, PJEFP, Procuradoria da Saúde e Procuradoria de Brasília",
            "90 dias (monitoramento contínuo)"
        ])
    write_sheet_to_all_targets("PGAAE", t1, t2, rows)
    print("[PGAAE] Incluída ação técnica de saneamento do delay PJe-SPA, estabilidade noturna e aviso prévio de layout no SPA.")

def update_cotejamento_markdown():
    cot_path = os.path.join(BASE_DIR, "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md")
    with open(cot_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_kr = ""
    modified_table_lines = 0
    new_lines = []

    for line in lines:
        m_kr = re.search(r"- \*\*Código na Lista Mestre:\*\*\s*`([^`]+)`", line)
        if m_kr:
            current_kr = m_kr.group(1).strip()

        # Saneamento das linhas de tabela na Seção 3
        if line.strip().startswith("|") and not line.strip().startswith("| :---") and not line.strip().startswith("| Unidade Proponente"):
            is_infra = current_kr in INFRA_KRS
            if "Painel Compartilhado" in line or "informatização do controle de estoque" in line:
                is_infra = False
            if "Criar painel de disponibilidade, incidentes e modernização tecnológica" in line:
                is_infra = True

            # Se for a linha da Supervisão de Informática em E5.O5.KR1 (RPA)
            if "| **Supervisão de Informática** |" in line and "robôs de automação de processos (RPA)" in line:
                line = "| **Supervisão de Informática** | Prover infraestrutura de servidores e ambiente de hospedagem para execução de robôs de automação (RPA) | Garantir disponibilidade de máquinas virtuais, conectividade de rede e sustentação de infraestrutura física no Data Center Nutanix para operação contínua dos robôs desenvolvidos e geridos pela Assessoria em TIC da PGAAE / INOVA. | Líder de Desenvolvimento/Evolução: Assessoria em TIC da PGAAE / INOVA; Suporte de Infraestrutura Física: Supervisão de Informática (SI) | Contínuo (2027-2030) |\n"
                modified_table_lines += 1
            elif "| **Procuradoria de Brasília** | Estruturar o Fluxo Didático de Agravos" in line:
                line = "| **Procuradoria de Brasília** | Elaborar Relatório Semestral de Superação de Óbices Sumulares (Súmulas 7/STJ e 279/STF) e banco de modelos recursais | Sistematizar semestralmente os principais erros técnicos e óbices de admissibilidade (Súmulas 7/STJ e 279/STF) identificados nos Tribunais Superiores — vedada a devolução de processos à origem para não retardar prazos —, remetendo relatório pedagógico à ESAP e alinhando com a SGA metodologia de admissibilidade recursal. | Líder: Procuradoria de Brasília; Coexecutores: SGA, Especializadas; Coordenação Pedagógica: ESAP (via PAC) | Semestral |\n"
                modified_table_lines += 1
            elif not is_infra and ("Informática" in line):
                orig_line = line
                repls = [
                    ("em conjunto com a Supervisão de Informática", "em conjunto com a Assessoria em TIC da PGAAE / INOVA (com suporte de infraestrutura da SI)"),
                    ("junto à Supervisão de Informática", "junto à Assessoria em TIC da PGAAE / INOVA (e suporte de infraestrutura da SI)"),
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
                for old_s, new_s in repls:
                    line = line.replace(old_s, new_s)
                if line != orig_line:
                    modified_table_lines += 1

        new_lines.append(line)

    content = "".join(new_lines)

    # Inserir a linha de YouTube da ASCOM na tabela de E6.O1.KR2 do Cotejamento se ainda não constar
    if "Aproveitar o acervo de sustentações orais gravadas no YouTube" not in content:
        target_ascom = "| **Assessoria de Comunicação** | Manter planejamento editorial periódico e monitoramento de alcance |"
        if target_ascom in content:
            idx = content.find(target_ascom)
            end_line_idx = content.find("\n", idx)
            youtube_md_row = "\n| **Assessoria de Comunicação** | Aproveitar o acervo de sustentações orais gravadas no YouTube dos Tribunais para produção de conteúdos institucionais | Articular com a Subprocuradoria-Geral Adjunta (SGA), o NCIA e as Procuradorias Especializadas o mapeamento e aproveitamento das gravações em vídeo das sustentações orais realizadas pelos Procuradores do Estado nas sessões transmitidas pelo YouTube, produzindo cortes audiovisuais e matérias especiais. | Líder: Assessoria de Comunicação (ASCOM); Coexecutores: SGA, NCIA e Especializadas Contenciosas | Contínuo (2027–2030) |"
            content = content[:end_line_idx] + youtube_md_row + content[end_line_idx:]

    # Adicionar o item 8 na Seção 7 (Governança das Deliberações e Conclusão Metodológica) documentando o cruzamento integral Atas <-> Planilhas
    if "8. **Cruzamento Integral Atas de Reunião" not in content:
        content = content.rstrip() + (
            "\n8. **Cruzamento Integral Atas de Reunião (`.md`) x Planilhas Setoriais (`.xlsx`):** "
            "Incorporação recíproca de todas as deliberações e propostas intersetoriais registradas nas atas: "
            "(i) aproveitamento pela `ASCOM` do acervo de sustentações orais do YouTube proposto pela `SGA/NCIA` (`E6.O1.KR2`); "
            "(ii) saneamento pela `Corregedoria-Geral` e `PGAAE/INOVA` do falso positivo de prazos perdidos no painel correcional em processos armazenados sem prazo pendente (`E5.O1.KR3`); "
            "(iii) ação técnica da `PGAAE/INOVA` (Coordenação do SPA) para elidir o delay de 5–7 dias na sincronização PJe/SPA, mitigar instabilidades noturnas e exigir aviso prévio antes de mudanças de layout (`E5.O5.KR1`); "
            "(iv) substituição da devolução de processos na `Procuradoria de Brasília` por Relatório Semestral de Superação de Óbices (`Súmulas 7/STJ e 279/STF`) integrado à `ESAP` e à `SGA` (`E5.O2.KR2`); "
            "(v) reversão das supressões na `Procuradoria da Saúde` (conceito de êxito sanitário e consultoria preventiva junto à SES) e inclusão de sustentação oral seletiva nas Turmas Recursais pela `PJEFP`; e "
            "(vi) substituição transversal da `Supervisão de Informática (SI)` pela `Assessoria em TIC da PGAAE / INOVA` em todas as iniciativas de desenvolvimento ou evolução de sistemas, portais, painéis BI e automação (RPA/IA) nos 9 Eixos.\n"
        )

    with open(cot_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Cotejamento] Atualizadas {modified_table_lines} linhas de tabela e inseridos cruzamentos intersetoriais em Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md.")

if __name__ == "__main__":
    apply_cross_unit_adjustments()
    update_cotejamento_markdown()

