import sys
from pathlib import Path
import openpyxl

sys.path.insert(0, str(Path(__file__).parent))
from saneamento_ascom_e_ti import load_rows, write_sheet_to_all_targets

BASE = Path(r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados")
CONS = BASE / "Planilhas_Pos_Comparacao_Consolidadas"

def save_unit(sigla, rows, t1, t2):
    write_sheet_to_all_targets(sigla, t1, t2, rows)

# 1. PJEFP: Adicionar E5.O1.KR2 (2º P: Presença nas Turmas Recursais e Incidentes de Uniformização)
rows, t1, t2 = load_rows(CONS / "Plano_Acao_Pos_Comparacao_PJEFP.xlsx")
has_e5o1kr2 = any("E5.O1.KR2" in str(r[2]) for r in rows)
if not has_e5o1kr2:
    rows.insert(0, [
        "Eixo 5 – Alcançar maior eficiência e resolutividade nos processos internos e externos",
        "O1: Garantir atuação estratégica nos processos judiciais prioritários",
        "[E5.O1.KR2] KR2: Garantir atuação processual estratégica qualificada em 100% dos processos prioritários monitorados até 2030",
        "Realizar sustentação oral seletiva e entrega de memoriais perante as Turmas Recursais e em Incidentes de Uniformização",
        "Mapear processos com efeito multiplicador, pedidos de uniformização de interpretação de lei (PUIL/Turma de Uniformização) e recursos estratégicos nas Turmas Recursais da Fazenda Pública, assegurando despacho de memoriais sintéticos e sustentação oral seletiva para formação de precedentes favoráveis ao Estado.",
        "Líder: Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP); Coexecutores: PGAAJ, Subprocuradoria-Geral Adjunta (SGA)",
        "Contínuo (2027–2030)"
    ])
save_unit("PJEFP", rows, t1, t2)
print(f"PJEFP atualizado: {len(rows)} acoes (incluido E5.O1.KR2 - 2o P)")

# 2. PSAU: Corrigir KR da linha de 'Êxito Qualificado em Saúde Pública' de E5.O1.KR2 para E5.O1.KR3
rows, t1, t2 = load_rows(CONS / "Plano_Acao_Pos_Comparacao_PSAU.xlsx")
for r in rows:
    if "Êxito Qualificado em Saúde Pública" in str(r[3]):
        r[2] = "[E5.O1.KR3] KR3: Atingir taxa de êxito de 80% nos processos judiciais estratégicos até 2027"
save_unit("PSAU", rows, t1, t2)
print(f"PSAU atualizado: {len(rows)} acoes (E5.O1.KR3 devidamente classificado)")

# 3. PDA: Expurgar os 3 registros residuais de E4.O1.KR2 (exclusivo da Ouvidoria) e incluir E4.O1.KR1 (1º P: Prazo consultivo com SEFAZ/órgãos)
rows, t1, t2 = load_rows(CONS / "Plano_Acao_Pos_Comparacao_PDA.xlsx")
rows = [r for r in rows if "[E4.O1.KR2]" not in str(r[2])]
if not any("[E4.O1.KR1]" in str(r[2]) for r in rows):
    rows.append([
        "Eixo 4 – Melhorar a experiência do usuário dos serviços da PGE",
        "O1: Melhorar a experiência do usuário dos serviços da PGE",
        "[E4.O1.KR1] KR1: Responder ao menos 90% das consultas dos órgãos estaduais dentro do prazo regulamentar até 2030",
        "Garantir resposta tempestiva a ao menos 90% das consultas e expedientes da SEFAZ e órgãos estaduais sobre inscrição e cobrança da Dívida Ativa",
        "Controlar no SEI/SPA o SLA de resposta às consultas técnicas, pedidos de revisão de inscrição, certidões e orientações encaminhados pela SEFAZ e demais órgãos estaduais, assegurando ao menos 90% de atendimento dentro do prazo regulamentar.",
        "Líder: Procuradoria da Dívida Ativa (PDA); Coexecutores: SEFAZ, PGAAJ",
        "Contínuo (2027–2030)"
    ])
save_unit("PDA", rows, t1, t2)
print(f"PDA atualizado: {len(rows)} acoes (expurgado E4.O1.KR2 residual e incluido E4.O1.KR1)")

# 4. Atualizar Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md para refletir a taxonomia canonica exata
p3_path = BASE / "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md"
txt = p3_path.read_text(encoding="utf-8")

# Fix headers in tables
txt = txt.replace(
    "1º P: PRAZO (`E5.O1.KR3` e `E4.O1.KR1`)",
    "1º P: PRAZO (`E5.O6.KR1` e `E4.O1.KR1`)"
).replace(
    "2º P: PRESENÇA NOS TRIBUNAIS (`E5.O1.KR1`, `E5.O2.KR1/KR2` e `E5.O2.KR2`)",
    "2º P: PRESENÇA NOS TRIBUNAIS (`E5.O1.KR1/KR2/KR3` e `E5.O2.KR2`)"
).replace(
    "2º P: PRESENÇA NOS TRIBUNAIS (`E5.O1.KR1`, `E5.O2.KR1/KR2`)",
    "2º P: PRESENÇA NOS TRIBUNAIS (`E5.O1.KR1/KR2/KR3` e `E5.O2.KR2`)"
).replace(
    "3º P: PADRONIZAÇÃO (`E5.O1.KR2`, `E5.O2.KR1`, `E5.O3.KR1/KR2`)",
    "3º P: PADRONIZAÇÃO E PREVENÇÃO (`E5.O5.KR1/KR2` e `E5.O3.KR1/KR2`)"
).replace(
    "3º P: PADRONIZAÇÃO (`E5.O1.KR2`, `E7.O1.KR1`)",
    "3º P: PADRONIZAÇÃO E PREVENÇÃO (`E5.O5.KR1/KR2` e `E5.O3.KR1/KR2`)"
)

# Update PJEFP and PSAU rows in Bloco A table so they reflect the completed sanitation
old_pjefp = "| **5. Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP)**       |    **SIM**<br>Check-list diário de audiências/prazos de 10 dias úteis e matriz de substituição automática.    |         **LACUNA DETECTADA**<br>Excluiu `E5.O1.KR1`, `E5.O2.KR1/KR2` alegando volume massivo (24 audiências/dia) e não possui ação de presença em Turmas Recursais.         |                              **SIM**<br>Kit de defesa rápida e banco de peças padronizadas no Assistente do SPA + Cartilhas para SEGEP/SEDUC/SES/SSP.                              | **Necessita saneamento no 2º P (Presença nos Tribunais):** Embora atue em massa no 1º grau, deve incorporar ação de **sustentação oral e memoriais seletivos perante as Turmas Recursais** e em **Incidentes de Uniformização de Jurisprudência**.                 |"
new_pjefp = "| **5. Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP)**<br>*(Dr. Lucas Leite dos Reis)* | **SIM**<br>Monitoramento diário da fila de prazos de 10 dias úteis (`E5.O6.KR1`) e acionamento imediato da TI diante de instabilidades do SPA. | **SIM (Saneado Pós-Reunião)**<br>Sustentação oral seletiva e despacho de memoriais nas Turmas Recursais e em Incidentes de Uniformização (`E5.O1.KR2`). | **SIM**<br>Adoção da ferramenta MINUTIA/SPA (`E5.O5.KR1`), repositório de minutas padronizadas (`E5.O5.KR2`) e notas de dispensa recursal/acordos (`E5.O3.KR2`). | **100% aderente aos 3 Ps após saneamento.** Incorporada na planilha consolidada a ação de sustentação oral seletiva e memoriais nas Turmas Recursais e Incidentes de Uniformização (`E5.O1.KR2`). |"

old_pb = "| **6. Procuradoria de Brasília**<br>*(Dr. Belande)*                          |             **SIM**<br>Auditoria diária PJe/e-STF/e-STJ vs. SPA e redistribuição imediata em 24h.             |                     **SIM (Foco Nuclear)**<br>Inversão da lógica recursal + Memorial Sintético de 2 páginas e sustentação oral no STF/STJ/TST.                     |                          **PARCIAL (Ajuste PGAAE)**<br>Propôs *\"Fluxo Didático de Agravos\"* devolvendo processos à origem; Dr. Marcus determinou ajuste.                           | **Ajuste determinado no 3º P:** Não devolver processos à origem (para não atrasar prazo); transformar o levantamento de erros técnicos (`Súmulas 7/STJ e 279/STF`) em **Relatório Semestral para Capacitação via ESAP** e banco de modelos de superação de óbices. |"
new_pb = "| **6. Procuradoria de Brasília (PB)**<br>*(Dr. Ricardo Séllos)* | **SIM**<br>Controle diário cruzado de prazos nos portais STF/STJ/TST vs. SPA (`E5.O6.KR1`) e redistribuição imediata. | **SIM (Foco Nuclear)**<br>Carteira estratégica no Monitor PGE (`E5.O1.KR1`), memoriais e sustentações orais presenciais no STF/STJ/TST (`E5.O1.KR2`) e Inversão da Lógica Recursal (`E5.O2.KR2`). | **SIM (Saneado Pós-Reunião)**<br>Repositório padronizado de superação das Súmulas 7/STJ e 279/STF (`E5.O5.KR2`), RPA de triagem (`E5.O5.KR1`) e Relatório Semestral à ESAP/PGAAJ sem devolução operacional à origem (`E5.O2.KR2`). | **100% aderente aos 3 Ps após saneamento.** Acolhida a diretriz do Dr. Marcus Bacellar vedando devolução operacional de agravos à origem (evitando retrabalho), mantendo a discussão pedagógica em oficinas com ESAP/PGAAJ. |"

old_psau = "| **7. Procuradoria da Saúde**<br>*(Dr. Carlos Santana)*                      |     **SIM**<br>Rotina de dupla checagem diária de liminares no PJe/SPA e fluxo de urgência em 24h a 48h.      | **PARCIAL (Reverter Corte)**<br>Manteve `E5.O2.KR1` (despachos/memoriais no TJMA/TRF1), mas havia **suspendido `E5.O2.KR2`** (80% de êxito) e cortado `E5.O2.KR2`. | **PARCIAL (Reverter Corte)**<br>Manteve banco de contestações com NAT-Jus no `E5.O1.KR2`, mas havia **descartado `E5.O2.KR1` e `E5.O3.KR1/KR2`** (padronização preventiva na SES). | **Determinação expressa de Dr. Marcus:** Reverter todos os cortes da Saúde; manter `E5.O2.KR2` (criando ação para definir o conceito de êxito sanitário) e manter `E5.O2.KR1` e `E5.O3.KR1/KR2` (consultoria preventiva e padronização junto à SES).               |"
new_psau = "| **7. Procuradoria da Saúde (PSAU)**<br>*(Reunião com Corpo de Assessores)* | **SIM (Mantido por Decisão da PGAAE)**<br>Conciliação diária PJe/SPA e canal 24h–48h com SES/CEMARC (`E5.O6.KR1`) + SLA de 90% nas consultas da SES (`E4.O1.KR1`). | **SIM (Saneado Pós-Reunião)**<br>Monitor PGE (`E5.O1.KR1`), memoriais e sustentações no TJMA/TRF1 (`E5.O1.KR2`), aferição de Êxito Qualificado em Saúde (`E5.O1.KR3`) e filtro REsp/RE (`E5.O2.KR2`). | **SIM (Saneado Pós-Reunião)**<br>Banco de minutas inteligentes e pareceres NATJUS (`E5.O5.KR2`), triagem automatizada (`E5.O5.KR1`) e notas orientativas/checklists preventivos junto à SES (`E5.O3.KR2`). | **100% aderente aos 3 Ps após saneamento.** Revertidos os cortes e mantido o `E4.O1.KR1` (90% SLA nas consultas da SES) por deliberação do Dr. Marcus Bacellar (PGAAE). |"

txt = txt.replace(old_pjefp, new_pjefp).replace(old_pb, new_pb).replace(old_psau, new_psau)
p3_path.write_text(txt, encoding="utf-8")
print("Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md atualizado.")


# 5. Expurgar as 2 linhas residuais de E4.O1.KR2 da PGAAE e atualizar documentos sobre supressão por impossibilidade material
rows_pgaae, t1_pgaae, t2_pgaae = load_rows(CONS / "Plano_Acao_Pos_Comparacao_PGAAE.xlsx")
before_pgaae = len(rows_pgaae)
rows_pgaae = [r for r in rows_pgaae if "[E4.O1.KR2]" not in str(r[2])]
save_unit("PGAAE", rows_pgaae, t1_pgaae, t2_pgaae)
print(f"PGAAE atualizado: {before_pgaae} -> {len(rows_pgaae)} acoes (expurgado E4.O1.KR2 residual)")

# Verificar 0 ocorrencias de E4.O1.KR2 nas 41 planilhas
rem = 0
for f in CONS.glob("*.xlsx"):
    wb = openpyxl.load_workbook(f)
    ws = wb.active
    for r in range(5, ws.max_row + 1):
        if "E4.O1.KR2" in str(ws.cell(r, 3).value or ""):
            rem += 1
assert rem == 0, f"Ainda restam {rem} linhas de E4.O1.KR2!"
print("Confirmado: 0 linhas de E4.O1.KR2 nas 41 planilhas .xlsx.")

# Atualizar Notas_Tecnicas_Respostas_SEI_ASCOM_Ouvidoria_Financas.md
nt_path = BASE / "Notas_Tecnicas_Respostas_SEI_ASCOM_Ouvidoria_Financas.md"
nt_txt = nt_path.read_text(encoding="utf-8")
old_b = '>    - **b) Unificação institucional da pesquisa de satisfação do usuário externo (`E4.O1.KR2`):** Considerando que os sistemas `e-OUV` e `e-SIC` (geridos pela STC/OGE) não dispõem de módulo nativo de pesquisa de satisfação gerenciável pela PGE-MA, foi suprimida a criação de formulários isolados por setor. O indicador `E4.O1.KR2` (*"Alcançar índice mínimo de 90% de satisfação dos usuários externos quanto à clareza, utilidade e tempestividade das manifestações jurídicas"*) foi estruturado como **pesquisa institucional unificada por amostragem**, com apoio técnico da **Assessoria em TIC da PGAAE / INOVA** (formulário eletrônico no site institucional, QR Code e link nas comunicações oficiais).'
new_b = '>    - **b) Supressão formal da meta quantitativa de satisfação do usuário externo (`E4.O1.KR2`) por impossibilidade material e redirecionamento para capacitação em Escuta Ativa e CNV (`E9.O2.KR1`):** Conforme demonstrado no parecer técnico e na reunião de alinhamento da Ouvidoria-Geral, a PGE-MA não detém governabilidade tecnológica sobre as plataformas oficiais estaduais e federais (`e-OUV`/`Fala.BR` e `e-SIC`, geridas pela `OGE/STC` e `CGU`), as quais não possuem módulo nativo de avaliação de satisfação gerenciável pelo órgão, além do severo viés amostral negativo de formulários voluntários avulsos. Por conseguinte, o indicador `E4.O1.KR2` foi **integralmente suprimido de todas as 41 planilhas setoriais (incluindo Ouvidoria e PGAAE)**, convertendo-se a diretriz de atendimento cordial e humanizado em iniciativa permanente de capacitação institucional em **Escuta Ativa e Comunicação Não Violenta (CNV)** em parceria com a **ESAP** e o **Comitê de Equidade** (`E9.O2.KR1`).'
if old_b in nt_txt:
    nt_path.write_text(nt_txt.replace(old_b, new_b), encoding="utf-8")

# Atualizar Sintese_Encaminhamentos_Pendentes_Planejamento.md
sint_path = BASE / "Sintese_Encaminhamentos_Pendentes_Planejamento.md"
sint_txt = sint_path.read_text(encoding="utf-8")
sint_txt = sint_txt.replace(
    "com expurgo do `E4.O1.KR1`, unificação do `E4.O1.KR2`, métrica de",
    "com expurgo integral do `E4.O1.KR1` e supressão formal do `E4.O1.KR2` (por impossibilidade material das plataformas externas `e-OUV`/`e-SIC`, convertido em capacitação em Escuta Ativa e CNV junto à `ESAP`), métrica de"
)
sint_path.write_text(sint_txt, encoding="utf-8")

# Atualizar Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md
cot_path = BASE / "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md"
cot_txt = cot_path.read_text(encoding="utf-8")
cot_txt = cot_txt.replace(
    "- **Situação de Governança Saneada:** **META EXPURGADA DAS ROTINAS OPERACIONAIS DAS UNIDADES E DA OUVIDORIA / CENTRALIZADA EM PESQUISA CORPORATIVA ANUAL (GABINETE/ASCOM)**",
    "- **Situação de Governança Saneada:** **META INTEGRALMENTE SUPRIMIDA DAS 41 PLANILHAS SETORIAIS POR IMPOSSIBILIDADE MATERIAL DE PLATAFORMA EXTERNA (`e-OUV`/`Fala.BR` E `e-SIC` — `OGE/STC` E `CGU`) E REDIRECIONADA PARA CAPACITAÇÃO EM ESCUTA ATIVA E CNV (`ESAP` / `OUV` — `E9.O2.KR1`)**"
).replace(
    "> * **Canal Único e Exclusivo:** Caso a Administração Superior mantenha o indicador `E4.O1.KR2` no nível estratégico corporativo, sua apuração será realizada **exclusivamente por Pesquisa Amostral Global Anual conduzida centralmente pelo Gabinete do Procurador-Geral e ASCOM**.",
    "> * **Redirecionamento para o Plano de Ação (`E9.O2.KR1`):** Conforme deliberado na reunião da Ouvidoria-Geral, diante da ausência de controle sobre as plataformas estaduais/federais de ouvidoria (`OGE/STC` e `CGU`) e do viés amostral negativo de pesquisas abertas voluntárias, a diretriz de atendimento cordial e humanizado foi convertida em ação permanente de capacitação em **Escuta Ativa e Comunicação Não Violenta (CNV)** junto à `ESAP` e ao Comitê de Equidade."
).replace(
    "concentrando a governança do indicador em pesquisa amostral anual corporativa (Gabinete/ASCOM).",
    "suprimindo o indicador de todas as 41 planilhas por impossibilidade material das plataformas externas (`e-OUV`/`e-SIC`) e convertendo-o em capacitação em Escuta Ativa e CNV junto à `ESAP` (`E9.O2.KR1`)."
)
cot_path.write_text(cot_txt, encoding="utf-8")
print("Todos os documentos .md atualizados com a supressao formal do E4.O1.KR2.")
