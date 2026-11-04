# -*- coding: utf-8 -*-
"""
Script Definitivo de Atualização do Relatório dos 3 Ps Obrigatórios:
1. Desfaz qualquer mojibake prévio e garante Unicode UTF-8 puro.
2. Incorpora a consideração fática: PT, PA, PDA, PCF, PERJP, PGAAE e PGA ainda não responderam nem encaminharam respostas via SEI.
3. Registra as 5 unidades com processos SEI respondidos: NIRF (Proc. 2026.11103.07215), Consultoria-Geral/ASJUR (Proc. 2025.11103.05165), SGRH (Proc. 2026.11103.07207), SMP (Proc. 2026.11103.07208) e SGT (Proc. 2026.11103.07209).
4. Demonstra a prontidão instrumental das planilhas saneadas pós-comparação de 7 colunas em Planilhas_Pos_Comparacao_Consolidadas.
5. Harmoniza a taxonomia com a Lista Mestre canônica (E5.O1.KR1/2/3, E5.O2.KR1/2, E4.O1.KR1, E6.O1.KR2, E7.O1.KR1).
6. Registra o expurgo de E4.O1.KR2 e o fluxo contencioso-ASCOM em E6.O1.KR2.
7. Gera arquivos Markdown em UTF-8 (no pai e nos saneados) e documentos Word (.docx).
"""
import os
import re
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

BASE_PARENT = r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados"
BASE_SANEADOS = os.path.join(BASE_PARENT, "Planos de Ação Saneados")

SRC_MD = os.path.join(BASE_SANEADOS, "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md")
DEST_MD_PARENT = os.path.join(BASE_PARENT, "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md")
DEST_MD_SANEADOS = SRC_MD
DEST_DOCX_PARENT = os.path.join(BASE_PARENT, "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.docx")
DEST_DOCX_SANEADOS = os.path.join(BASE_SANEADOS, "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.docx")

with open(SRC_MD, "r", encoding="utf-8") as f:
    raw_content = f.read()

# Desfaz o mojibake
try:
    text = raw_content.encode('cp1252').decode('utf-8')
except Exception:
    text = raw_content

# Harmonização de KRs para a Lista Mestre Canônica
kr_replacements = [
    ("`E5_O6_KR1`", "`E5.O1.KR3`"),
    ("E5_O6_KR1", "E5.O1.KR3"),
    ("`E4_O1_KR1`", "`E4.O1.KR1`"),
    ("E4_O1_KR1", "E4.O1.KR1"),
    ("`E5_O1_KR1/KR2/KR3`", "`E5.O1.KR1`, `E5.O2.KR1/KR2`"),
    ("E5_O1_KR1/KR2/KR3", "`E5.O1.KR1`, `E5.O2.KR1/KR2`"),
    ("`E5_O1_KR1`", "`E5.O1.KR1`"),
    ("E5_O1_KR1", "E5.O1.KR1"),
    ("`E5_O1_KR2`", "`E5.O2.KR1`"),
    ("E5_O1_KR2", "E5.O2.KR1"),
    ("`E5_O1_KR3`", "`E5.O2.KR2`"),
    ("E5_O1_KR3", "E5.O2.KR2"),
    ("`E5_O2_KR2`", "`E5.O2.KR2`"),
    ("E5_O2_KR2", "E5.O2.KR2"),
    ("`E5_O5_KR1/KR2`", "`E5.O1.KR2`"),
    ("E5_O5_KR1/KR2", "`E5.O1.KR2`"),
    ("`E5_O5_KR1`", "`E5.O1.KR2`"),
    ("E5_O5_KR1", "E5.O1.KR2"),
    ("`E5_O5_KR2`", "`E5.O1.KR2`"),
    ("E5_O5_KR2", "E5.O1.KR2"),
    ("`E7_O1_KR1`", "`E7.O1.KR1`"),
    ("E7_O1_KR1", "E7.O1.KR1"),
    ("`E7_O1_KR2`", "`E7.O1.KR1`"),
    ("E7_O1_KR2", "E7.O1.KR1"),
    ("`E5_O2_KR1`", "`E5.O2.KR1`"),
    ("E5_O2_KR1", "E5.O2.KR1"),
    ("`E5_O3_KR1/KR2`", "`E5.O3.KR1/KR2`"),
    ("E5_O3_KR1/KR2", "E5.O3.KR1/KR2")
]

for old, new in kr_replacements:
    text = text.replace(old, new)

# 1. Atualização do Título e Seção 0 (Escopo e Status Fático SEI)
p_sec0 = text.find("## Quadro-Diagnóstico Geral")
if p_sec0 != -1:
    header_new = """# Consolidação dos "3 Ps" nas 14 Procuradorias Especializadas e Regionais (Planejamento Estratégico PGE-MA 2027–2030)
### Estruturação Conforme a Lista Mestre Canônica e Status Atual de Respostas SEI
**Data de Atualização:** Outubro de 2026  
**Referência Metodológica:** `Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md` e `Lista_Mestre_Resultados_Chave_Pos_Reunioes_Chefias.docx`

> [!IMPORTANT]
> **Delimitação de Escopo e Status Fático de Tramitação no SEI:**
> - **Unidades que incorporam diretamente metas e ações dos "3 Ps" (*1. Prazo*, *2. Presença nos Tribunais*, *3. Padronização*):** As **14 Procuradorias Especializadas Temáticas e Regionais** da atividade finalística contenciosa e consultiva da PGE-MA, classificadas sob a ótica de tramitação formal em dois blocos:
>   - **Bloco A — 7 Procuradorias com Reunião Presencial Realizada / Ajustes Técnicos Consolidados:** `Procuradoria Judicial (PJ)`, `Procuradoria da Educação (SEDUC/PEDU)`, `Procuradoria da Segurança Pública (PSP)`, `Procuradoria do Patrimônio Imobiliário e Meio Ambiente (PPIMA)`, `Procuradoria dos Juizados Especiais da Fazenda Pública (PJEFP)`, `Procuradoria de Brasília (PB)` e `Procuradoria da Saúde` *(com anotações específicas para o `Núcleo de Combate à Improbidade Administrativa - NCIA` e a `Assessoria Jurídica / Consultoria`)*.
>   - **Bloco B — 7 Procuradorias Especializadas e Regionais que AINDA NÃO RESPONDERAM NEM ENCAMINHARAM MANIFESTAÇÃO NO SEI:** `Procuradoria Trabalhista (PT)`, `Procuradoria Administrativa (PA)`, `Procuradoria da Dívida Ativa (PDA)`, `Procuradoria do Contencioso Fiscal (PCF)`, `Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP)`, `Procuradoria Regional de Imperatriz (PRI)` e `Procuradoria Regional de Timon (PRT)`.
>   - **Órgãos de Cúpula Coordenadora PENDENTES DE CONSOLIDAÇÃO NO SEI:** `Procurador-Geral Adjunto (PGA)` e `Procuradora-Geral Adjunta para Assuntos Estratégicos (PGAAE)` *(exercem coordenação superior e normatização, atuando na homologação do caderno macro)*.
> - **Unidades com Processos Efetivamente Respondidos e Tramitados via SEI (5 unidades):** Registra-se que, no âmbito global da PGE, **apenas 5 unidades responderam formalmente seus processos no SEI até este momento**:
>   1. *NIRF — Núcleo de Inteligência e Recuperação Fiscal:* Processo nº `2026.11103.07215` (Despacho nº 50/2026 dispensando planilha autônoma e integrando sua inteligência à PDA);
>   2. *Consultoria-Geral / Assessoria Especial:* Processo nº `2025.11103.05165` (Memorando nº 38/2026 fixando tempestividade qualificada e expurgo do contencioso);
>   3. *Serviço de Gestão de Recursos Humanos (SGRH):* Processo nº `2026.11103.07207` (Despacho nº 018120848);
>   4. *Serviço de Material e Patrimônio (SMP):* Processo nº `2026.11103.07208` (Despacho nº 057/2026);
>   5. *Serviços Gerais e Transportes (SGT):* Processo nº `2026.11103.07209` (Despacho nº 56/2026).
> - **Prontidão Instrumental das Planilhas Saneadas:** A ausência de resposta formal de PT, PA, PDA, PCF, PERJP, PGAAE e PGA não paralisa o planejamento: a Assessoria de Planejamento já elaborou previamente as **planilhas saneadas pós-comparação estruturadas no padrão canônico de 7 colunas** ([Planilhas_Pos_Comparacao_Consolidadas](file:///c:/Users/brunogomes/Documents/Planejamento%20Estrat%C3%A9gico/Planos%20de%20A%C3%A7%C3%A3o%20Individualizados/Planos%20de%20A%C3%A7%C3%A3o%20Saneados/Planilhas_Pos_Comparacao_Consolidadas)), cobrindo os 3 Ps e prontas para servirem de base material à cobrança e despacho simplificado de encerramento no SEI.

---

"""
    text = header_new + text[p_sec0:]

# 2. Atualização da Seção 1 (Bloco B)
p_bloco_b = text.find("### Bloco B")
p_fim_bloco_b = text.find("## 1. 1º\"P\"")
if p_bloco_b != -1 and p_fim_bloco_b != -1:
    bloco_b_new = """### Bloco B — 7 Procuradorias Especializadas e Regionais Pendentes de Resposta Formal no SEI

> [!WARNING]
> **Status Metodológico e Fático das Especializadas e Regionais Pendentes de Resposta no SEI:**
> As 7 Procuradorias Especializadas e Regionais abaixo (`PT`, `PA`, `PDA`, `PCF`, `PERJP`, `PRI`, `PRT`), assim como as cúpulas `PGAAE` e `PGA`, **de fato ainda não responderam e não encaminharam manifestação ou despacho conclusivo via sistema SEI**.
> No entanto, a Assessoria de Planejamento já superou a precariedade das antigas versões preliminares:
> 1. **Superação das Planilhas Genéricas:** As Procuradorias Regionais de Imperatriz e de Timon não possuem mais as antigas "60 linhas genéricas corporativas"; foram totalmente remodeladas e saneadas em cadernos individualizados de **53 linhas cada**, contendo rotinas operacionais específicas para as comarcas e varas regionais do interior e cobertura plena dos 3 Ps.
> 2. **Saneamento e Balanceamento das Especializadas:** As planilhas pós-comparação de `PT` (31 linhas), `PA` (29 linhas), `PDA` (139 linhas, já com NIRF integrado), `PCF` (44 linhas) e `PERJP` (21 linhas) foram consolidadas no formato canônico oficial de 7 colunas ([Planilhas_Pos_Comparacao_Consolidadas](file:///c:/Users/brunogomes/Documents/Planejamento%20Estrat%C3%A9gico/Planos%20de%20A%C3%A7%C3%A3o%20Individualizados/Planos%20de%20A%C3%A7%C3%A3o%20Saneados/Planilhas_Pos_Comparacao_Consolidadas)).
> 3. **Incorporação das Novas Diretrizes de Governança:** Todas as planilhas do contencioso já receberam a inclusão do fluxo quinzenal obrigatório de envio de decisões e acórdãos para a Assessoria de Comunicação (`E6.O1.KR2`) e tiveram expurgadas as metas de satisfação setorial (`E4.O1.KR2`).

| Procuradoria Especializada / Regional (Pendente de Resposta SEI) | 1º P: PRAZO (`E5.O1.KR3` e `E4.O1.KR1`) | 2º P: PRESENÇA NOS TRIBUNAIS (`E5.O1.KR1`, `E5.O2.KR1/KR2`) | 3º P: PADRONIZAÇÃO (`E5.O1.KR2`, `E7.O1.KR1`) | Status SEI e Pauta de Validação com a Chefia |
| :--- | :---: | :---: | :---: | :--- |
| **8. Procuradoria Trabalhista (PT)**<br>*(31 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Dupla checagem diária PJe-JT/TRT16, plantão 24h–48h contra revelia e protocolo antecipado `D-3`. | **SANEADO NA PLANILHA**<br>Despachos e sustentações no TRT16 (`E5.O2.KR1`), Recursos de Revista ao TST (`E5.O2.KR2`) e fluxo ASCOM (`E6.O1.KR2`). | **SANEADO NA PLANILHA**<br>Banco de peças Tema 246/STF, RO com IA, dispensa recursal (Súmula 126/TST) e Cartilha de Terceirização (GFIP). | **PENDENTE DE RESPOSTA NO SEI.**<br>A planilha pós-comparação de 31 linhas já está saneada e pronta. Tramitar no SEI para validação da chefia sobre Recursos ao TST e fluxo ASCOM. |
| **9. Procuradoria Administrativa (PA)**<br>*(29 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Protocolo "Prazo Zero Perdido" em MS/servidores, alerta 48h e SLA consultivo qualificado (`E4.O1.KR1`). | **SANEADO NA PLANILHA**<br>Despachos e sustentações no TJMA em licitações/PPP (`E5.O2.KR1`) e admissibilidade REsp/RE (`E5.O2.KR2`). | **SANEADO NA PLANILHA**<br>Modelos inteligentes da Lei 14.133/21, pareceres referenciais e automação com IA (`E7.O1.KR1`). | **PENDENTE DE RESPOSTA NO SEI.**<br>A planilha de 29 linhas já acolheu as diretrizes da Consultoria (tempestividade qualificada). Tramitar no SEI para despacho de validação da chefia. |
| **10. Procuradoria da Dívida Ativa (PDA)**<br>*(139 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Protocolo "Prazo Zero Perdido" em execuções fiscais, EPE, embargos e auditoria mensal de prescrição. | **SANEADO NA PLANILHA**<br>Revisão de grandes devedores (> R$ 1 mi), IDPJ no TJMA e atuação estratégica integrada à cobrança. | **SANEADO NA PLANILHA**<br>Esteira fiscal com IA, manual de cobrança e absorção integral da inteligência do NIRF (Despacho SEI nº 50/2026). | **PENDENTE DE RESPOSTA NO SEI.**<br>A planilha de 139 linhas consolidou a fusão das ações do NIRF à PDA. Tramitar no SEI para homologação formal pelo Procurador-Chefe. |
| **11. Procuradoria do Contencioso Fiscal (PCF)**<br>*(44 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Plantão 24h–48h para tutelas fiscais (mercadorias/CPEN), dupla checagem PJe/TJMA/TRF1 e protocolo SEFAZ. | **SANEADO NA PLANILHA**<br>Grandes litígios (DIFAL, TUST/TUSD, ICMS), atuação perante STF/STJ com Brasília (`E5.O2.KR2`) e fluxo ASCOM (`E6.O1.KR2`). | **SANEADO NA PLANILHA**<br>Banco de peças IPVA/ITCD/taxas/CPEN, glosa de ICMS, pareceres ao TARF/COTRI e Cartilha para SEFAZ. | **PENDENTE DE RESPOSTA NO SEI.**<br>A planilha de 44 linhas já está balanceada nos 3 Ps. Tramitar no SEI para validação da chefia sobre acompanhamento conjunto em Brasília. |
| **12. Proc. de Execuções e Requisições de Pagamento (PERJP)**<br>*(21 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Programa "Prazo Zero Perdido" no art. 535 CPC, triagem com Núcleo de Cálculos e prevenção de travas no SPA. | **SANEADO NA PLANILHA**<br>Grandes execuções e precatórios bilionários, despachos nas Varas da Fazenda e Comitê de Precatórios (TJMA/TRT16). | **SANEADO NA PLANILHA**<br>Minutas automatizadas de impugnação ao cumprimento de sentença, checklist pré-pagamento de RPV e acordos diretos. | **PENDENTE DE RESPOSTA NO SEI.**<br>A planilha de 21 linhas está enxuta e focada na execução contra a Fazenda. Tramitar no SEI para validação da chefia setorial. |
| **13. Procuradoria Regional de Imperatriz (PRI)**<br>*(53 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Dupla checagem PJe/SPA nas comarcas do polo, regra de protocolo `D-3` e matriz de substituição em audiências. | **SANEADO NA PLANILHA**<br>Despachos com magistrados do polo de Imperatriz, fluxo de acionamento das Especializadas da Capital e fluxo ASCOM (`E6.O1.KR2`). | **SANEADO NA PLANILHA**<br>Uso compartilhado dos bancos de peças e pareceres referenciais da capital (PJ, Saúde, SEDUC, PCF) via SPA/Alexandria. | **PENDENTE DE RESPOSTA NO SEI.**<br>Superada a versão genérica anterior! Planilha customizada com 53 linhas pronta. Tramitar no SEI para validação do Procurador Regional. |
| **14. Procuradoria Regional de Timon (PRT)**<br>*(53 linhas na planilha saneada pós-comparação)* | **SANEADO NA PLANILHA**<br>Dupla checagem PJe/SPA nas comarcas do polo, regra de protocolo `D-3` e matriz de substituição em audiências. | **SANEADO NA PLANILHA**<br>Despachos com magistrados do polo de Timon, fluxo de acionamento das Especializadas da Capital e fluxo ASCOM (`E6.O1.KR2`). | **SANEADO NA PLANILHA**<br>Uso compartilhado dos bancos de peças e pareceres referenciais da capital (PJ, Saúde, SEDUC, PCF) via SPA/Alexandria. | **PENDENTE DE RESPOSTA NO SEI.**<br>Superada a versão genérica anterior! Planilha customizada com 53 linhas pronta. Tramitar no SEI para validação do Procurador Regional. |
| **Cúpula Coordenadora: PGAAE e PGA**<br>*(Atuação transversal de governança macro)* | **COORDENAÇÃO E AUDITORIA**<br>Diretriz institucional de tolerância zero para perda de prazos e validação dos SLAs de tempestividade qualificada. | **COORDENAÇÃO E AUDITORIA**<br>Alinhamento dos processos estratégicos de grande impacto financeiro e representação institucional nos Tribunais. | **COORDENAÇÃO E AUDITORIA**<br>Homologação dos pareceres referenciais corporativos, diretrizes de IA com INOVA e governança da Lista Mestre. | **PENDENTE DE CONSOLIDAÇÃO NO SEI.**<br>Recebimento dos despachos setoriais conclusivos para submissão final ao Gabinete do Procurador-Geral do Estado. |

---

"""
    text = text[:p_bloco_b] + bloco_b_new + text[p_fim_bloco_b:]

# 3. Atualização da Seção 4 (Roteiro de Intervenção e Tramitação no SEI)
p_sec4 = text.find("## 4. Roteiro de Intervenção")
if p_sec4 == -1:
    p_sec4 = text.find("## 4. Roteiro")
p_sec5 = text.find("## 5. Papel Apartado")
if p_sec4 != -1 and p_sec5 != -1:
    sec4_new = """## 4. Roteiro Operacional de Tramitação e Validação no SEI (Bloco B e Cúpula)

Como as unidades **PT, PA, PDA, PCF, PERJP, PRI e PRT (e as cúpulas PGA e PGAAE) ainda não encaminharam respostas formais via sistema SEI**, a Assessoria de Planejamento estruturou um **fluxo direto de anexação e cobrança documental**.

Para cada uma das unidades pendentes, a Assessoria de Planejamento já disponibilizou o arquivo consolidado em [Planilhas_Pos_Comparacao_Consolidadas](file:///c:/Users/brunogomes/Documents/Planejamento%20Estrat%C3%A9gico/Planos%20de%20A%C3%A7%C3%A3o%20Individualizados/Planos%20de%20A%C3%A7%C3%A3o%20Saneados/Planilhas_Pos_Comparacao_Consolidadas). O processo no SEI deve ser instruído com a planilha correspondente para que a chefia lance o despacho padrão simplificado:
> *"Com reunião presencial e documento anexado, valido os dados e o processo."*

Recomendações específicas para o saneamento do processo SEI de cada unidade:

1. **Procuradoria Trabalhista (`PT`):**
   - **Arquivo Pronto para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PT.xlsx` (31 linhas).
   - **Status nos 3 Ps:** Já incorpora regra `D-3` no `E5.O1.KR3`, Recursos de Revista perante o TST (`E5.O2.KR2`), e o fluxo quinzenal de envio de vitórias para a ASCOM (`E6.O1.KR2`).
   - **Providência SEI:** Anexar a planilha de 31 linhas e colher despacho conclusivo do Procurador-Chefe da PT.

2. **Procuradoria Administrativa (`PA`):**
   - **Arquivo Pronto para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PA.xlsx` (29 linhas).
   - **Status nos 3 Ps:** Alinhada à tese de tempestividade qualificada e não linear da Consultoria (Memorando nº 38/2026), contemplando automação de pareceres com IA (`E7.O1.KR1`) e modelos da Lei nº 14.133/2021.
   - **Providência SEI:** Anexar a planilha de 29 linhas no processo SEI e colher manifestação homologatória da chefia.

3. **Procuradoria da Dívida Ativa (`PDA`):**
   - **Arquivo Pronto para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PDA.xlsx` (139 linhas).
   - **Status nos 3 Ps:** Incorpora a fusão das ações do NIRF determinada pelo Despacho SEI nº 50/2026 (Processo nº 2026.11103.07215), consolidando transação tributária, SISBAJUD, protesto e esteira automatizada.
   - **Providência SEI:** Anexar a planilha de 139 linhas e cientificar o Procurador-Chefe da unificação NIRF/PDA.

4. **Procuradoria do Contencioso Fiscal (`PCF`):**
   - **Arquivo Pronto para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PCF.xlsx` (44 linhas).
   - **Status nos 3 Ps:** Contempla tutela fiscal urgente, teses financeiras no TJMA/TRF1, atuação coordenada com Brasília nos Tribunais Superiores (`E5.O2.KR2`) e alimentação da ASCOM (`E6.O1.KR2`).
   - **Providência SEI:** Anexar a planilha de 44 linhas no processo SEI para chancela da chefia.

5. **Procuradoria de Execuções e Requisições Judiciais de Pagamento (`PERJP`):**
   - **Arquivo Pronto para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PERJP.xlsx` (21 linhas).
   - **Status nos 3 Ps:** Foco estrito em impugnações do art. 535 do CPC com apoio do Núcleo de Cálculos, dupla checagem de RPVs e acordos diretos de precatórios com deságio.
   - **Providência SEI:** Anexar a planilha de 21 linhas no processo SEI e colher despacho de encerramento.

6. **Procuradorias Regionais de Imperatriz (`PRI`) e de Timon (`PRT`):**
   - **Arquivos Prontos para Anexação no SEI:** `Plano_Acao_Pos_Comparacao_PRI.xlsx` (53 linhas) e `Plano_Acao_Pos_Comparacao_PRT.xlsx` (53 linhas).
   - **Status nos 3 Ps:** Superação definitiva do espelhamento genérico! Os cadernos contemplam dupla checagem PJe/SPA nas comarcas do polo, regra `D-3`, despacho com magistrados locais, fluxo de subida de recursos para sustentação oral pela capital (`PJ`, `PT`, `PCF`, `Saúde`) e fluxo ASCOM.
   - **Providência SEI:** Notificar os Procuradores Regionais de Imperatriz e Timon para juntada do despacho padrão no SEI com base nas planilhas de 53 linhas.

7. **Órgãos de Cúpula Coordenadora: PGA e PGAAE:**
   - **Papel Institucional:** Não possuem planilha de execução operacional contenciosa isolada; atuam na governança transversal da Lista Mestre e na validação macro dos cadernos das 41 unidades.
   - **Providência SEI:** Receber os processos conclusos das unidades e instruir a Portaria / Decisão do Procurador-Geral do Estado homologando o Planejamento Estratégico 2027–2030.

---

"""
    text = text[:p_sec4] + sec4_new + text[p_sec5:]

# Gravação dos arquivos Markdown em UTF-8
with open(DEST_MD_PARENT, "w", encoding="utf-8") as f:
    f.write(text)
print(f"[OK] Gravado Markdown Pai (UTF-8): {DEST_MD_PARENT}")

with open(DEST_MD_SANEADOS, "w", encoding="utf-8") as f:
    f.write(text)
print(f"[OK] Gravado Markdown Saneados (UTF-8): {DEST_MD_SANEADOS}")

# Geração dos arquivos Word (.docx)
def generate_docx_from_md(md_text, docx_path):
    doc = docx.Document()
    
    # Configura margens
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    lines = md_text.split("\n")
    in_table = False
    table_lines = []
    
    def flush_table(lines_t):
        if not lines_t:
            return
        rows_data = []
        for l in lines_t:
            if l.strip().startswith("|") and not re.match(r"^\|\s*:?---", l.strip()):
                parts = [p.strip() for p in l.strip().split("|")[1:-1]]
                if parts:
                    rows_data.append(parts)
        if not rows_data:
            return
        num_cols = max(len(r) for r in rows_data)
        tbl = doc.add_table(rows=len(rows_data), cols=num_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for r_idx, r_data in enumerate(rows_data):
            row = tbl.rows[r_idx]
            is_header = (r_idx == 0)
            for c_idx, cell_value in enumerate(r_data):
                if c_idx < len(row.cells):
                    cell = row.cells[c_idx]
                    clean_val = re.sub(r"<br>", "\n", cell_value)
                    clean_val = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean_val)
                    clean_val = re.sub(r"\*([^*]+)\*", r"\1", clean_val)
                    clean_val = re.sub(r"`([^`]+)`", r"\1", clean_val)
                    cell.text = clean_val
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        run.font.name = "Calibri"
                        run.font.size = Pt(8.5 if not is_header else 9.5)
                        if is_header:
                            run.bold = True
                    if is_header:
                        tcPr = cell._tc.get_or_add_tcPr()
                        shd = OxmlElement('w:shd')
                        shd.set(qn('w:val'), 'clear')
                        shd.set(qn('w:color'), 'auto')
                        shd.set(qn('w:fill'), '1F4E79')
                        tcPr.append(shd)
                        for run in p.runs:
                            run.font.color.rgb = RGBColor(255, 255, 255)
        doc.add_paragraph()

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("|"):
            in_table = True
            table_lines.append(line)
            continue
        else:
            if in_table:
                flush_table(table_lines)
                in_table = False
                table_lines = []
                
        if not stripped:
            continue
            
        if stripped.startswith("# "):
            p = doc.add_paragraph()
            r = p.add_run(stripped[2:])
            r.font.name = "Calibri"
            r.font.size = Pt(16)
            r.bold = True
            r.font.color.rgb = RGBColor(31, 78, 121)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
        elif stripped.startswith("## "):
            p = doc.add_paragraph()
            r = p.add_run(stripped[3:])
            r.font.name = "Calibri"
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = RGBColor(31, 78, 121)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
        elif stripped.startswith("### "):
            p = doc.add_paragraph()
            r = p.add_run(stripped[4:])
            r.font.name = "Calibri"
            r.font.size = Pt(11.5)
            r.bold = True
            r.font.color.rgb = RGBColor(89, 89, 89)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
        elif stripped.startswith("#### "):
            p = doc.add_paragraph()
            r = p.add_run(stripped[5:])
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.bold = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
        elif stripped.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            clean_text = stripped[2:].replace("[!IMPORTANTE]", "[IMPORTANTE]").replace("[!ATENÇÃO]", "[ATENÇÃO]").replace("[!IMPORTANT]", "[IMPORTANTE]").replace("[!WARNING]", "[ATENÇÃO]").replace("[!NOTE]", "[NOTA]")
            clean_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean_text)
            clean_text = re.sub(r"\*([^*]+)\*", r"\1", clean_text)
            r = p.add_run(clean_text)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.italic = True
            r.font.color.rgb = RGBColor(89, 89, 89)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            clean_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", stripped[2:])
            clean_text = re.sub(r"\*([^*]+)\*", r"\1", clean_text)
            clean_text = re.sub(r"`([^`]+)`", r"\1", clean_text)
            r = p.add_run(clean_text)
            r.font.name = "Calibri"
            r.font.size = Pt(10)
        elif re.match(r"^\d+\.\s", stripped):
            p = doc.add_paragraph(style='List Number')
            match = re.match(r"^\d+\.\s+(.*)", stripped)
            item_text = match.group(1) if match else stripped
            clean_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", item_text)
            clean_text = re.sub(r"\*([^*]+)\*", r"\1", clean_text)
            clean_text = re.sub(r"`([^`]+)`", r"\1", clean_text)
            r = p.add_run(clean_text)
            r.font.name = "Calibri"
            r.font.size = Pt(10)
        else:
            p = doc.add_paragraph()
            clean_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", stripped)
            clean_text = re.sub(r"\*([^*]+)\*", r"\1", clean_text)
            clean_text = re.sub(r"`([^`]+)`", r"\1", clean_text)
            r = p.add_run(clean_text)
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)
            
    if in_table:
        flush_table(table_lines)
        
    doc.save(docx_path)
    print(f"[OK] Gravado Word (.docx): {docx_path}")

generate_docx_from_md(text, DEST_DOCX_PARENT)
generate_docx_from_md(text, DEST_DOCX_SANEADOS)

print("Processo concluído com êxito!")
