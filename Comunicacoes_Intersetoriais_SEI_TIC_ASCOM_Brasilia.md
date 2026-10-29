# 📨 Comunicações Intersetoriais — Memorandos e Despachos SEI (Ciclo 2027–2030)

**Órgão:** Procuradoria-Geral do Estado do Maranhão (PGE-MA)  
**Unidade Emitente:** Comissão de Planejamento Estratégico / Assessoria de Planejamento e Gestão Estratégica  
**Finalidade:** Formalização no SEI das demandas transversais e interdependências críticas colhidas nas reuniões de validação dos Planos de Ação 2027–2030 junto à **Governança de TIC / Coordenação do SPA**, **Assessoria de Comunicação (ASCOM)** e **Procuradoria de Brasília (PB) / Subprocuradoria-Geral de Assuntos Jurídicos (SGA)**.

---

## 1. Memorando / Despacho SEI nº 01 — Governança de TIC e Coordenação do SPA

**Destinatários:**
- **Procuradoria-Geral Adjunta para Assuntos Estratégicos (`PGAAE`) / Assessoria em TIC da PGAAE**
- **Núcleo de Inovação (`INOVA`) / Coordenação Técnica do SPA**
- **Supervisão de Informática (`SI`) — Suporte de Infraestrutura Física, Redes e Servidores**
- **C/C:** Corregedoria-Geral da PGE-MA (`CG`), Subprocuradoria-Geral de Assuntos Jurídicos (`SGA`), Procuradoria Judicial (`PJEFP`), Procuradoria da Saúde (`PSAU`) e Procuradoria de Brasília (`PB`)

**Anexos de Referência:**
- `Plano_Acao_Pos_Comparacao_PGAAE.xlsx`
- `Plano_Acao_Pos_Comparacao_INOVA.xlsx`
- `Plano_Acao_Pos_Comparacao_SI.xlsx`
- `Plano_Acao_Pos_Comparacao_CG.xlsx`

### Minuta para Inserção no SEI

> **MEMORANDO / DESPACHO INTERSETORIAL — SANEAMENTO DE GARGALOS CRÍTICOS DO SPA E INTEGRAÇÕES (CICLO 2027–2030)**
>
> **Assunto:** Relato consolidado de vulnerabilidades operacionais do Sistema de Processos Administrativos e Judiciais (`SPA`) apontadas pelas unidades finalísticas e diretrizes de priorização técnica (`E5.O2.KR1`, `E7.O2.KR1`, `E7.O2.KR2`, `E7.O3.KR1` e `E7.O3.KR2`).
>
> 1. **Contextualização:** No curso das reuniões presenciais e remotas de validação dos Planos de Ação Individualizados do Planejamento Estratégico 2027–2030, diversas unidades finalísticas e de controle interno (**Procuradoria Judicial — `PJEFP`**, **Procuradoria da Saúde — `PSAU`**, **Procuradoria de Brasília — `PB`**, **Subprocuradoria-Geral de Assuntos Jurídicos — `SGA`** e **Corregedoria-Geral — `CG`**) reportaram entraves tecnológicos recorrentes no **`SPA`** que impactam diretamente a segurança dos prazos processuais e a fidedignidade das métricas estratégicas do ciclo 2027–2030.
>
> 2. **Gargalos Críticos Reportados pelas Unidades Jurídicas:**
>
>    - **a) Delay de 5 a 7 dias na migração de intimações entre PJe / Portais dos Tribunais Superiores e o SPA (`PJEFP`, `PSAU` e `PB`):** As equipes e chefias da Procuradoria dos Juizados Especiais da Fazenda Pública (Dr. Lucas Leite), Procuradoria da Saúde (corpo de assessoria) e Procuradoria de Brasília (Dr. Ricardo Séllos) relataram defasagem média de **5 (cinco) a 7 (sete) dias** entre a disponibilização real da intimação no `PJe` (ou nos portais do `STF`/`STJ`) e sua efetiva importação e distribuição na caixa do procurador no `SPA`. Nos casos de tutelas de urgência em saúde pública (prazos de 24h a 72h) e recursos nos Tribunais Superiores, esse hiato consome parcela substancial do prazo legal antes mesmo da abertura da tarefa no sistema interno.
>
>    - **b) Instabilidade e indisponibilidade noturna do SPA após as 18h (`PJEFP` e `PSAU`):** Foi reportada lentidão severa e quedas frequentes de conexão do `SPA` no período noturno (especialmente após as 18h), prejudicando o peticionamento em regime de plantão, o cumprimento de liminares urgentes e o fechamento de prazos fatais.
>
>    - **c) Alterações de layout e fluxos de tela no SPA sem aviso prévio ou homologação das chefias (`PJEFP` e `SGA`):** Os procuradores relataram que atualizações de interface e mudanças na disposição de botões/fluxos de trabalho vêm sendo implantadas em produção sem comunicação prévia, manual rápido ou janela de ambientação, gerando risco de erro operacional no protocolo de peças.
>
>    - **d) Falsos positivos de "perda de prazo" no Dashboard Correcional em processos armazenados sem prazo pendente (`Corregedoria-Geral — CG`):** O Corregedor-Geral (Dr. Gustavo Saboia) apontou falha na regra de negócio da integração entre o `SPA` e o painel de monitoramento correcional (`E5.O2.KR1`), na qual processos meramente armazenados ou movimentados para acompanhamento simples (sem intimação com prazo processual aberto) vêm sendo contabilizados indevidamente como pendência ou perda de prazo.
>
> 3. **Deliberações e Providências Incorporadas aos Planos de Ação (`PGAAE / Assessoria em TIC`, `INOVA` e `SI`):** Em resposta a esses apontamentos, foram formalizadas as seguintes ações vinculantes nas planilhas pós-comparação:
>
>    - **À Assessoria em TIC da PGAAE e ao Núcleo de Inovação (`INOVA`):**
>      1. **Força-Tarefa de Sincronização PJe/Portais–SPA (`E7.O3.KR1` / `E7.O3.KR2`):** Priorização da auditoria dos conectores via API/MNI junto ao TJMA, TRFs, STJ e STF para eliminar o delay de 5 a 7 dias na importação de intimações, estabelecendo fila prioritária para mandados de urgência da `PSAU` e intimações de Tribunais Superiores (`PB`).
>      2. **Protocolo de Gestão de Mudanças (Change Management) no SPA (`E7.O3.KR1`):** Instituição de rito obrigatório de homologação prévia junto às chefias setoriais e emissão de comunicado/changelog com antecedência mínima antes da publicação em produção de qualquer alteração de layout ou fluxo de tela no `SPA`.
>      3. **Saneamento da Regra de Negócio do Painel Correcional (`E5.O2.KR1` c/c `CG`):** Ajuste imediato dos filtros de extração do `SPA` para expurgar falsos positivos de perda de prazo em processos armazenados sem prazo pendente de cumprimento.
>
>    - **À Supervisão de Informática (`SI` — Infraestrutura Física e Servidores) em conjunto com a Assessoria em TIC da PGAAE:**
>      1. **Estabilidade de Alta Disponibilidade 24x7 e Monitoramento Noturno (`E7.O2.KR1` e `E7.O2.KR2`):** Revisão das janelas de rotinas pesadas de banco de dados e backup (`Veeam`/`Nutanix`) para horários de madrugada de menor impacto, garantindo estabilidade plena do `SPA` no turno noturno (18h às 23h59).
>
> 4. **Encaminhamento:** Remetam-se os autos à **`PGAAE` (Assessoria em TIC)**, ao **`INOVA`** e à **`SI`** para ciência, abertura de frente técnica conjunta e apresentação de cronograma de mitigação em até **15 (quinze) dias**, dando-se ciência à `CG`, `SGA`, `PJEFP`, `PSAU` e `PB`.

---

## 2. Memorando / Despacho SEI nº 02 — Aproveitamento Institucional de Sustentações Orais no YouTube (`ASCOM` e `SGA/NCIA`)

**Destinatários:**
- **Assessoria de Comunicação (`ASCOM`) — Sra. Ana Paula Bastos Silva**
- **Subprocuradoria-Geral de Assuntos Jurídicos (`SGA`) / Núcleo de Ações Estratégicas (`NCIA`) — Dr. Francisco Beolândio**
- **C/C:** Procuradoria de Brasília (`PB`), Procuradoria Judicial (`PJEFP`) e Escola Superior da Advocacia Pública (`ESAP`)

**Anexos de Referência:**
- `Plano_Acao_Pos_Comparacao_ASCOM.xlsx` (Linha 16 — `E6.O1.KR2`)
- `Plano_Acao_Pos_Comparacao_SGA.xlsx` (`E5.O1.KR2`)

### Minuta para Inserção no SEI

> **MEMORANDO INTERSETORIAL — FLUXO DE APROVEITAMENTO DE SUSTENTAÇÕES ORAIS GRAVADAS NO YOUTUBE DOS TRIBUNAIS (`E6.O1.KR2` E `E5.O1.KR2`)**
>
> **Assunto:** Operacionalização de ação transversal para captação, edição e divulgação institucional de sustentações orais de Procuradores do Estado transmitidas nos canais oficiais do Poder Judiciário no YouTube.
>
> 1. **Origem da Demanda:** Durante a validação do Plano de Ação da **Subprocuradoria-Geral de Assuntos Jurídicos (`SGA` / `NCIA`)**, o Subprocurador-Geral **Dr. Francisco Beolândio** apresentou proposta de sinergia imediata entre a atuação contenciosa estratégica nos Tribunais (`E5.O1.KR2`) e a meta de ampliação do alcance institucional nas redes sociais (`E6.O1.KR2`), consistente no aproveitamento do acervo público de sessões de julgamento transmitidas e gravadas no **YouTube oficial dos Tribunais (TJMA, TRF1, STJ, STF e TST)**.
>
> 2. **Racionalidade e Ganho Institucional:** Atualmente, todas as sustentações orais proferidas por Procuradores do Estado em sessões presenciais ou por videoconferência ficam publicamente arquivadas nos canais do YouTube dos respectivos Tribunais, contendo o registro audiovisual integral da defesa técnica do Estado do Maranhão em causas de alta relevância financeira, patrimonial e social. O aproveitamento desse material:
>    - **Dispensa deslocamento de equipe de filmagem** da ASCOM para sessões judiciais;
>    - **Contorna a escassez de insumos visuais** para alimentação do Instagram, YouTube e portal institucional da PGE-MA;
>    - **Valoriza a atuação técnica dos membros da carreira** e dá transparência ativa à sociedade maranhense sobre a defesa do interesse público (`E6.O1.KR2`);
>    - **Forma acervo pedagógico real** para capacitação de procuradores e residentes jurídicos junto à `ESAP`.
>
> 3. **Fluxo Operacional Homologado nos Planos de Ação (`SGA` e `ASCOM`):**
>    - **Etapa 1 (Comunicação da Sustentação — `SGA`, `PB` e Especializadas):** Sempre que houver realização de sustentação oral relevante perante o TJMA, TRFs ou Tribunais Superiores, o procurador atuante ou a `SGA/PB` encaminhará à `ASCOM` (via canal direto/SEI ou formulário simplificado) o **link da sessão no YouTube do Tribunal**, a **minutagem aproximada (timestamp)** da sustentação, o **número do processo** e uma **síntese de 3 linhas sobre a tese defendida e o impacto para o Estado**.
>    - **Etapa 2 (Recorte, Identidade Visual e Publicação — `ASCOM`):** A `ASCOM` realizará o download do trecho indicado, aplicará a moldura/identidade visual institucional da PGE-MA (com legenda acessível e contextualização em linguagem cidadã) e programará a publicação no Instagram (Reels), YouTube e portal institucional, observadas as restrições de sigilo processual e os períodos de defeso eleitoral.
>
> 4. **Encaminhamento:** Remeta-se o presente despacho à **`ASCOM`** e à **`SGA`**, com cópia à **`PB`**, **`PJEFP`** e **`ESAP`**, para início imediato do fluxo cooperativo já consolidado nas planilhas `Plano_Acao_Pos_Comparacao_ASCOM.xlsx` e `Plano_Acao_Pos_Comparacao_SGA.xlsx`.

---

## 3. Memorando / Despacho SEI nº 03 — Alinhamento da Metodologia de Admissibilidade Recursal e Relatório de Superação de Óbices (`PB` e `SGA`)

**Destinatários:**
- **Procuradoria de Brasília (`PB`) — Dr. Ricardo Séllos (Procurador-Chefe da Procuradoria de Brasília)**
- **Subprocuradoria-Geral de Assuntos Jurídicos (`SGA`) — Dr. Francisco Beolândio**
- **C/C:** Assessoria em TIC da PGAAE / `INOVA` e Procuradorias Especializadas (`PJ`, `PT`, `PCF`, `PRI`, `PRT`, `PSAU`)

**Anexos de Referência:**
- `Plano_Acao_Pos_Comparacao_PB.xlsx` (`E1.O1.KR1`, `E2.O2.KR2` e `E5.O1.KR2`)
- `Plano_Acao_Pos_Comparacao_SGA.xlsx`

### Minuta para Inserção no SEI

> **MEMORANDO INTERSETORIAL — METODOLOGIA CONJUNTA DE MENSURAÇÃO DE ADMISSIBILIDADE RECURSAL E SUPERAÇÃO DE ÓBICES NOS TRIBUNAIS SUPERIORES (`PB` E `SGA`)**
>
> **Assunto:** Padronização da metodologia de aferição da qualidade das peças recursais e instituição do Relatório Semestral de Superação de Óbices Sumulares (Súmulas 7/STJ e 279/STF) sem devolução de processos à origem.
>
> 1. **Contextualização:** Em cumprimento às deliberações consolidadas nas reuniões de validação dos Planos de Ação da **Procuradoria de Brasília (`PB`)** e da **Subprocuradoria-Geral de Assuntos Jurídicos (`SGA`)**, faz-se necessário formalizar o alinhamento metodológico entre ambas as unidades para a execução coordenada das ações estratégicas vinculadas aos indicadores **`E1.O1.KR1`**, **`E2.O2.KR2`** e **`E5.O1.KR2`** no ciclo 2027–2030.
>
> 2. **Diretrizes Operacionais e Metodológicas Homologadas:**
>
>    - **a) Vedação de devolução de processos às Procuradorias de origem e criação do Relatório Semestral de Superação de Óbices:** Conforme deliberação da Procuradoria-Geral Adjunta para Assuntos Estratégicos (Dr. Marcus Bacellar), visando evitar retrabalho e sobrecarga de prazos, a atuação da Procuradoria de Brasília **não envolve a devolução operacional de agravos às Especializadas de origem** após a interposição recursal (sem prejuízo de que a ideia de análise didática de casos concretos seja discutida e amadurecida em oficinas pedagógicas conjuntas com a `ESAP` e a `PGAAJ`). Em substituição, a `PB` elaborará e encaminhará à `SGA` e às chefias das Especializadas, com periodicidade **semestral**, o **Relatório Técnico de Superação de Óbices de Admissibilidade**, mapeando os principais motivos de inadmissão no STJ e STF (especialmente incidência das **Súmulas 7/STJ e 279/STF**, ausência de prequestionamento e deficiência de cotejo analítico) e propondo diretrizes preventivas de redação para os recursos futuros na origem.
>
>    - **b) Alinhamento da metodologia de mensuração da taxa de admissibilidade e êxito recursal (`PB` + `SGA`):** Considerando que o juízo de admissibilidade nos Tribunais Superiores reflete conjuntamente a qualidade da peça interposta na origem (2º grau) e a atuação estratégica de acompanhamento, memoriais e agravos internos em Brasília, a **`PB` e a `SGA`** definirão matriz metodológica conjunta (com apoio de extração de dados da **Assessoria em TIC da PGAAE / `INOVA`** no `SPA`) que:
>      1. Separe estatisticamente as decisões de não conhecimento por óbices formais/sumulares oriundos da instância ordinária daquelas decorrentes de teses de mérito pacificadas em recursos repetitivos ou repercussão geral;
>      2. Mensure o índice de reversão de decisões monocráticas desfavoráveis da Presidência do STJ/STF após atuação específica da `PB` (agravos regimentais/internos, despachos presenciais e memoriais);
>      3. Alimente anualmente a revisão dos enunciados, manuais e modelos de Recursos Especiais e Extraordinários disponibilizados no repositório institucional (`E2.O2.KR2`).
>
> 3. **Encaminhamento:** Remetam-se os autos à **Procuradoria de Brasília (`PB`)** e à **Subprocuradoria-Geral de Assuntos Jurídicos (`SGA`)** para designação de ponto focal conjunto e validação da ficha metodológica do indicador até o início do ciclo de monitoramento, com cópia à **Assessoria em TIC da PGAAE / `INOVA`** para parametrização das etiquetas correspondentes no `SPA`.

