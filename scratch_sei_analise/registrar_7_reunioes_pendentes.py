from pathlib import Path

base = Path(r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados")

# 1. Update Kit_Despachos_SEI_e_Mensagens_WhatsApp.md
kit_path = base / "Kit_Despachos_SEI_e_Mensagens_WhatsApp.md"
kit_text = kit_path.read_text(encoding="utf-8")
start_marker = "## 3. Bloco II"
end_marker = "## 4. Bloco III"
s_idx = kit_text.find(start_marker)
e_idx = kit_text.find(end_marker)
assert s_idx != -1 and e_idx != -1

new_sec3 = """## 3. Bloco II — 7 Unidades com Reunião de Alinhamento Pendente com as Chefias (`PGAAE`, `PGA`, `PERJP`, `PDA`, `PCF`, `PA`, `PT`) + Regionais (`PRI`, `PRT`)

> [!IMPORTANT]
> **Marco Crítico para Conclusão da Etapa:**
> Embora as planilhas pós-comparação das unidades abaixo já estejam 100% saneadas, formatadas no padrão de 7 colunas da Lista Mestre Canônica e adequadas aos **3 Ps (Prazo, Presença nos Tribunais e Padronização)**, **ainda restam 7 reuniões de alinhamento com chefias pendentes de realização (`PGAAE`, `PGA`, `PERJP`, `PDA`, `PCF`, `PA` e `PT`)**, cuja condução é essencial para a conclusão formal desta etapa.
> As planilhas abaixo funcionam como **proposta-base saneada para deliberação nas respectivas reuniões**:

### 3.1. Quadro das 7 Reuniões Pendentes com Chefias (Indispensáveis para Fechamento da Etapa)

| Unidade (Reunião Pendente) | Planilha-Base Saneada para a Reunião | Pauta Técnica e Pontos Focais para Deliberação com a Chefia |
| :--- | :--- | :--- |
| **1. PGAAE (Assuntos Estratégicos)**<br>*(Dr. Marcus Bacellar)* | [Plano_Acao_Pos_Comparacao_PGAAE.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PGAAE.xlsx) | Governança macro do Planejamento (`E5.O5.KR1`), coordenação dos 10 artefatos BID/Profisco (`E3.O1.KR3`), titularidade da `Assessoria em TIC da PGAAE / INOVA` em sistemas/BI/IA e Extranet do Fórum José Sarney (`E9.O1.KR2`). |
| **2. PGA (Assuntos Administrativos)** | [Plano_Acao_Pos_Comparacao_PGA.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PGA.xlsx) | Coordenação executiva da eficiência administrativa (Eixo 2), execução orçamentária/FUNPGE e captação externa com articulação da `PGARI` (Eixo 3), sustentabilidade (Eixo 8) e obras/reformas (Eixo 9). |
| **3. Proc. de Execuções e Pagamentos (PERJP)** | [Plano_Acao_Pos_Comparacao_PERJP.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PERJP.xlsx) | Recuperação de créditos/depósitos (`E1.O1.KR1`), redução de 90% em bloqueios/duplicidades de RPVs com Núcleo de Cálculos (`E1.O1.KR2`), acordos em precatórios, regra `D-3` no art. 535 CPC (`E5.O6.KR1`) e admissibilidade recursal (`E5.O2.KR2`). |
| **4. Procuradoria da Dívida Ativa (PDA)** | [Plano_Acao_Pos_Comparacao_PDA.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PDA.xlsx) | Fusão integral com o `NIRF` (Despacho SEI nº 50/2026), metas de arrecadação/rating/protesto/transação (`E1.O2.KR1` a `KR7`), grandes devedores, admissibilidade recursal, fluxo `ASCOM` e PAC/`ESAP` (`E9.O2.KR1`). |
| **5. Procuradoria do Contencioso Fiscal (PCF)** | [Plano_Acao_Pos_Comparacao_PCF.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PCF.xlsx) | Plantão 24h–48h tutelas fiscais, grandes litígios (ICMS/DIFAL), conversão de depósitos em renda (`E1.O1.KR1`), admissibilidade STF/STJ com Brasília (`E5.O2.KR2`), fluxo `ASCOM` e PAC/`ESAP` (`E9.O2.KR1`). |
| **6. Procuradoria Administrativa (PA)** | [Plano_Acao_Pos_Comparacao_PA.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PA.xlsx) | Protocolo Prazo Zero Perdido (`E5.O6.KR1`), SLA consultivo (`E4.O1.KR1`), admissibilidade recursal (`E5.O2.KR2`), modelos Lei 14.133/21, fluxo `ASCOM`, honorários (`E9.O3.KR1`) e PAC/`ESAP`. |
| **7. Procuradoria Trabalhista (PT)** | [Plano_Acao_Pos_Comparacao_PT.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PT.xlsx) | Regra `D-3` PJe-JT/TRT16 (`E5.O6.KR1`), Recursos de Revista ao TST (`E5.O2.KR2`), Tema 246/STF, fluxo `ASCOM` (`E6.O1.KR2`), honorários (`E9.O3.KR1`) e PAC/`ESAP` (`E9.O2.KR1`). |

- **Mensagem WhatsApp de Convite / Agendamento das 7 Reuniões Pendentes (`PGAAE`, `PGA`, `PERJP`, `PDA`, `PCF`, `PA`, `PT`):**
  ```text
  Olá, Doutor(a)! Tudo bem?
  Para avançarmos na conclusão da etapa de pactuação setorial do Planejamento Estratégico 2027–2030 da PGE-MA, nossa equipe já preparou a proposta-base saneada da planilha da sua unidade (Plano_Acao_Pos_Comparacao_[SIGLA].xlsx, em anexo), eliminando metas sem governabilidade direta e estruturando as ações na Lista Mestre Canônica e nos 3 Ps (Prazo, Presença nos Tribunais e Padronização).
  Gostaríamos de agendar nossa breve reunião de alinhamento para validar os pontos-chave com Vossa Excelência e colher eventuais ajustes antes da juntada final no SEI. Qual o melhor dia e horário nesta semana?
  ```

### 3.2. Procuradorias Regionais (`PRI` e `PRT`) e Despacho SEI Pós-Alinhamento

| Unidade Regional | Linhas Saneadas | Arquivo Pronto para Anexação no SEI | Destaques Técnicos da Planilha Saneada |
| :--- | :---: | :--- | :--- |
| **Procuradoria Regional de Imperatriz (PRI)** | 54 ações | [Plano_Acao_Pos_Comparacao_PRI.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PRI.xlsx) | Superada planilha genérica; rotina `D-3` nas comarcas do polo, subida de recursos à Capital, bancos de peças, honorários (`E9.O3.KR1`) e PAC/ESAP (`E9.O2.KR1`). |
| **Procuradoria Regional de Timon (PRT)** | 54 ações | [Plano_Acao_Pos_Comparacao_PRT.xlsx](file:///c:/Users/brunogomes/Documents/Planejamento%20Estratégico/Planos%20de%20Ação%20Individualizados/Planos%20de%20Ação%20Saneados/Planilhas_Pos_Comparacao_Consolidadas/Plano_Acao_Pos_Comparacao_PRT.xlsx) | Superada planilha genérica; rotina `D-3` nas comarcas do polo, subida de recursos à Capital, bancos de peças, honorários (`E9.O3.KR1`) e PAC/ESAP (`E9.O2.KR1`). |

- **Despacho SEI Padrão (Para envio após a realização da reunião de alinhamento com `PGAAE`, `PGA`, `PERJP`, `PDA`, `PCF`, `PA`, `PT` ou validação de `PRI`/`PRT`):**
  ```text
  Ao(À) Procurador(a)-Geral Adjunto(a) / Procurador(a)-Chefe / Procurador(a) Regional,
  No âmbito da consolidação do Planejamento Estratégico 2027–2030 da PGE-MA, e em conformidade com o alinhamento técnico realizado com a chefia desta unidade, a Assessoria de Planejamento e Gestão Estratégica acosta aos presentes autos a versão consolidada e saneada do Plano de Ação Setorial (Plano_Acao_Pos_Comparacao_[SIGLA].xlsx).
  O documento contempla a estruturação oficial de 7 colunas da Lista Mestre Canônica, a cobertura dos 3 pilares finalísticos (Controle de Prazos, Presença nos Tribunais e Padronização/IA) e a delimitação estrita às competências de governabilidade da unidade.
  Solicita-se a conferência e o lançamento de despacho simplificado de validação ("Com reunião de alinhamento e planilha saneada anexada aos autos, valido os dados e o Plano de Ação desta unidade para o ciclo 2027–2030"), restituindo-se o processo a esta Assessoria.
  ```

---

"""
kit_path.write_text(kit_text[:s_idx] + new_sec3 + kit_text[e_idx:], encoding="utf-8")

# 2. Update Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md
p3_path = base / "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md"
p3_text = p3_path.read_text(encoding="utf-8")
p3_text = p3_text.replace(
    "**Bloco B — 7 Procuradorias Especializadas e Regionais que AINDA NÃO RESPONDERAM NEM ENCAMINHARAM MANIFESTAÇÃO NO SEI:** `Procuradoria Trabalhista (PT)`, `Procuradoria Administrativa (PA)`, `Procuradoria da Dívida Ativa (PDA)`, `Procuradoria do Contencioso Fiscal (PCF)`, `Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP)`, `Procuradoria Regional de Imperatriz (PRI)` e `Procuradoria Regional de Timon (PRT)`.",
    "**Bloco B — 5 Procuradorias Especializadas com Reunião de Chefia Pendente (`PT`, `PA`, `PDA`, `PCF`, `PERJP`) + 2 Procuradorias Regionais Pendentes de Validação SEI (`PRI`, `PRT`):** `Procuradoria Trabalhista (PT)`, `Procuradoria Administrativa (PA)`, `Procuradoria da Dívida Ativa (PDA)`, `Procuradoria do Contencioso Fiscal (PCF)` e `Procuradoria de Execuções e Requisições Judiciais de Pagamento (PERJP)` **(cujas reuniões de alinhamento com as respectivas chefias ainda estão pendentes de realização e são essenciais para a conclusão desta etapa)**, além da `Procuradoria Regional de Imperatriz (PRI)` e `Procuradoria Regional de Timon (PRT)`."
).replace(
    "**Órgãos de Cúpula Coordenadora PENDENTES DE CONSOLIDAÇÃO NO SEI:** `Procurador-Geral Adjunto (PGA)` e `Procuradora-Geral Adjunta para Assuntos Estratégicos (PGAAE)` *(exercem coordenação superior e normatização, atuando na homologação do caderno macro)*.",
    "**Órgãos de Cúpula Coordenadora com Reunião de Alinhamento e Consolidação Pendente (`PGAAE` e `PGA`):** `Procuradoria-Geral Adjunta para Assuntos Estratégicos (PGAAE)` e `Procuradoria-Geral Adjunta para Assuntos Administrativos (PGA)`, cujas reuniões de alinhamento e fechamento compõem, junto com `PERJP`, `PDA`, `PCF`, `PA` e `PT`, o **bloco de 7 reuniões pendentes e essenciais para a conclusão desta etapa**."
)
p3_path.write_text(p3_text, encoding="utf-8")

# 3. Update Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md
cot_path = base / "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md"
cot_text = cot_path.read_text(encoding="utf-8")
target_cot = "* **Assessoria em TIC da PGAAE + Laboratório INOVA:** Liderança indelegável no **Objetivo 1 (Ferramentas de Inteligência Artificial e automação de pareceres)** e no **Objetivo 3 (Projetos estratégicos de inovação prática, LegalTech e design de processos)**, atuando a SI como coexecutora estritamente para suporte de infraestrutura física/hospedagem."
replacement_cot = (
    target_cot
    + "\n>\n> **Status de Pactuação com Chefias (7 Reuniões Pendentes para Conclusão da Etapa):**\n> * Todas as 41 planilhas setoriais (`Plano_Acao_Pos_Comparacao_*.xlsx`) encontram-se tecnicamente saneadas e sincronizadas com esta Matriz.\n> * Registra-se que **ainda restam 7 reuniões de alinhamento com chefias pendentes de realização**, essenciais para a conclusão formal desta etapa: **`PGAAE`**, **`PGA`**, **`PERJP` (Execuções)**, **`PDA` (Dívida Ativa)**, **`PCF` (Contencioso Fiscal)**, **`PA` (Administrativa)** e **`PT` (Trabalhista)**, nas quais as respectivas planilhas pós-comparação servirão como proposta-base para deliberação e homologação final."
)
if "Status de Pactuação com Chefias (7 Reuniões Pendentes" not in cot_text:
    cot_path.write_text(cot_text.replace(target_cot, replacement_cot, 1), encoding="utf-8")

print("OK: Todos os arquivos .md atualizados com o registro das 7 reunioes pendentes.")

