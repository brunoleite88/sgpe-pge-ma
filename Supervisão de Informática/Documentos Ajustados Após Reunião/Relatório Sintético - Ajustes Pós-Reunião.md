# Relatório Sintético de Ajustes Pós-Reunião
**Unidade:** Supervisão de Informática (TIC / PGE-MA)  
**Ciclo Estratégico:** 2026–2030  
**Atas de Referência:** `Reuniao_-_Gestao_de_TI_na_Procuradoria_-_Alinhamento_Profisc.md` e `ata-reuniao-profisco-pge-ma.md`  

---

## 1. Contexto do Alinhamento e Papel Institucional da Supervisão de Informática
A reunião técnica de alinhamento com a gestão da Supervisão de Informática da PGE-MA consolidou o plano de metas do setor para o ciclo 2026–2030, conciliando os projetos financiados pelo BID (PROFISCO III) com as competências reais da equipe e a capacidade operacional da infraestrutura de tecnologia.

A Supervisão de Informática atua como o alicerce operacional da Procuradoria, sendo responsável pela disponibilidade ininterrupta do Data Center, segurança cibernética, conectividade de redes, integridade de backups e sustentação de plataformas essenciais como o Sistema de Processos Administrativos (SPA) e as ferramentas de inteligência artificial institucional.

---

## 2. Diagnóstico Técnico e Diretrizes Críticas Deliberadas
Durante o alinhamento setorial, destacaram-se os seguintes encaminhamentos e decisões estruturantes:
1. **Fronteira entre Infraestrutura e Desenvolvimento:** A equipe interna de TI é altamente especializada e enxuta. A gestão fixou que a competência primária da Informática é assegurar a infraestrutura tecnológica estável, escalável e segura para que os sistemas funcionem, superando a expectativa de desenvolvimento artesanal de soluções sob medida sem governança (*"analogia do Microsoft Word: software empacotado e padronizado"*).
2. **Padrão Redacional Padronizado:** Convencionou-se que as ações da matriz 5W2H vinculadas a automações, IA e sistemas iniciam formalmente com: *"Garantir a infraestrutura necessária para..."* ou *"Dar suporte e condições de infraestrutura para que [a solução] seja executada"*.
3. **Gargalo Crítico de Capacitação (Nutanix HCI e Veeam Backup):** A PGE possui infraestrutura de ponta de grande porte (Hiperconvergência Nutanix HCI) e a suíte global Veeam Backup & Replication. Contudo, a capacitação prometida no Profisco original nunca foi fornecida, forçando a equipe a operar de modo autodidata. Pactuou-se como prioridade máxima a inclusão de treinamentos oficiais e certificados com recursos do PROFISCO III.
4. **Soberania Tecnológica do Data Center da PGE vs. ATI:** Deliberou-se pela recusa técnica categórica ao pedido da Agência Estadual de TIC (ATI) para hospedar o sistema SEI Estadual nos servidores da PGE. A recusa baseou-se em 4 riscos inaceitáveis: efeito irreversível (*"Bolsa Família"*), sufocamento da expansão interna da PGE, degradação de CPU e RAM no sistema SPA e assimetria injusta de responsabilidade sobre a equipe enxuta da PGE.
5. **Conectividade e Ponto Único de Falha na ATI:** Apesar de contar com duas fibras ópticas dedicadas, todo o tráfego da PGE afunila em um único túnel de internet na ATI, gerando instabilidades e oscilações diárias externas (manutenções da ATI entre 9h30 e 10h), alheias ao controle da PGE.
6. **Inviabilidade de Convênios com Bolsistas:** A experiência prática comprovou a ineficácia de atrair estagiários/bolsistas para desenvolvimento contínuo devido ao alto *turnover* (evasão em 30 dias frente ao mercado privado), devendo a PGE priorizar a aquisição de softwares consolidados ou contratos com fábricas de software especializadas.

---

## 3. Quadro Comparativo de Metas (Antes vs. Depois da Reunião)

| Meta Preliminar (Antes) | Status Pós-Reunião | Redação Oficial Ajustada (Lista Mestre) | Fundamentação do Ajuste |
| :--- | :--- | :--- | :--- |
| **Eixo 7 / Obj 2 / KR2:** 100% de recuperação de dados com novo sistema de backup até 2028 | **MANTIDA E FORTALECIDA** | **Assegurar 100% de capacidade de recuperação de dados processuais em contingências até 2028** | Foco na operação da suíte Veeam Backup, testes semestrais de Disaster Recovery e capacitação oficial da equipe em HCI Nutanix. |
| **Eixo 7 / Obj 2 / KR1:** Substituir 100% dos equipamentos defasados até 2027 | **MANTIDA E RASTREADA** | **Substituir 100% dos equipamentos de TI obsoletos até 2027** | Inventário de 29 computadores obsoletos mapeados pela TI, aquisições por recursos próprios finalizadas e complementação via PROFISCO III. |
| **Eixo 7 / Obj 4 / KR1:** Executar 100% do Plano Diretor de TIC até 2030 | **MANTIDA** | **Executar 100% do Plano Diretor de Tecnologia da Informação e Comunicação até 2030** | Consolidação de governança corporativa, investimentos plurianuais e políticas de segurança da informação. |
| **Eixo 7 / Obj 1 / KR2:** Automatizar 30% dos pareceres padronizados com modelos de IA até 2028 | **MANTIDA COM PAPEL DE INFRA** | **Automatizar 30% da elaboração de pareceres padronizados com inteligência artificial até 2028** | Papel da TI delimitado em garantir o ambiente tecnológico, servidores, APIs seguras e busca semântica para os modelos assistidos. |
| **Eixo 7 / Obj 1 / KRs 1 e 3:** Implementar ao menos 2 soluções de IA e 1 ferramenta de pesquisa jurídica | **UNIFICADAS EM PROJETOS DE INOVAÇÃO** | **Implementar 5 projetos estratégicos de inovação e modernização voltados a desafios até 2030** | Unificação metodológica na carteira de projetos de IA (Minuta IA, robôs RPA e plataformas de pesquisa jurídica inteligente). |
| **Eixo 7 / Obj 3 / KRs 2 e 3:** Capacitar 25% em IA e certificar 25% dos servidores até 2029 | **MANTIDAS E DIRECIONADAS** | **Capacitar 25% do corpo funcional (2027) e certificar 25% dos técnicos de TI em competências digitais (2029)** | Trilhas funcionais com ESAP e certificações oficiais obrigatórias para os técnicos de TI em HCI, Veeam e segurança. |
| **Eixo 3 / Obj 1 / KR3:** Executar 100% dos projetos e recursos do PROFISCO III previstos para a PGE até 2030 | **COEXECUÇÃO TÉCNICA** | **Executar 100% dos projetos e recursos do PROFISCO III previstos para a PGE até 2030** | Supervisão e governança técnica sobre os ETPs, TRs e marcos de entrega de hardware, software e consultoria BID de TIC. |

---

## 4. Síntese do Plano de Ação 5W2H Ajustado

| Ação (O Quê) | Subação e Recursos (Como) | Responsáveis (Quem) | Prazo (Quando) |
| :--- | :--- | :--- | :--- |
| **Garantir infraestrutura de backup Veeam e contingência** | Projetar e manter rotinas de cópia automatizada em ambiente secundário com Veeam Backup para proteção do SPA e bases da PGE. | Líder: TI; Coexecutores: SGA | 90 dias / Contínuo |
| **Capacitação oficial em Nutanix HCI e Veeam Backup** | Incluir no PROFISCO e realizar treinamento oficial/certificado em Hiperconvergência e Veeam para sanar a operação autodidata. | Líder: TI; Coexecutores: SGA, PROFISCO III | 180 dias |
| **Calendário semestral de testes práticos de contingência** | Realizar simulações de Disaster Recovery auditando a recuperação do SPA e medindo tempo (RTO) e perda de dados (RPO). | Líder: TI; Coexecutores: SGA | Semestral |
| **Executar plano plurianual de renovação do parque de TI** | Substituir 100% das estações obsoletas (29 computadores mapeados) via recursos ordinários e PROFISCO III até 2027. | Líder: TI; Coexecutores: SGA (UGAM e USF) | Até 2027 |
| **Gerenciar e executar ações do Plano Diretor de TIC** | Executar cronograma anual de investimentos, conectividade e políticas de segurança da informação do PDTIC. | Líder: TI; Coexecutores: SGA | Até 2030 (anual) |
| **Ambiente tecnológico seguro para IA em pareceres (30%)** | Garantir servidores, APIs seguras e busca semântica para modelos assistidos de pareceres e minutas das consultivas. | Líder: TI; Coexecutores: Consultivas, SGA | 180 dias / Contínuo |
| **Infraestrutura para 5 projetos de inovação da PGE** | Viabilizar ambiente e sustentação técnica para Minuta IA, robôs RPA, pesquisa inteligente e modernização do SPA. | Líder: TI; Coexecutores: ESAP, PGAAE, Gabinete | Até 2030 (cronograma BID) |
| **Certificação técnica oficial dos servidores de TIC (25%)** | Inscrever a equipe de TI em certificações oficiais reconhecidas em Nutanix, Veeam, redes/firewall e governança ITIL. | Líder: TI; Coexecutores: ESAP, SGA | Até 2029 |
| **Apoiar capacitação funcional em Direito Digital e IA** | Disponibilizar laboratórios e apoio técnico para formações continuadas da ESAP/EGMA em IA e processo eletrônico. | Coexecutores: ESAP, TI, SGA | Semestral até 2027 |
| **Governança técnica na carteira de TIC do PROFISCO III** | Acompanhar ETPs, TRs e marcos de entrega de hardware, software e consultorias especializadas de TIC financiadas pelo BID. | Líder: TI; Coexecutores: SGA, USF, PGAAE | Contínuo até 2030 |
| **Sustentação e infraestrutura para robôs de automação RPA** | Manter operacionais e integrados aos sistemas PJe/SPA os robôs RPA Distribuição, Monitor PGE, RPV, Honorários e Dativos. | Líder: TI; Coexecutores: Especializadas, SGA | Contínuo até 2029 |
| **Soberania do Data Center e governança de chamados** | Preservar integridade/memória dos servidores Nutanix da PGE (vedando SEI da ATI) e instituir fluxo formal de chamados ('analogia do Word'). | Líder: TI; Instância Decisória: Gabinete PGE | Imediato / Permanente |

---

## 5. Despacho Padrão de Encerramento e Encaminhamento (SEI)

```text
DESPACHO / MEMORANDO DE ENCERRAMENTO

PROCESSO SEI: Planejamento Estratégico Institucional PGE-MA (2026–2030)
DE: Supervisão de Informática (TIC)
PARA: Subprocuradoria-Geral Adjunta / Assessoria de Planejamento e Gestão Estratégica

Senhor Subprocurador-Geral Adjunto,

1. Em cumprimento às diretrizes do Planejamento Estratégico PGE 2030 e após alinhamentos técnicos com a equipe de facilitação, submeto a Vossa Excelência os documentos saneados e ajustados da Supervisão de Informática:
   a) Documento de Eixos, Objetivos e Metas (KRs), harmonizado com a Lista Mestre Oficial, estruturado no Eixo 7 (modernização de 100% dos equipamentos de TI até 2027, 100% de recuperação de dados via Veeam Backup até 2028, execução do PDTIC, IA para pareceres e certificação da equipe) e coexecuções estratégicas no PROFISCO III (Eixo 3) e robôs RPA (Eixo 5);
   b) Matriz 5W2H do Plano de Ação em formato .xlsx, adotando o padrão redacional de garantia de infraestrutura necessária e incorporando o pleito imperativo de capacitação oficial em Nutanix HCI e Veeam Backup;
   c) Consolidação das diretrizes de preservação da soberania do Data Center da PGE frente à ATI e padronização rígida de fluxos e chamados de TIC para sustentabilidade institucional.

2. Ante o exposto, submeto o presente caderno ajustado para homologação superior e publicação institucional no âmbito do Planejamento Estratégico da PGE-MA.

São Luís (MA), data da assinatura eletrônica.

Gestão da Supervisão de Informática
Procuradoria-Geral do Estado do Maranhão
```
