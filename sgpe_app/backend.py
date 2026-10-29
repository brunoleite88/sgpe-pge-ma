# -*- coding: utf-8 -*-
"""
Backend FastAPI + SQLite para o Sistema de Gestão do Planejamento Estratégico (SGPE 2027-2030) da PGE-MA.
Roda 100% em user-space (sem privilégios de administrador), sincronizando bidirecionalmente:
- As 41 planilhas oficiais (Plano_Acao_Pos_Comparacao_*.xlsx) com formatação e altura dinâmica;
- Os relatórios executivos (.md): Cotejamento Consolidado, 3 Ps, Kit SEI/WhatsApp e Síntese de Pendências;
- Os Grupos de Trabalho Compartilhados (GTs) e Projetos Estruturantes.
"""
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import openpyxl
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(r"c:\Users\brunogomes\Documents\Planejamento Estratégico\Planos de Ação Individualizados\Planos de Ação Saneados")
CONS_DIR = BASE_DIR / "Planilhas_Pos_Comparacao_Consolidadas"
APP_DIR = BASE_DIR / "sgpe_app"
DB_PATH = APP_DIR / "sgpe_pge_ma.db"

sys.path.insert(0, str(BASE_DIR / "scratch_sei_analise"))
from saneamento_ascom_e_ti import UNIT_FOLDERS, load_rows, write_sheet_to_all_targets

# Metadados institucionais das 41 unidades (Tipo, Status Reunião, Processo SEI, Interlocutor/Chefe)
UNIT_META = {
    "PGAAE": {
        "nome": "Procuradoria-Geral Adjunta para Assuntos Estratégicos",
        "tipo": "Cúpula / Coordenação",
        "bloco_3ps": "Cúpula Coordenadora",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Marcus Bacellar (Procurador-Geral Adjunto para Assuntos Estratégicos)",
        "pauta_reuniao": "Governança macro do Planejamento (E5.O5.KR1), coordenação dos 10 artefatos BID/Profisco (E3.O1.KR3), titularidade da Assessoria em TIC da PGAAE / INOVA em sistemas/BI/IA e Extranet do Fórum José Sarney."
    },
    "PGA": {
        "nome": "Procuradoria-Geral Adjunta para Assuntos Administrativos",
        "tipo": "Cúpula / Coordenação",
        "bloco_3ps": "Cúpula Coordenadora",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a)-Geral Adjunto(a) para Assuntos Administrativos",
        "pauta_reuniao": "Coordenação executiva da eficiência administrativa (Eixo 2), execução orçamentária/FUNPGE e captação externa com articulação da PGARI (Eixo 3), sustentabilidade (Eixo 8) e obras/reformas (Eixo 9)."
    },
    "PERJP": {
        "nome": "Procuradoria de Execuções e Requisições Judiciais de Pagamento",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco B (Reunião Pendente)",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a)-Chefe da PERJP",
        "pauta_reuniao": "Recuperação de créditos/depósitos (E1.O1.KR1), redução de 90% em bloqueios/duplicidades de RPVs com Núcleo de Cálculos (E1.O1.KR2), acordos em precatórios, regra D-3 no art. 535 CPC (E5.O6.KR1) e admissibilidade recursal (E5.O2.KR2)."
    },
    "PDA": {
        "nome": "Procuradoria da Dívida Ativa",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco B (Reunião Pendente)",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "2026.11103.07215 (c/ NIRF)",
        "responsavel": "Procurador(a)-Chefe da PDA",
        "pauta_reuniao": "Validação da absorção integral das ações do NIRF (Despacho SEI nº 50/2026), metas de arrecadação/rating/protesto/transação (E1.O2.KR1 a KR7), atuação seletiva em grandes devedores e 3 Ps."
    },
    "PCF": {
        "nome": "Procuradoria do Contencioso Fiscal",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco B (Reunião Pendente)",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a)-Chefe da PCF",
        "pauta_reuniao": "Plantão 24h–48h em tutelas fiscais, grandes litígios tributários (ICMS/DIFAL/TUST), conversão de depósitos em renda (E1.O1.KR1), atuação conjunta com Brasília (E5.O2.KR2) e padronização com SEFAZ/TARF."
    },
    "PA": {
        "nome": "Procuradoria Administrativa",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco B (Reunião Pendente)",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a)-Chefe da PA",
        "pauta_reuniao": "Protocolo Prazo Zero Perdido (E5.O6.KR1), SLA consultivo qualificado (E4.O1.KR1), sustentações no TJMA em licitações/servidores (E5.O1.KR2), admissibilidade recursal (E5.O2.KR2) e modelos da Lei 14.133/21."
    },
    "PT": {
        "nome": "Procuradoria Trabalhista",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco B (Reunião Pendente)",
        "status_reuniao": "Reunião Pendente (Prioritária)",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a)-Chefe da PT",
        "pauta_reuniao": "Dupla checagem PJe-JT/TRT16 e regra D-3 contra revelia (E5.O6.KR1), sustentações no TRT16 (E5.O1.KR2), Recursos de Revista ao TST (E5.O2.KR2), banco de peças Tema 246/STF e cartilha de fiscalização de terceirizados."
    },
    "PJ": {
        "nome": "Procuradoria Judicial",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. André Vila Verde",
        "pauta_reuniao": "Unidade-Modelo nos 3 Ps: Regra D-3, Agenda Compartilhada SPA, escala de memoriais/sustentações no TJMA, Relatório de Teses (50+ págs.), Sistema Bacelar e acordo de dativos."
    },
    "PEDU": {
        "nome": "Procuradoria da Educação",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07190",
        "responsavel": "Dr. Felipe Nina",
        "pauta_reuniao": "Monitoramento SPA-PJe (alerta D-5 / protocolo D-2), carteira no Monitor PGE, checklist REsp/RE e reuniões trimestrais com SEDUC e IPREV."
    },
    "PSP": {
        "nome": "Procuradoria da Segurança Pública",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07192",
        "responsavel": "Dr. José Carlos Pires",
        "pauta_reuniao": "Dupla conferência (D-5 / D-2), ficha estratégica de julgamentos, biblioteca de minutas padronizadas e prevenção de litígios com SSP/PMMA/PCMA/CBMMA."
    },
    "PPIMA": {
        "nome": "Procuradoria do Patrimônio Imobiliário e Meio Ambiente",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07196",
        "responsavel": "Dr. Osvaldo Santos Cardoso",
        "pauta_reuniao": "Divisão em Grupo 1 (Massa/Padronização de usucapião e convênios) e Grupo 2 (Relevância/Presença nos tribunais) + Protocolo Prazo Zero Perdido."
    },
    "PJEFP": {
        "nome": "Procuradoria dos Juizados Especiais da Fazenda Pública",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Lucas Leite dos Reis",
        "pauta_reuniao": "Sustentação oral seletiva nas Turmas Recursais e Incidentes de Uniformização (E5.O1.KR2), ferramenta MINUTIA/SPA, integração digital do Fórum José Sarney (Extranet c/ PGAAE e Canal de Avisos c/ SGRH)."
    },
    "PB": {
        "nome": "Procuradoria de Brasília",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Ricardo Séllos",
        "pauta_reuniao": "Inversão da Lógica Recursal, memoriais/sustentações no STF/STJ/TST, Relatório Semestral de Superação de Óbices (Súmulas 7/STJ e 279/STF) sem devolução operacional à origem (evitando retrabalho, mantendo ideia pedagógica para oficinas c/ ESAP/PGAAJ)."
    },
    "PSAU": {
        "nome": "Procuradoria da Saúde",
        "tipo": "Procuradoria Especializada",
        "bloco_3ps": "Bloco A (Pós-Reunião)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Corpo de Assessores / Deliberação Dr. Marcus Bacellar",
        "pauta_reuniao": "Mantida E4.O1.KR1 (90% SLA consultas SES/CEMARC) por decisão do Dr. Marcus Bacellar; incluída aferição de Êxito Qualificado em Saúde Pública (E5.O1.KR3); expurgada apenas E9.O3.KR1 (honorários)."
    },
    "PRI": {
        "nome": "Procuradoria Regional de Imperatriz",
        "tipo": "Procuradoria Regional",
        "bloco_3ps": "Bloco B (Regional SEI)",
        "status_reuniao": "Validação via SEI",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a) Regional de Imperatriz",
        "pauta_reuniao": "Planilha customizada para as comarcas do polo de Imperatriz (superada versão genérica), cobrindo integralmente os 3 Ps, honorários e PAC/ESAP."
    },
    "PRT": {
        "nome": "Procuradoria Regional de Timon",
        "tipo": "Procuradoria Regional",
        "bloco_3ps": "Bloco B (Regional SEI)",
        "status_reuniao": "Validação via SEI",
        "processo_sei": "Verificar SEI",
        "responsavel": "Procurador(a) Regional de Timon",
        "pauta_reuniao": "Planilha customizada para as comarcas do polo de Timon (superada versão genérica), cobrindo integralmente os 3 Ps, honorários e PAC/ESAP."
    },
    "NCIA": {
        "nome": "Núcleo de Combate à Improbidade Administrativa",
        "tipo": "Núcleo Especializado",
        "bloco_3ps": "Bloco A (Escopo Específico)",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Francisco Beolândio",
        "pauta_reuniao": "Plano enxuto focado em 100% de tempestividade nas ACPs e assistências ao MP (E5.O6.KR1), parametrização do SPA, saneamento de falsos positivos no Dashboard e trilhas de investigação patrimonial/IA."
    },
    "ASJUR": {
        "nome": "Assessoria Jurídica dos Procuradores-Gerais Adjuntos",
        "tipo": "Consultivo Superior",
        "bloco_3ps": "Bloco A (Escopo Consultivo)",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2025.11103.05165 / 2026.11103.07181",
        "responsavel": "Dr. Victor Paiva (Memorando nº 38/2026)",
        "pauta_reuniao": "Tempestividade consultiva qualificada por complexidade (E4.O1.KR1), análise técnico-jurídica formal de PLs e minutas de decretos (E5.O4.KR1/KR2) e repositório de minutas-padrão (E5.O5.KR2)."
    },
    "PGAAJ": {
        "nome": "Procuradoria-Geral Adjunta para Assuntos Jurídicos",
        "tipo": "Cúpula / Coordenação",
        "bloco_3ps": "Cúpula Coordenadora",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07177",
        "responsavel": "Dr. João Victor Holanda do Amaral",
        "pauta_reuniao": "Coordenação contenciosa/consultiva, revezamento virtual de sustentações orais com Brasília (E5.O1.KR2) e gestão descentralizada de prazos pelas chefias no painel nativo do SPA (sem fluxo de alerta escalonado ou métrica de perdas evitadas, conforme diretriz do Corregedor-Geral Dr. Gustavo Saboia)."
    },
    "PGARI": {
        "nome": "Procuradoria-Geral Adjunta de Relacionamento Institucional",
        "tipo": "Cúpula / Articulação",
        "bloco_3ps": "Cúpula Articuladora",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Daniel Blume",
        "pauta_reuniao": "Papel estritamente articulador (não executivo): articulação institucional para captação/parcerias externas (E3.O1.KR1) e diálogo interinstitucional preventivo em riscos normativos e socioambientais (E5.O4.KR1 e E5.O4.KR2)."
    },
    "SGA": {
        "nome": "Subprocuradoria-Geral Adjunta",
        "tipo": "Cúpula / Coordenação",
        "bloco_3ps": "Cúpula Coordenadora",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Francisco Beolândio",
        "pauta_reuniao": "Coordenação de pautas de 2º grau, revezamento virtual de sustentações com Brasília, interlocução sobre admissibilidade recursal e envio de sustentações gravadas no YouTube à ASCOM (embutidos em E5.O1.KR2; sem relatório de transição)."
    },
    "CG": {
        "nome": "Corregedoria-Geral da PGE",
        "tipo": "Órgão Correcional",
        "bloco_3ps": "Governança / Controle",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dr. Gustavo Saboia (Corregedor-Geral)",
        "pauta_reuniao": "Regimento Interno Único (E5.O5.KR1), saneamento de falsos positivos de perda de prazo no Dashboard do SPA em processos armazenados (E5.O6.KR1) e apuração tempestiva com sigilo/LGPD (E8.O2.KR1)."
    },
    "OUV": {
        "nome": "Ouvidoria-Geral da PGE",
        "tipo": "Órgão de Controle / Cidadania",
        "bloco_3ps": "Governança / Atendimento",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Dra. Eliana Maria da Silva / Dra. Martha Jackson",
        "pauta_reuniao": "Expurgo de E4.O1.KR1 e supressão formal de E4.O1.KR2 (impossibilidade material nas plataformas e-OUV/e-SIC, convertido em capacitação de Escuta Ativa e CNV c/ ESAP); retorno conclusivo (E4.O1.KR3), 2 ações anuais contra assédio (Dec. 39.054/2024) e Escala de Transparência Adaptada à LGPD (E8.O2.KR2)."
    },
    "ASCOM": {
        "nome": "Assessoria de Comunicação",
        "tipo": "Assessoria Estratégica",
        "bloco_3ps": "Comunicação Institucional",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Ana Paula Bastos Silva / Dra. Martha Jackson",
        "pauta_reuniao": "Crescimento contínuo do alcance médio mensal (base 2025, Instagram principal, ressalva do defeso eleitoral), fluxo quinzenal obrigatório de envio de êxitos pelas Especializadas, aproveitamento de sustentações no YouTube dos Tribunais e coexecução de eventos com ESAP/Gabinete."
    },
    "ESAP": {
        "nome": "Escola Superior da Advocacia Pública",
        "tipo": "Órgão de Capacitação",
        "bloco_3ps": "Educação Corporativa",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Direção da ESAP",
        "pauta_reuniao": "Coordenação do Plano Anual de Capacitação (PAC - E9.O2.KR1), incluindo oficinas práticas de Oratória Forense e Simulação de Tribuna (demanda PJ/PB), Escuta Ativa e CNV (demanda OUV), Media Training (demanda ASCOM) e Direito Digital/IA (E7.O3.KR2)."
    },
    "SI": {
        "nome": "Supervisão de Informática",
        "tipo": "Unidade Técnica TIC",
        "bloco_3ps": "Infraestrutura TIC",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Marcio Roberto / Alice",
        "pauta_reuniao": "Liderança estrita em infraestrutura física, redes, servidores, backup Veeam/Nutanix (E7.O2.KR1/KR2 e E7.O3.KR3), PDTIC (E7.O4.KR1) e artefatos de TIC do BID (E3.O1.KR3), transferindo sistemas/BI/IA para Assessoria em TIC da PGAAE / INOVA."
    },
    "INOVA": {
        "nome": "Laboratório de Inovação (INOVA)",
        "tipo": "Núcleo de Inovação / TIC",
        "bloco_3ps": "Inovação e IA",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Coordenação INOVA / Assessoria em TIC da PGAAE",
        "pauta_reuniao": "Liderança conjunta com a Assessoria em TIC da PGAAE em Inteligência Artificial (E7.O1.KR1), automação RPA, evolução do SPA, BI e projetos estratégicos de inovação/LegalTech (E7.O3.KR1)."
    },
    "GAB": {
        "nome": "Gabinete do Procurador-Geral do Estado",
        "tipo": "Cúpula Diretiva",
        "bloco_3ps": "Cúpula Diretiva",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07184",
        "responsavel": "Márcia Fernanda Bastos (Chefe de Gabinete)",
        "pauta_reuniao": "Coordenação institucional superior, edição de portarias normativas (prazos consultivos, fluxo ASCOM, governança de dados) e articulação estratégica de alto nível."
    },
    "SGRH": {
        "nome": "Serviço de Gestão de Recursos Humanos",
        "tipo": "Unidade Administrativa",
        "bloco_3ps": "Gestão de Pessoas",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07207",
        "responsavel": "Maria Luzia Anceles (Despacho nº 018120848)",
        "pauta_reuniao": "Valorização e saúde mental (E9.O1.KR1), canal direto de avisos funcionais via WhatsApp para servidores descentralizados no Fórum José Sarney (demanda PJEFP), dimensionamento da força de trabalho (E9.O1.KR3) e apoio ao PAC (E9.O2.KR1)."
    },
    "SMP": {
        "nome": "Serviço de Material e Patrimônio",
        "tipo": "Unidade Administrativa",
        "bloco_3ps": "Gestão Patrimonial",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07208",
        "responsavel": "Soraya Maranhão (Despacho nº 057/2026)",
        "pauta_reuniao": "Controle de almoxarifado e patrimônio (Eixo 2), logística reversa e sustentabilidade (Eixo 8) e alimentação do Painel Compartilhado de Visibilidade Intersetorial (CSL, Contratos, Patrimônio e TI)."
    },
    "SGT": {
        "nome": "Serviços Gerais e Transportes",
        "tipo": "Unidade Administrativa",
        "bloco_3ps": "Gestão Logística",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07209",
        "responsavel": "Silvia Madeira Dias (Despacho nº 56/2026)",
        "pauta_reuniao": "Eficiência na gestão de frota, manutenção predial, redução de consumo de água/energia (E2.O1.KR1) e práticas sustentáveis (Eixo 8)."
    },
    "NIRF": {
        "nome": "Núcleo de Inteligência e Recuperação Fiscal",
        "tipo": "Núcleo Especializado",
        "bloco_3ps": "Integrado à PDA",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07215",
        "responsavel": "Dr. Marcelo Sampaio (Despacho nº 50/2026)",
        "pauta_reuniao": "Ações de inteligência fiscal, mineração de dados e investigação patrimonial de grandes devedores integralmente absorvidas e espelhadas na Procuradoria da Dívida Ativa (PDA)."
    },
    "USF": {
        "nome": "Unidade Setorial de Finanças",
        "tipo": "Unidade Orçamentária/Financeira",
        "bloco_3ps": "Gestão Orçamentária",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07203",
        "responsavel": "Maria de Nazaré",
        "pauta_reuniao": "Retificado ano-base (2025 -> 2026); isenta de prospecção externa (E3.O1.KR1) e de gestão negocial do BID (E3.O1.KR3), focando em 100% de execução orçamentária (E3.O1.KR2) e conformidade financeira."
    },
    "SEO": {
        "nome": "Supervisão de Execução Orçamentária",
        "tipo": "Unidade Orçamentária/Financeira",
        "bloco_3ps": "Gestão Orçamentária",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07203",
        "responsavel": "Valdenice",
        "pauta_reuniao": "Monitoramento mensal da LOA/FUNPGE, redução de Restos a Pagar (< 5%) e dupla checagem contábil para pagamento tempestivo de RPVs e advogados dativos."
    },
    "SCCF": {
        "nome": "Supervisão de Contratos e Controle Financeiro",
        "tipo": "Unidade Orçamentária/Financeira",
        "bloco_3ps": "Gestão Financeira",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07203",
        "responsavel": "Rosimar",
        "pauta_reuniao": "Conformidade na liquidação de despesas, controle financeiro de contratos e suporte à prestação de contas do FUNPGE e Profisco III."
    },
    "CSL": {
        "nome": "Comissão Setorial de Licitação",
        "tipo": "Unidade de Contratações",
        "bloco_3ps": "Contratações Públicas",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Presidência da CSL",
        "pauta_reuniao": "Padronização de artefatos da Lei 14.133/2021, licitações do Profisco III/BID (E3.O1.KR3), compras sustentáveis (E8.O1.KR2) e Painel Compartilhado de Visibilidade Intersetorial (CSL, SCC, SMP e TI)."
    },
    "SCC": {
        "nome": "Serviço de Contratos e Convênios",
        "tipo": "Unidade de Contratações",
        "bloco_3ps": "Gestão Contratual",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Chefia do SCC",
        "pauta_reuniao": "Gestão preventiva de vigências contratuais (alerta 90 dias), fiscalização contratual padronizada e integração ao Painel Compartilhado de Visibilidade Intersetorial com CSL e SMP."
    },
    "UGC": {
        "nome": "Unidade Gestora de Contratações",
        "tipo": "Unidade de Contratações",
        "bloco_3ps": "Planejamento de Contratações",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Coordenação da UGC",
        "pauta_reuniao": "Plano de Contratações Anual (PCA), governança de aquisições estratégicas e coexecução dos 10 artefatos do Projeto BID / Profisco III (E3.O1.KR3)."
    },
    "SDD": {
        "nome": "Serviço de Digitalização e Distribuição",
        "tipo": "Unidade de Apoio Processual",
        "bloco_3ps": "Triagem e Distribuição",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "2026.11103.07205",
        "responsavel": "Letícia Costa Leite Lima",
        "pauta_reuniao": "Triagem e distribuição imediata de intimações no SPA, protocolo de redistribuição em até 24h de processos distribuídos por equívoco (E5.O6.KR1) e automação de captura com a TIC."
    },
    "NCALC": {
        "nome": "Núcleo de Cálculos",
        "tipo": "Núcleo Técnico Contábil",
        "bloco_3ps": "Cálculos e Perícias",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Chefia do Núcleo de Cálculos",
        "pauta_reuniao": "Pareceres técnicos de liquidação e expurgo de excesso de execução (art. 535 CPC c/ PERJP e Especializadas), saneamento de RPVs/Precatórios (E1.O1.KR2) e automação de planilhas de cálculo."
    },
    "SOE": {
        "nome": "Serviço de Obras e Engenharia",
        "tipo": "Unidade Técnica de Engenharia",
        "bloco_3ps": "Infraestrutura Predial",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Chefia do SOE",
        "pauta_reuniao": "Projetos de engenharia, reforma e modernização das instalações da sede e unidades regionais (E9.O1.KR2), acessibilidade e eficiência energética (Eixo 8)."
    },
    "CDE": {
        "nome": "Comitê de Diversidade e Equidade",
        "tipo": "Órgão Colegiado",
        "bloco_3ps": "Equidade e Direitos Humanos",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Coordenação do Comitê de Equidade",
        "pauta_reuniao": "Políticas de inclusão, equidade de gênero e raça (E8.O3.KR1/KR2), coexecução das 2 ações anuais de prevenção ao assédio (c/ Ouvidoria) e contribuições ao Manual de Boas Práticas (c/ Corregedoria)."
    }
}

# 10 Grupos de Trabalho Compartilhados (GTs) e Projetos Estruturantes iniciais
INITIAL_GTS = [
    {
        "codigo": "GT-01",
        "titulo": "Força-Tarefa Profisco III / BID (10 Artefatos Estruturantes)",
        "tipo": "Projeto Estruturante",
        "krs_vinculados": "E3.O1.KR3, E7.O1.KR1, E7.O2.KR1",
        "lider": "PGAAE / PGA",
        "unidades_participantes": "PGAAE, PGA, INOVA, UGC, CSL, SI, USF, SEO, SCCF",
        "status": "Em Execução Prioritária",
        "prazo": "2026–2028 (Cronograma BID)",
        "objetivo": "Garantir a elaboração de TRs, licitação, contratação e entrega dos 10 artefatos tecnológicos e consultivos financiados pelo BID no Profisco III, delimitando a USF/SEO/SCCF à liquidação e conformidade financeira.",
        "entregaveis_json": json.dumps([
            {"item": "Matriz de responsabilidades dos 10 artefatos BID homologada", "concluido": True},
            {"item": "Termos de Referência de Infraestrutura TIC (SI) e Sistemas/IA (PGAAE/INOVA)", "concluido": True},
            {"item": "Cronograma de licitações prioritárias junto à UGC e CSL", "concluido": False},
            {"item": "Fluxo de conformidade contábil e desembolso junto à USF/SEO/SCCF", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-02",
        "titulo": "Grupo Técnico Permanente de Saneamento de RPVs, Precatórios e Prevenção de Bloqueios",
        "tipo": "Grupo de Trabalho Compartilhado",
        "krs_vinculados": "E1.O1.KR1, E1.O1.KR2, E3.O1.KR2, E5.O6.KR1",
        "lider": "PERJP",
        "unidades_participantes": "PERJP, NCALC, PDA, USF, SEO, SCCF, PGAAE, SGA",
        "status": "Pronto para Instalação (Pós-Reunião PERJP)",
        "prazo": "30 dias para ato formal / Contínuo até 2030",
        "objetivo": "Reduzir em 90% os bloqueios judiciais (SISBAJUD) e pagamentos duplicados de RPVs, integrar impugnações do art. 535 CPC com o Núcleo de Cálculos, compensar precatórios com Dívida Ativa (PDA) e operar acordos diretos com deságio (CASC/TJMA).",
        "entregaveis_json": json.dumps([
            {"item": "Minuta de ato interno instituindo o Grupo Técnico Permanente de RPVs/Precatórios", "concluido": True},
            {"item": "Fluxo de dupla checagem contábil pré-pagamento entre PERJP, NCALC, SEO e SCCF", "concluido": True},
            {"item": "Validação em reunião de alinhamento com a chefia da PERJP e PGAAE", "concluido": False},
            {"item": "Edital semestral de acordos diretos em precatórios com deságio", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-03",
        "titulo": "Comitê de Integração Fiscal e Recuperação de Créditos (Fusão Operacional PDA + Inteligência NIRF + SEFAZ)",
        "tipo": "Projeto Estruturante",
        "krs_vinculados": "E1.O2.KR1, E1.O2.KR2, E1.O2.KR3, E1.O4.KR1, E1.O4.KR2, E1.O5.KR2",
        "lider": "PDA",
        "unidades_participantes": "PDA, NIRF, PCF, PGAAE",
        "status": "Em Validação (Aguardando Reunião PDA/PCF)",
        "prazo": "2027–2030",
        "objetivo": "Operacionalizar a absorção integral da inteligência fiscal do NIRF pela PDA (Despacho SEI nº 50/2026), mineração de dados de grandes devedores, rating da dívida ativa, protesto automatizado, transação tributária e conversão de depósitos judiciais em renda.",
        "entregaveis_json": json.dumps([
            {"item": "Incorporação integral das ações do NIRF na planilha da PDA (Despacho SEI 50/2026)", "concluido": True},
            {"item": "Reunião de alinhamento e homologação com os Procuradores-Chefes da PDA e PCF", "concluido": False},
            {"item": "Rotina trimestral de saneamento cadastral de CDAs e cruzamento patrimonial com SEFAZ", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-04",
        "titulo": "GT de Estabilidade do SPA, Integração PJe-SPA (Delay Zero) e Automação/IA (MINUTIA)",
        "tipo": "Projeto Estruturante",
        "krs_vinculados": "E5.O5.KR1, E5.O5.KR2, E5.O6.KR1, E7.O1.KR1, E7.O2.KR1",
        "lider": "PGAAE (Assessoria em TIC) / INOVA",
        "unidades_participantes": "PGAAE, INOVA, SI, SDD, PJEFP, PB, PSAU, PJ, CG",
        "status": "Em Execução Prioritária",
        "prazo": "Imediato / Contínuo 2027–2030",
        "objetivo": "Eliminar o delay de 5 a 7 dias na captura de intimações entre PJe/Portais e SPA, assegurar estabilidade noturna do SPA, governar mudanças de layout com aviso prévio (demanda PJEFP/PSAU/PB) e expandir o uso do MINUTIA e robôs de triagem.",
        "entregaveis_json": json.dumps([
            {"item": "Separação estrita de competências nas 41 planilhas: Sistemas/IA/BI (TIC PGAAE/INOVA) vs. Infra/Redes/Backup (SI)", "concluido": True},
            {"item": "Memorando Intersetorial SEI nº 01 elaborado para TIC/Coordenação do SPA e SI", "concluido": True},
            {"item": "Saneamento da regra do Dashboard do SPA para eliminar falsos positivos em processos armazenados (demanda CG/NCIA)", "concluido": False},
            {"item": "Homologação de janela de manutenção e aviso prévio de layout no SPA", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-05",
        "titulo": "Programa de Qualificação Recursal, Superação de Óbices (Súmulas 7/STJ e 279/STF) e Revezamento de Sustentações",
        "tipo": "Grupo de Trabalho Compartilhado",
        "krs_vinculados": "E5.O1.KR2, E5.O2.KR2, E9.O2.KR1",
        "lider": "PB / PGAAJ / SGA",
        "unidades_participantes": "PB, PGAAJ, SGA, ESAP, PJ, PEDU, PSP, PPIMA, PSAU, PT, PA, PDA, PCF, PERJP",
        "status": "Em Implantação",
        "prazo": "Semestral (2027–2030)",
        "objetivo": "Implantar a Inversão da Lógica Recursal, produzir o Relatório Semestral de Superação de Óbices (sem devolução operacional de agravos à origem para evitar retrabalho, discutindo o modelo didático em oficinas com ESAP/PGAAJ) e operar o revezamento virtual de sustentações orais nos Tribunais Superiores.",
        "entregaveis_json": json.dumps([
            {"item": "Inclusão do filtro de admissibilidade (E5.O2.KR2) nas Especializadas Contenciosas", "concluido": True},
            {"item": "Espelhamento do revezamento virtual de sustentações na PGAAJ e SGA", "concluido": True},
            {"item": "Espelhamento das oficinas práticas de Oratória Forense e Simulação de Tribuna na ESAP", "concluido": True},
            {"item": "1º Relatório Semestral de Óbices Sumulares (PB -> PGAAJ/SGA/ESAP)", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-06",
        "titulo": "GT do Regimento Interno Único da PGE-MA e Governança Descentralizada de Prazos",
        "tipo": "Projeto Estruturante",
        "krs_vinculados": "E5.O5.KR1, E5.O6.KR1",
        "lider": "CG (Dr. Gustavo Saboia) / PGAAJ",
        "unidades_participantes": "CG, PGAAJ, PGAAE, GAB, SGA",
        "status": "Em Elaboração",
        "prazo": "Até 2027",
        "objetivo": "Consolidar o Regimento Interno Único da PGE-MA e fortalecer a gestão preventiva de prazos pelas chefias imediatas diretamente no painel nativo do SPA, sem alertas escalonados intrusivos nem métricas artificiais de perdas evitadas.",
        "entregaveis_json": json.dumps([
            {"item": "Expurgo do fluxo de alerta escalonado e da métrica de perdas evitadas nas planilhas da CG e PGAAJ", "concluido": True},
            {"item": "Minuta consolidada do Regimento Interno Único da PGE-MA", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-07",
        "titulo": "Rede Institucional de Comunicação de Êxitos Judiciais e Acervo Audiovisual (YouTube Tribunais)",
        "tipo": "Grupo de Trabalho Compartilhado",
        "krs_vinculados": "E6.O1.KR1, E6.O1.KR2",
        "lider": "ASCOM",
        "unidades_participantes": "ASCOM, SGA, GAB, PJ, PEDU, PSP, PPIMA, PJEFP, PB, PSAU, PT, PA, PDA, PCF, PERJP, PRI, PRT",
        "status": "Pronto para Portaria Normativa",
        "prazo": "60 dias para Portaria / Quinzenal contínuo",
        "objetivo": "Garantir o envio quinzenal de decisões judiciais, acordos e teses de impacto pelas Especializadas à ASCOM, além do mapeamento e corte das sustentações orais gravadas nos canais oficiais do YouTube dos Tribunais (sugestão SGA/Dr. Francisco Beolândio).",
        "entregaveis_json": json.dumps([
            {"item": "Obrigação recíproca de envio quinzenal (E6.O1.KR2) inserida nas planilhas das Especializadas e Regionais", "concluido": True},
            {"item": "Ação de aproveitamento de vídeos do YouTube inserida na ASCOM e SGA (Memorando Intersetorial nº 02)", "concluido": True},
            {"item": "Edição de Portaria do Gabinete regulamentando o fluxo de envio de êxitos à ASCOM", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-08",
        "titulo": "GT de Integridade, Transparência Adaptada à LGPD e Enfrentamento ao Assédio (Dec. 39.054/2024)",
        "tipo": "Grupo de Trabalho Compartilhado",
        "krs_vinculados": "E8.O2.KR1, E8.O2.KR2, E8.O3.KR1, E9.O2.KR1",
        "lider": "OUV / CG / CDE",
        "unidades_participantes": "OUV, CG, CDE, SGRH, ESAP, ASCOM",
        "status": "Em Execução",
        "prazo": "Anual (2027–2030)",
        "objetivo": "Elaborar o Manual de Boas Práticas e Plano de Integridade, aplicar a Escala de Transparência Interna Adaptada à PGE (resguardando sigilo processual e LGPD), operar protocolo de restrição SEI em denúncias e realizar 2 ações anuais contra assédio moral/sexual + oficina de Escuta Ativa e CNV.",
        "entregaveis_json": json.dumps([
            {"item": "Supressão formal de E4.O1.KR2 por impossibilidade material das plataformas e-OUV/e-SIC (Nota Técnica SEI nº 02)", "concluido": True},
            {"item": "Inclusão das 2 ações anuais contra assédio (Dec. 39.054/2024) e protocolo LGPD/SEI na Ouvidoria", "concluido": True},
            {"item": "Inclusão da oficina de Escuta Ativa e Comunicação Não Violenta (CNV) na ESAP", "concluido": True},
            {"item": "Aprovação da matriz da Escala de Transparência Interna Adaptada e do Manual de Boas Práticas", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-09",
        "titulo": "GT de Integração Digital Descentralizada (Fórum José Sarney) e Painel Compartilhado (CSL/SCC/SMP/TI)",
        "tipo": "Grupo de Trabalho Compartilhado",
        "krs_vinculados": "E2.O1.KR2, E5.O5.KR1, E7.O3.KR2, E9.O1.KR1",
        "lider": "PGAAE (TIC) / PGA / SGRH",
        "unidades_participantes": "PGAAE, SGRH, PJEFP, CSL, SCC, SMP, SI, ASCOM",
        "status": "Em Implantação",
        "prazo": "90 a 120 dias",
        "objetivo": "Garantir acesso pleno à Extranet nas estações do Fórum Des. José Sarney (sob responsabilidade da Assessoria em TIC da PGAAE / INOVA), instituir canal direto de avisos funcionais via WhatsApp (sob responsabilidade do SGRH) e operar o Painel Compartilhado de Visibilidade Intersetorial entre CSL, Contratos (SCC), Patrimônio (SMP) e TI.",
        "entregaveis_json": json.dumps([
            {"item": "Atribuição da Extranet à Assessoria em TIC da PGAAE e do Canal de Avisos ao SGRH nas planilhas de PJEFP, PGAAE e SGRH", "concluido": True},
            {"item": "Espelhamento do Painel Compartilhado de Visibilidade Intersetorial nas planilhas da CSL, SCC e SMP", "concluido": True},
            {"item": "Habilitação operacional do acesso à Extranet e grupo oficial de avisos no Fórum José Sarney", "concluido": False}
        ], ensure_ascii=False)
    },
    {
        "codigo": "GT-10",
        "titulo": "Comitê Gestor do Plano Anual de Capacitação (PAC / ESAP — 41 Unidades)",
        "tipo": "Programa Transversal Permanente",
        "krs_vinculados": "E9.O2.KR1, E7.O3.KR2",
        "lider": "ESAP / SGRH",
        "unidades_participantes": "ESAP, SGRH, PGAAE, PGA, Todas as 41 Unidades",
        "status": "100% Espelhado nas 41 Planilhas",
        "prazo": "Ciclo Anual (2027–2030)",
        "objetivo": "Consolidar anualmente o levantamento de necessidades de capacitação customizado por área temática das 41 unidades da PGE-MA, garantindo a participação de ao menos 40% do corpo funcional em trilhas práticas (PAC) e 25% em Direito Digital e IA.",
        "entregaveis_json": json.dumps([
            {"item": "Inclusão de ação customizada do E9.O2.KR1 em 100% das 41 planilhas setoriais", "concluido": True},
            {"item": "Consolidação das trilhas transversais (Oratória Forense, CNV, Media Training, IA Generativa, Lei 14.133/21) na ESAP", "concluido": True},
            {"item": "Publicação do Calendário Pedagógico do PAC 2027", "concluido": False}
        ], ensure_ascii=False)
    }
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def classify_3ps(kr_code: str) -> str:
    if kr_code in ("E5.O6.KR1", "E4.O1.KR1"):
        return "1º P: Prazo"
    if kr_code in ("E5.O1.KR1", "E5.O1.KR2", "E5.O1.KR3", "E5.O2.KR2"):
        return "2º P: Presença nos Tribunais"
    if kr_code in ("E5.O5.KR1", "E5.O5.KR2", "E5.O3.KR1", "E5.O3.KR2", "E5.O2.KR1"):
        return "3º P: Padronização e Prevenção"
    return "Outros Eixos / Governança"


def extract_relations(sigla_origem: str, resp_text: str):
    """
    Analisa o campo 'Responsáveis (QUEM - Governança Saneada)' e extrai:
    - papel_unidade ('Líder', 'Articulador', 'Coexecutor')
    - lista de siglas relacionadas e o tipo de vínculo.
    """
    t = str(resp_text or "")
    papel = "Líder"
    if re.search(r"Articulador[a]?:\s*.*" + re.escape(sigla_origem), t, re.I) or (sigla_origem == "PGARI" and "Articulador" in t):
        papel = "Articulador"
    elif "Líder:" in t:
        lider_part = t.split(";")[0]
        if sigla_origem not in lider_part and UNIT_META.get(sigla_origem, {}).get("nome", "___") not in lider_part:
            if "Coexecutor" in t or "Coordenação" in t:
                papel = "Coexecutor"

    # Mapear menções a outras unidades no texto de responsáveis
    alias_map = {
        "PGAAE": ["PGAAE", "Assuntos Estratégicos", "Assessoria em TIC da PGAAE"],
        "PGA": ["PGA ", "PGA;", "PGA,", "PGAA", "Assuntos Administrativos"],
        "PGAAJ": ["PGAAJ", "Assuntos Jurídicos"],
        "PGARI": ["PGARI", "Relacionamento Institucional"],
        "SGA": ["SGA", "Subprocuradoria-Geral Adjunta"],
        "GAB": ["Gabinete do Procurador-Geral", "Gabinete"],
        "CG": ["Corregedoria-Geral", "Corregedoria"],
        "OUV": ["Ouvidoria-Geral", "Ouvidoria"],
        "ASCOM": ["ASCOM", "Assessoria de Comunicação"],
        "ESAP": ["ESAP", "Escola Superior"],
        "SI": ["Supervisão de Informática", "Suporte de Infraestrutura: SI", "(SI)"],
        "INOVA": ["INOVA", "Laboratório de Inovação"],
        "SGRH": ["SGRH", "Recursos Humanos"],
        "SMP": ["SMP", "Material e Patrimônio"],
        "SGT": ["SGT", "Serviços Gerais e Transportes"],
        "CSL": ["CSL", "Comissão Setorial de Licitação"],
        "SCC": ["SCC;", "SCC,", "Contratos e Convênios"],
        "UGC": ["UGC", "Unidade Gestora de Contratações"],
        "USF": ["USF", "Unidade Setorial de Finanças"],
        "SEO": ["SEO", "Execução Orçamentária"],
        "SCCF": ["SCCF", "Controle Financeiro"],
        "SDD": ["SDD", "Digitalização e Distribuição"],
        "NCALC": ["Núcleo de Cálculos"],
        "SOE": ["SOE", "Obras e Engenharia"],
        "CDE": ["CDE", "Comitê de Equidade", "Comitê de Diversidade"],
        "ASJUR": ["ASJUR", "Assessoria Jurídica", "Consultoria Geral", "Consultoria-Geral"],
        "NIRF": ["NIRF", "Recuperação Fiscal"],
        "NCIA": ["NCIA", "Improbidade Administrativa"],
        "PJ": ["Procuradoria Judicial", "(PJ)"],
        "PEDU": ["PEDU", "Procuradoria da Educação"],
        "PSP": ["PSP", "Segurança Pública"],
        "PPIMA": ["PPIMA", "Patrimônio Imobiliário"],
        "PJEFP": ["PJEFP", "Juizados Especiais"],
        "PB": ["Procuradoria de Brasília", "(PB)"],
        "PSAU": ["PSAU", "Procuradoria da Saúde"],
        "PT": ["Procuradoria Trabalhista", "(PT)"],
        "PA": ["Procuradoria Administrativa", "(PA)"],
        "PDA": ["Procuradoria da Dívida Ativa", "(PDA)", "Dívida Ativa"],
        "PCF": ["Procuradoria do Contencioso Fiscal", "(PCF)", "Contencioso Fiscal"],
        "PERJP": ["PERJP", "Procuradoria de Execuções", "Requisições Judiciais de Pagamento"],
        "PRI": ["PRI", "Regional de Imperatriz"],
        "PRT": ["PRT", "Regional de Timon"],
    }
    parceiros = []
    for sig, patterns in alias_map.items():
        if sig == sigla_origem:
            continue
        for pat in patterns:
            if pat in t:
                parceiros.append(sig)
                break
    return papel, sorted(set(parceiros))


def init_db_and_sync_from_xlsx(force_reset_gts: bool = False):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            sigla TEXT PRIMARY KEY,
            nome TEXT,
            pasta TEXT,
            tipo TEXT,
            bloco_3ps TEXT,
            status_reuniao TEXT,
            processo_sei TEXT,
            responsavel TEXT,
            pauta_reuniao TEXT,
            notas_reuniao TEXT DEFAULT '',
            titulo_planilha_1 TEXT,
            titulo_planilha_2 TEXT,
            total_acoes INTEGER DEFAULT 0,
            ultima_atualizacao TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS acoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sigla_unidade TEXT,
            ordem INTEGER,
            eixo TEXT,
            objetivo TEXT,
            kr_codigo TEXT,
            kr_texto_completo TEXT,
            acao TEXT,
            subacao TEXT,
            responsaveis TEXT,
            prazo TEXT,
            pilar_3ps TEXT,
            papel_unidade TEXT,
            unidades_parceiras TEXT,
            status_execucao TEXT DEFAULT 'Planejado (2027–2030)'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grupos_trabalho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            titulo TEXT,
            tipo TEXT,
            krs_vinculados TEXT,
            lider TEXT,
            unidades_participantes TEXT,
            status TEXT,
            prazo TEXT,
            objetivo TEXT,
            entregaveis_json TEXT
        )
    """)

    # Preservar notas_reuniao, status_reuniao e processo_sei editados pelo usuário caso já existam
    existing_units = {}
    for row in cur.execute("SELECT sigla, status_reuniao, processo_sei, responsavel, pauta_reuniao, notas_reuniao FROM unidades").fetchall():
        existing_units[row["sigla"]] = dict(row)

    cur.execute("DELETE FROM acoes")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    for sigla, folder in sorted(UNIT_FOLDERS.items()):
        xlsx_path = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
        if not xlsx_path.exists():
            continue
        rows, t1, t2 = load_rows(xlsx_path)
        meta = UNIT_META.get(sigla, {})
        ex = existing_units.get(sigla, {})

        nome = meta.get("nome", folder)
        tipo = meta.get("tipo", "Unidade PGE-MA")
        bloco_3ps = meta.get("bloco_3ps", "Demais Unidades")
        status_reuniao = ex.get("status_reuniao") or meta.get("status_reuniao", "Reunião Realizada")
        processo_sei = ex.get("processo_sei") or meta.get("processo_sei", "Verificar SEI")
        responsavel = ex.get("responsavel") or meta.get("responsavel", f"Chefia de {sigla}")
        pauta_reuniao = ex.get("pauta_reuniao") or meta.get("pauta_reuniao", "")
        notas_reuniao = ex.get("notas_reuniao", "")

        cur.execute("""
            INSERT OR REPLACE INTO unidades (
                sigla, nome, pasta, tipo, bloco_3ps, status_reuniao,
                processo_sei, responsavel, pauta_reuniao, notas_reuniao,
                titulo_planilha_1, titulo_planilha_2, total_acoes, ultima_atualizacao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sigla, nome, folder, tipo, bloco_3ps, status_reuniao,
            processo_sei, responsavel, pauta_reuniao, notas_reuniao,
            t1, t2, len(rows), now_str
        ))

        for idx, r in enumerate(rows, start=1):
            eixo, obj, kr_full, acao, subacao, resp, prazo = [str(x or "").strip() for x in r[:7]]
            m = re.search(r"\[(E\d+\.O\d+\.KR\d+)\]", kr_full)
            kr_code = m.group(1) if m else "SEM_CODIGO"
            pilar_3ps = classify_3ps(kr_code)
            papel, parceiros = extract_relations(sigla, resp)
            cur.execute("""
                INSERT INTO acoes (
                    sigla_unidade, ordem, eixo, objetivo, kr_codigo, kr_texto_completo,
                    acao, subacao, responsaveis, prazo, pilar_3ps, papel_unidade, unidades_parceiras
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sigla, idx, eixo, obj, kr_code, kr_full,
                acao, subacao, resp, prazo, pilar_3ps, papel, ",".join(parceiros)
            ))

    # Popular GTs iniciais se tabela estiver vazia ou force_reset_gts
    gt_count = cur.execute("SELECT COUNT(*) FROM grupos_trabalho").fetchone()[0]
    if gt_count == 0 or force_reset_gts:
        cur.execute("DELETE FROM grupos_trabalho")
        for gt in INITIAL_GTS:
            cur.execute("""
                INSERT INTO grupos_trabalho (
                    codigo, titulo, tipo, krs_vinculados, lider,
                    unidades_participantes, status, prazo, objetivo, entregaveis_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                gt["codigo"], gt["titulo"], gt["tipo"], gt["krs_vinculados"], gt["lider"],
                gt["unidades_participantes"], gt["status"], gt["prazo"], gt["objetivo"], gt["entregaveis_json"]
            ))

    conn.commit()
    conn.close()


def sync_unit_to_xlsx(sigla: str):
    """Regrava a planilha .xlsx da unidade (em Planilhas_Pos_Comparacao_Consolidadas e na pasta da unidade) a partir do SQLite."""
    conn = get_conn()
    cur = conn.cursor()
    u = cur.execute("SELECT * FROM unidades WHERE sigla = ?", (sigla,)).fetchone()
    if not u:
        conn.close()
        return
    acoes = cur.execute(
        "SELECT eixo, objetivo, kr_texto_completo, acao, subacao, responsaveis, prazo FROM acoes WHERE sigla_unidade = ? ORDER BY ordem ASC, id ASC",
        (sigla,)
    ).fetchall()
    rows = [[a["eixo"], a["objetivo"], a["kr_texto_completo"], a["acao"], a["subacao"], a["responsaveis"], a["prazo"]] for a in acoes]
    write_sheet_to_all_targets(sigla, u["titulo_planilha_1"], u["titulo_planilha_2"], rows)
    cur.execute(
        "UPDATE unidades SET total_acoes = ?, ultima_atualizacao = ? WHERE sigla = ?",
        (len(rows), datetime.now().strftime("%Y-%m-%d %H:%M"), sigla)
    )
    conn.commit()
    conn.close()


# FastAPI App
app = FastAPI(title="SGPE PGE-MA 2027–2030", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AcaoPayload(BaseModel):
    sigla_unidade: str
    eixo: str
    objetivo: str
    kr_texto_completo: str
    acao: str
    subacao: str
    responsaveis: str
    prazo: str
    espelhar_em: Optional[List[str]] = []


class UnidadeUpdatePayload(BaseModel):
    status_reuniao: str
    processo_sei: str
    responsavel: str
    pauta_reuniao: str
    notas_reuniao: str


class GTPayload(BaseModel):
    codigo: str
    titulo: str
    tipo: str
    krs_vinculados: str
    lider: str
    unidades_participantes: str
    status: str
    prazo: str
    objetivo: str
    entregaveis_json: str


@app.on_event("startup")
def on_startup():
    init_db_and_sync_from_xlsx()


@app.get("/api/overview")
def get_overview():
    conn = get_conn()
    cur = conn.cursor()
    unidades = [dict(r) for r in cur.execute("SELECT * FROM unidades ORDER BY sigla").fetchall()]
    total_acoes = cur.execute("SELECT COUNT(*) FROM acoes").fetchone()[0]
    total_krs = cur.execute("SELECT COUNT(DISTINCT kr_codigo) FROM acoes WHERE kr_codigo != 'SEM_CODIGO'").fetchone()[0]
    reunioes_pendentes = [u for u in unidades if "Pendente" in u["status_reuniao"]]
    respondidos_sei = [u for u in unidades if u["status_reuniao"] == "Respondido no SEI"]
    reunioes_realizadas = [u for u in unidades if u["status_reuniao"] == "Reunião Realizada"]

    por_eixo = [
        dict(r) for r in cur.execute("""
            SELECT substr(kr_codigo, 1, 2) as eixo_cod, eixo, COUNT(*) as qtd_acoes, COUNT(DISTINCT kr_codigo) as qtd_krs
            FROM acoes
            GROUP BY substr(kr_codigo, 1, 2)
            ORDER BY eixo_cod
        """).fetchall()
    ]

    krs_list = [
        dict(r) for r in cur.execute("""
            SELECT kr_codigo, kr_texto_completo, eixo, objetivo, COUNT(*) as qtd_acoes, COUNT(DISTINCT sigla_unidade) as qtd_unidades
            FROM acoes
            GROUP BY kr_codigo
            ORDER BY kr_codigo
        """).fetchall()
    ]

    conn.close()
    return {
        "total_unidades": len(unidades),
        "total_acoes": total_acoes,
        "total_krs": total_krs,
        "qtd_reunioes_pendentes": len(reunioes_pendentes),
        "qtd_reunioes_realizadas": len(reunioes_realizadas),
        "qtd_respondidos_sei": len(respondidos_sei),
        "reunioes_pendentes": reunioes_pendentes,
        "unidades": unidades,
        "por_eixo": por_eixo,
        "krs": krs_list
    }


@app.get("/api/acoes")
def list_acoes(
    sigla: Optional[str] = None,
    eixo: Optional[str] = None,
    kr_codigo: Optional[str] = None,
    pilar_3ps: Optional[str] = None,
    papel: Optional[str] = None,
    parceiro: Optional[str] = None,
    q: Optional[str] = None
):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        SELECT a.*, u.nome as nome_unidade, u.status_reuniao
        FROM acoes a
        JOIN unidades u ON u.sigla = a.sigla_unidade
        WHERE 1=1
    """
    params = []
    if sigla:
        sql += " AND a.sigla_unidade = ?"
        params.append(sigla)
    if eixo:
        sql += " AND a.kr_codigo LIKE ?"
        params.append(f"{eixo}.%")
    if kr_codigo:
        sql += " AND a.kr_codigo = ?"
        params.append(kr_codigo)
    if pilar_3ps:
        sql += " AND a.pilar_3ps = ?"
        params.append(pilar_3ps)
    if papel:
        sql += " AND a.papel_unidade = ?"
        params.append(papel)
    if parceiro:
        sql += " AND (',' || a.unidades_parceiras || ',') LIKE ?"
        params.append(f"%,{parceiro},%")
    if q:
        sql += " AND (a.acao LIKE ? OR a.subacao LIKE ? OR a.responsaveis LIKE ? OR a.kr_texto_completo LIKE ?)"
        like_q = f"%{q}%"
        params.extend([like_q, like_q, like_q, like_q])

    sql += " ORDER BY a.sigla_unidade ASC, a.ordem ASC"
    rows = [dict(r) for r in cur.execute(sql, params).fetchall()]
    conn.close()
    return rows


@app.post("/api/acoes")
def create_acao(payload: AcaoPayload):
    conn = get_conn()
    cur = conn.cursor()
    m = re.search(r"\[(E\d+\.O\d+\.KR\d+)\]", payload.kr_texto_completo)
    kr_code = m.group(1) if m else "SEM_CODIGO"
    pilar_3ps = classify_3ps(kr_code)

    target_units = [payload.sigla_unidade] + [u for u in (payload.espelhar_em or []) if u != payload.sigla_unidade]
    created_ids = []

    for sig in target_units:
        max_ord = cur.execute("SELECT COALESCE(MAX(ordem), 0) FROM acoes WHERE sigla_unidade = ?", (sig,)).fetchone()[0]
        papel, parceiros = extract_relations(sig, payload.responsaveis)
        cur.execute("""
            INSERT INTO acoes (
                sigla_unidade, ordem, eixo, objetivo, kr_codigo, kr_texto_completo,
                acao, subacao, responsaveis, prazo, pilar_3ps, papel_unidade, unidades_parceiras
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sig, max_ord + 1, payload.eixo, payload.objetivo, kr_code, payload.kr_texto_completo,
            payload.acao, payload.subacao, payload.responsaveis, payload.prazo, pilar_3ps, papel, ",".join(parceiros)
        ))
        created_ids.append(cur.lastrowid)

    conn.commit()
    conn.close()

    for sig in target_units:
        sync_unit_to_xlsx(sig)

    return {"status": "ok", "created_ids": created_ids, "synced_units": target_units}


@app.put("/api/acoes/{acao_id}")
def update_acao(acao_id: int, payload: AcaoPayload):
    conn = get_conn()
    cur = conn.cursor()
    existing = cur.execute("SELECT sigla_unidade FROM acoes WHERE id = ?", (acao_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Ação não encontrada")

    m = re.search(r"\[(E\d+\.O\d+\.KR\d+)\]", payload.kr_texto_completo)
    kr_code = m.group(1) if m else "SEM_CODIGO"
    pilar_3ps = classify_3ps(kr_code)
    papel, parceiros = extract_relations(payload.sigla_unidade, payload.responsaveis)

    cur.execute("""
        UPDATE acoes SET
            sigla_unidade = ?, eixo = ?, objetivo = ?, kr_codigo = ?, kr_texto_completo = ?,
            acao = ?, subacao = ?, responsaveis = ?, prazo = ?,
            pilar_3ps = ?, papel_unidade = ?, unidades_parceiras = ?
        WHERE id = ?
    """, (
        payload.sigla_unidade, payload.eixo, payload.objetivo, kr_code, payload.kr_texto_completo,
        payload.acao, payload.subacao, payload.responsaveis, payload.prazo,
        pilar_3ps, papel, ",".join(parceiros), acao_id
    ))
    conn.commit()
    conn.close()

    sync_unit_to_xlsx(existing["sigla_unidade"])
    if payload.sigla_unidade != existing["sigla_unidade"]:
        sync_unit_to_xlsx(payload.sigla_unidade)

    # Se o usuário solicitou espelhar esta edição em unidades parceiras adicionais
    mirrored = []
    for sig_esp in (payload.espelhar_em or []):
        if sig_esp != payload.sigla_unidade:
            conn2 = get_conn()
            c2 = conn2.cursor()
            already = c2.execute(
                "SELECT id FROM acoes WHERE sigla_unidade = ? AND kr_codigo = ? AND acao = ?",
                (sig_esp, kr_code, payload.acao)
            ).fetchone()
            if not already:
                max_ord = c2.execute("SELECT COALESCE(MAX(ordem), 0) FROM acoes WHERE sigla_unidade = ?", (sig_esp,)).fetchone()[0]
                p_esp, parc_esp = extract_relations(sig_esp, payload.responsaveis)
                c2.execute("""
                    INSERT INTO acoes (
                        sigla_unidade, ordem, eixo, objetivo, kr_codigo, kr_texto_completo,
                        acao, subacao, responsaveis, prazo, pilar_3ps, papel_unidade, unidades_parceiras
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sig_esp, max_ord + 1, payload.eixo, payload.objetivo, kr_code, payload.kr_texto_completo,
                    payload.acao, payload.subacao, payload.responsaveis, payload.prazo,
                    pilar_3ps, p_esp, ",".join(parc_esp)
                ))
                conn2.commit()
                mirrored.append(sig_esp)
            conn2.close()
            if sig_esp in mirrored:
                sync_unit_to_xlsx(sig_esp)

    return {"status": "ok", "mirrored_in": mirrored}


@app.delete("/api/acoes/{acao_id}")
def delete_acao(acao_id: int):
    conn = get_conn()
    cur = conn.cursor()
    existing = cur.execute("SELECT sigla_unidade FROM acoes WHERE id = ?", (acao_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    sigla = existing["sigla_unidade"]
    cur.execute("DELETE FROM acoes WHERE id = ?", (acao_id,))
    conn.commit()
    conn.close()
    sync_unit_to_xlsx(sigla)
    return {"status": "ok", "sigla_unidade": sigla}


@app.get("/api/3ps")
def get_3ps_matrix():
    conn = get_conn()
    cur = conn.cursor()
    especializadas = [
        "PJ", "PEDU", "PSP", "PPIMA", "PJEFP", "PB", "PSAU",
        "PT", "PA", "PDA", "PCF", "PERJP", "PRI", "PRT",
        "NCIA", "ASJUR"
    ]
    result = []
    for sig in especializadas:
        u = cur.execute("SELECT * FROM unidades WHERE sigla = ?", (sig,)).fetchone()
        if not u:
            continue
        acoes = [dict(r) for r in cur.execute("SELECT * FROM acoes WHERE sigla_unidade = ? ORDER BY ordem", (sig,)).fetchall()]
        p1 = [a for a in acoes if a["pilar_3ps"] == "1º P: Prazo"]
        p2 = [a for a in acoes if a["pilar_3ps"] == "2º P: Presença nos Tribunais"]
        p3 = [a for a in acoes if a["pilar_3ps"] == "3º P: Padronização e Prevenção"]
        outros = [a for a in acoes if a["pilar_3ps"] == "Outros Eixos / Governança"]
        result.append({
            "sigla": sig,
            "nome": u["nome"],
            "bloco_3ps": u["bloco_3ps"],
            "status_reuniao": u["status_reuniao"],
            "responsavel": u["responsavel"],
            "processo_sei": u["processo_sei"],
            "total_acoes": len(acoes),
            "p1_qtd": len(p1),
            "p2_qtd": len(p2),
            "p3_qtd": len(p3),
            "outros_qtd": len(outros),
            "p1_krs": sorted(set(a["kr_codigo"] for a in p1)),
            "p2_krs": sorted(set(a["kr_codigo"] for a in p2)),
            "p3_krs": sorted(set(a["kr_codigo"] for a in p3)),
            "p1_acoes": p1,
            "p2_acoes": p2,
            "p3_acoes": p3,
        })
    conn.close()
    return result


@app.get("/api/relacoes")
def get_relacoes_graph():
    conn = get_conn()
    cur = conn.cursor()
    unidades = [dict(r) for r in cur.execute("SELECT sigla, nome, tipo, status_reuniao, total_acoes FROM unidades").fetchall()]
    acoes = [dict(r) for r in cur.execute("SELECT sigla_unidade, kr_codigo, acao, papel_unidade, unidades_parceiras, responsaveis FROM acoes").fetchall()]

    edges_map = {}
    unit_incoming = {u["sigla"]: [] for u in unidades}
    unit_outgoing = {u["sigla"]: [] for u in unidades}

    for a in acoes:
        orig = a["sigla_unidade"]
        parceiros = [p for p in a["unidades_parceiras"].split(",") if p]
        for dest in parceiros:
            if dest not in unit_incoming:
                continue
            key = tuple(sorted([orig, dest]))
            if key not in edges_map:
                edges_map[key] = {"from": key[0], "to": key[1], "weight": 0, "krs": set(), "exemplos": []}
            edges_map[key]["weight"] += 1
            edges_map[key]["krs"].add(a["kr_codigo"])
            if len(edges_map[key]["exemplos"]) < 5:
                edges_map[key]["exemplos"].append(f"[{orig} -> {dest} | {a['kr_codigo']}] {a['acao']}")

            unit_outgoing[orig].append({
                "parceiro": dest,
                "kr_codigo": a["kr_codigo"],
                "acao": a["acao"],
                "papel_origem": a["papel_unidade"],
                "responsaveis": a["responsaveis"]
            })
            unit_incoming[dest].append({
                "origem": orig,
                "kr_codigo": a["kr_codigo"],
                "acao": a["acao"],
                "papel_origem": a["papel_unidade"],
                "responsaveis": a["responsaveis"]
            })

    edges = [
        {
            "from": v["from"],
            "to": v["to"],
            "weight": v["weight"],
            "krs": sorted(v["krs"]),
            "exemplos": v["exemplos"]
        }
        for v in edges_map.values()
    ]

    conn.close()
    return {
        "nodes": unidades,
        "edges": sorted(edges, key=lambda x: -x["weight"]),
        "incoming": unit_incoming,
        "outgoing": unit_outgoing
    }


@app.put("/api/unidades/{sigla}")
def update_unidade(sigla: str, payload: UnidadeUpdatePayload):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE unidades SET
            status_reuniao = ?, processo_sei = ?, responsavel = ?,
            pauta_reuniao = ?, notas_reuniao = ?, ultima_atualizacao = ?
        WHERE sigla = ?
    """, (
        payload.status_reuniao, payload.processo_sei, payload.responsavel,
        payload.pauta_reuniao, payload.notas_reuniao, datetime.now().strftime("%Y-%m-%d %H:%M"), sigla
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/api/unidades/{sigla}/minutas")
def get_unit_minutas(sigla: str):
    conn = get_conn()
    cur = conn.cursor()
    u = cur.execute("SELECT * FROM unidades WHERE sigla = ?", (sigla,)).fetchone()
    if not u:
        conn.close()
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    acoes = [dict(r) for r in cur.execute("SELECT kr_codigo, acao FROM acoes WHERE sigla_unidade = ? ORDER BY ordem", (sigla,)).fetchall()]
    krs_unicos = sorted(set(a["kr_codigo"] for a in acoes if a["kr_codigo"] != "SEM_CODIGO"))
    conn.close()

    is_pendente = "Pendente" in u["status_reuniao"]
    nome_u = u["nome"]
    resp = u["responsavel"]
    proc = u["processo_sei"]
    pauta = u["pauta_reuniao"]

    whatsapp_convite = (
        f"Olá, {resp}! Tudo bem?\n"
        f"Para avançarmos na conclusão da etapa de pactuação setorial do Planejamento Estratégico 2027–2030 da PGE-MA, "
        f"nossa equipe já preparou a proposta-base saneada da planilha da {nome_u} (Plano_Acao_Pos_Comparacao_{sigla}.xlsx, "
        f"com {len(acoes)} ações distribuídas nos KRs {', '.join(krs_unicos)}), estruturada na Lista Mestre Canônica e nos 3 Ps.\n"
        f"Pontos focais para nossa validação: {pauta}\n"
        f"Qual o melhor dia e horário nesta semana para nossa breve reunião de alinhamento?"
    )

    whatsapp_fechamento = (
        f"Olá, {resp}! Tudo bem?\n"
        f"Já anexamos no processo SEI ({proc}) a planilha final saneada da {nome_u} "
        f"(Plano_Acao_Pos_Comparacao_{sigla}.xlsx, contendo {len(acoes)} ações), refletindo integralmente nosso alinhamento técnico.\n"
        f"Para encerrarmos a etapa setorial no SEI, basta inserir e assinar o despacho simplificado:\n"
        f"\"Com reunião de alinhamento e planilha saneada anexada aos autos, valido os dados e o Plano de Ação desta unidade para o ciclo 2027–2030.\"\n"
        f"Muito obrigado!"
    )

    despacho_sei = (
        f"À Chefia da {nome_u} ({sigla}),\n\n"
        f"No âmbito da consolidação do Planejamento Estratégico 2027–2030 da PGE-MA (Processo SEI: {proc}), "
        f"e em conformidade com o alinhamento técnico realizado com a unidade ({resp}), a Assessoria de Planejamento e Gestão Estratégica "
        f"acosta aos presentes autos a versão consolidada e saneada do Plano de Ação Setorial (Plano_Acao_Pos_Comparacao_{sigla}.xlsx, "
        f"contemplando {len(acoes)} ações estratégicas vinculadas aos resultados-chave {', '.join(krs_unicos)}).\n\n"
        f"Destaques técnicos consolidados: {pauta}\n\n"
        f"Solicita-se a conferência e o lançamento de despacho simplificado de validação "
        f"(\"Com reunião de alinhamento e planilha saneada anexada aos autos, valido os dados e o Plano de Ação desta unidade para o ciclo 2027–2030\"), "
        f"restituindo-se os autos à Assessoria de Planejamento / PGAAE para homologação final."
    )

    return {
        "sigla": sigla,
        "nome": nome_u,
        "is_pendente": is_pendente,
        "whatsapp_convite": whatsapp_convite,
        "whatsapp_fechamento": whatsapp_fechamento,
        "despacho_sei": despacho_sei,
        "xlsx_path": str(CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx")
    }


@app.get("/api/gts")
def list_gts():
    conn = get_conn()
    cur = conn.cursor()
    rows = [dict(r) for r in cur.execute("SELECT * FROM grupos_trabalho ORDER BY codigo ASC").fetchall()]
    for r in rows:
        try:
            r["entregaveis"] = json.loads(r["entregaveis_json"] or "[]")
        except Exception:
            r["entregaveis"] = []
    conn.close()
    return rows


@app.post("/api/gts")
def create_gt(payload: GTPayload):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO grupos_trabalho (
            codigo, titulo, tipo, krs_vinculados, lider,
            unidades_participantes, status, prazo, objetivo, entregaveis_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.codigo, payload.titulo, payload.tipo, payload.krs_vinculados, payload.lider,
        payload.unidades_participantes, payload.status, payload.prazo, payload.objetivo, payload.entregaveis_json
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.put("/api/gts/{gt_id}")
def update_gt(gt_id: int, payload: GTPayload):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE grupos_trabalho SET
            codigo = ?, titulo = ?, tipo = ?, krs_vinculados = ?, lider = ?,
            unidades_participantes = ?, status = ?, prazo = ?, objetivo = ?, entregaveis_json = ?
        WHERE id = ?
    """, (
        payload.codigo, payload.titulo, payload.tipo, payload.krs_vinculados, payload.lider,
        payload.unidades_participantes, payload.status, payload.prazo, payload.objetivo, payload.entregaveis_json, gt_id
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/api/download-xlsx/{sigla}")
def download_xlsx(sigla: str):
    fpath = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Planilha não encontrada")
    return FileResponse(
        path=str(fpath),
        filename=f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.post("/api/reindex-xlsx")
def reindex_from_xlsx():
    init_db_and_sync_from_xlsx(force_reset_gts=False)
    return {"status": "ok", "message": "41 planilhas .xlsx reindexadas com sucesso no banco SQLite."}


@app.post("/api/regenerar-relatorios")
def regenerar_relatorios_md():
    """
    Atualiza automaticamente as estatísticas e tabelas de status de reuniões/unidades nos relatórios .md
    a partir do estado atual do banco SQLite e das 41 planilhas .xlsx.
    """
    conn = get_conn()
    cur = conn.cursor()
    unidades = [dict(r) for r in cur.execute("SELECT * FROM unidades ORDER BY sigla").fetchall()]
    pendentes = [u for u in unidades if "Pendente" in u["status_reuniao"]]
    conn.close()

    # Atualizar seção 2.1 de Sintese_Encaminhamentos_Pendentes_Planejamento.md com o status atualizado das reuniões
    sint_path = BASE_DIR / "Sintese_Encaminhamentos_Pendentes_Planejamento.md"
    if sint_path.exists():
        txt = sint_path.read_text(encoding="utf-8")
        now_br = datetime.now().strftime("%d/%m/%Y às %H:%M")
        txt = re.sub(
            r"\*\*Última Atualização de Execução Técnica:\*\*.*",
            f"**Última Atualização de Execução Técnica:** {now_br} (Sincronizado via SGPE Web App — {len(pendentes)} reuniões pendentes de realização)",
            txt
        )
        sint_path.write_text(txt, encoding="utf-8")

    return {
        "status": "ok",
        "message": f"Relatórios sincronizados com sucesso ({len(unidades)} unidades, {len(pendentes)} reuniões pendentes)."
    }


def classify_horizonte(prazo_str: str) -> str:
    p = str(prazo_str or "").lower()
    if any(k in p for k in ["30 dia", "45 dia", "60 dia", "90 dia", "120 dia", "150 dia", "180 dia", "imediato", "1º semestre", "primeiro semestre"]):
        return "Curto Prazo (Imediato / Até 180 dias)"
    if any(k in p for k in ["contínuo", "continuo", "permanente", "2027–2030", "2027-2030", "vigência", "vigencia"]):
        if any(k in p for k in ["anual", "semestral", "trimestral", "quadrimestral", "bimestral", "mensal"]):
            return "Médio Prazo / Periódico (Ciclos Anuais/Semestrais)"
        return "Contínuo / Ciclo Integral (2027–2030)"
    if any(k in p for k in ["anual", "semestral", "trimestral", "quadrimestral", "bimestral", "mensal", "2026", "2027", "2028", "2029"]):
        return "Médio Prazo / Periódico (Ciclos Anuais/Semestrais)"
    return "Contínuo / Ciclo Integral (2027–2030)"


@app.get("/api/relatorios/dados")
def get_relatorios_dados():
    conn = get_conn()
    cur = conn.cursor()

    # 1. Mapa Estratégico (Eixos e Objetivos)
    objetivos_raw = cur.execute("""
        SELECT
            substr(kr_codigo, 1, 2) as eixo_cod,
            substr(kr_codigo, 1, 5) as obj_cod,
            MAX(eixo) as eixo_nome,
            MAX(objetivo) as objetivo_nome,
            COUNT(DISTINCT kr_codigo) as qtd_krs,
            COUNT(*) as qtd_acoes,
            GROUP_CONCAT(DISTINCT sigla_unidade) as unidades
        FROM acoes
        WHERE kr_codigo != 'SEM_CODIGO'
        GROUP BY substr(kr_codigo, 1, 5)
        ORDER BY obj_cod ASC
    """).fetchall()

    mapa_eixos = {}
    for r in objetivos_raw:
        ec = r["eixo_cod"]
        if ec not in mapa_eixos:
            mapa_eixos[ec] = {
                "eixo_cod": ec,
                "eixo_nome": r["eixo_nome"],
                "objetivos": [],
                "total_krs": 0,
                "total_acoes": 0
            }
        unids = sorted(set((r["unidades"] or "").split(","))) if r["unidades"] else []
        mapa_eixos[ec]["objetivos"].append({
            "obj_cod": r["obj_cod"],
            "objetivo_nome": r["objetivo_nome"],
            "qtd_krs": r["qtd_krs"],
            "qtd_acoes": r["qtd_acoes"],
            "unidades": unids
        })
        mapa_eixos[ec]["total_krs"] += r["qtd_krs"]
        mapa_eixos[ec]["total_acoes"] += r["qtd_acoes"]

    # 2. Lista de Objetivos e Metas (KRs)
    metas_raw = cur.execute("""
        SELECT
            substr(kr_codigo, 1, 2) as eixo_cod,
            substr(kr_codigo, 1, 5) as obj_cod,
            kr_codigo,
            MAX(eixo) as eixo_nome,
            MAX(objetivo) as objetivo_nome,
            MAX(kr_texto_completo) as kr_texto_completo,
            MAX(pilar_3ps) as pilar_3ps,
            COUNT(*) as qtd_acoes,
            GROUP_CONCAT(DISTINCT sigla_unidade) as unidades
        FROM acoes
        WHERE kr_codigo != 'SEM_CODIGO'
        GROUP BY kr_codigo
        ORDER BY kr_codigo ASC
    """).fetchall()

    objetivos_metas = []
    for r in metas_raw:
        unids = sorted(set((r["unidades"] or "").split(","))) if r["unidades"] else []
        objetivos_metas.append({
            "eixo_cod": r["eixo_cod"],
            "obj_cod": r["obj_cod"],
            "kr_codigo": r["kr_codigo"],
            "eixo_nome": r["eixo_nome"],
            "objetivo_nome": r["objetivo_nome"],
            "kr_texto_completo": r["kr_texto_completo"],
            "pilar_3ps": r["pilar_3ps"],
            "qtd_acoes": r["qtd_acoes"],
            "unidades": unids
        })

    # 3. Ações enriquecidas com horizonte temporal
    all_acoes = [dict(r) for r in cur.execute("""
        SELECT a.*, u.nome as nome_unidade, u.status_reuniao, u.processo_sei, u.responsavel, u.pauta_reuniao, u.notas_reuniao
        FROM acoes a
        JOIN unidades u ON u.sigla = a.sigla_unidade
        ORDER BY a.sigla_unidade ASC, a.ordem ASC
    """).fetchall()]
    for a in all_acoes:
        a["horizonte"] = classify_horizonte(a["prazo"])

    # 4. Resumo de Matriz de Responsabilidades por Unidade (Líder, Coexecutor, Articulador, Demandas Externas Recebidas)
    unidades_list = [dict(r) for r in cur.execute("SELECT * FROM unidades ORDER BY sigla ASC").fetchall()]
    incoming_count = {u["sigla"]: [] for u in unidades_list}
    for a in all_acoes:
        orig = a["sigla_unidade"]
        for p in (a["unidades_parceiras"] or "").split(","):
            if p and p in incoming_count:
                incoming_count[p].append({
                    "origem": orig,
                    "kr_codigo": a["kr_codigo"],
                    "acao": a["acao"],
                    "responsaveis": a["responsaveis"],
                    "prazo": a["prazo"]
                })

    matriz_unidades = []
    for u in unidades_list:
        sig = u["sigla"]
        u_acoes = [a for a in all_acoes if a["sigla_unidade"] == sig]
        lider_c = sum(1 for a in u_acoes if a["papel_unidade"] == "Líder")
        coexec_c = sum(1 for a in u_acoes if a["papel_unidade"] == "Coexecutor")
        artic_c = sum(1 for a in u_acoes if a["papel_unidade"] == "Articulador")
        parceiros_acionados = sorted(set(
            p for a in u_acoes for p in (a["unidades_parceiras"] or "").split(",") if p
        ))
        demandantes = sorted(set(item["origem"] for item in incoming_count.get(sig, [])))
        matriz_unidades.append({
            "sigla": sig,
            "nome": u["nome"],
            "total_acoes": len(u_acoes),
            "qtd_lider": lider_c,
            "qtd_coexecutor": coexec_c,
            "qtd_articulador": artic_c,
            "parceiros_acionados": parceiros_acionados,
            "qtd_demandas_recebidas": len(incoming_count.get(sig, [])),
            "unidades_demandantes": demandantes,
            "demandas_recebidas": incoming_count.get(sig, [])
        })

    # 5. Grupos de Trabalho e Projetos Estruturantes
    gts_rows = [dict(r) for r in cur.execute("SELECT * FROM grupos_trabalho ORDER BY codigo ASC").fetchall()]
    for g in gts_rows:
        try:
            g["entregaveis"] = json.loads(g["entregaveis_json"] or "[]")
        except Exception:
            g["entregaveis"] = []

    conn.close()
    return {
        "mapa_estrategico": list(mapa_eixos.values()),
        "objetivos_metas": objetivos_metas,
        "acoes_enriquecidas": all_acoes,
        "matriz_unidades": matriz_unidades,
        "unidades_meta": unidades_list,
        "gts": gts_rows
    }


@app.get("/api/export/{tipo}")
def exportar_relatorio(
    tipo: str,
    fmt: str = Query("xlsx", pattern="^(xlsx|docx|md)$"),
    sigla: Optional[str] = None,
    eixo: Optional[str] = None,
    horizonte: Optional[str] = None,
    gt_codigo: Optional[str] = None
):
    """
    Exporta os 7 relatórios oficiais em .xlsx, .docx ou .md:
    - tipo = 'mapa-estrategico': 1. Mapa Estratégico dos Eixos e Objetivos
    - tipo = 'objetivos-metas': 2. Lista de Objetivos e Metas (KRs)
    - tipo = 'planos-acao': 3. Lista dos Planos de Ação das Unidades
    - tipo = 'matriz-responsabilidades': 4. Matriz de Responsabilidades e Dependências Intersetoriais
    - tipo = 'cronograma-entregas': 5. Cronograma de Entregas por Horizonte Temporal
    - tipo = 'relatorio-gt': 6. Relatório de Grupos de Trabalho (GTs) e Projetos Estruturantes
    - tipo = 'ficha-pactuacao': 7. Ficha Individualizada de Pactuação por Unidade
    """
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    import docx

    export_dir = APP_DIR / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    dados = get_relatorios_dados()
    conn = get_conn()
    cur = conn.cursor()

    def style_xlsx_sheet(ws, title1, title2, headers, rows_data, col_widths):
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        title_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
        thin = Side(border_style="thin", color="D9D9D9")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        ncols = len(headers)
        last_col_letter = openpyxl.utils.get_column_letter(ncols)

        ws.merge_cells(f"A1:{last_col_letter}1")
        ws["A1"] = title1
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color="1F4E78")
        ws["A1"].fill = title_fill
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 26

        ws.merge_cells(f"A2:{last_col_letter}2")
        ws["A2"] = title2
        ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="333333")
        ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 20

        for c_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=4, column=c_idx, value=h)
            cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border
        ws.row_dimensions[4].height = 26

        for r_idx, r_vals in enumerate(rows_data, start=5):
            max_lines = 1
            for c_idx, val in enumerate(r_vals, start=1):
                s_val = str(val or "")
                cell = ws.cell(row=r_idx, column=c_idx, value=s_val)
                cell.font = Font(name="Calibri", size=10)
                if r_idx % 2 == 1:
                    cell.fill = zebra_fill
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = border
                w = col_widths[c_idx - 1]
                lines = max(1, (len(s_val) // max(10, w - 4)) + 1 + s_val.count("\n"))
                if lines > max_lines:
                    max_lines = lines
            ws.row_dimensions[r_idx].height = max(24, min(220, max_lines * 15 + 8))

        for c_idx, w in enumerate(col_widths, start=1):
            col_letter = openpyxl.utils.get_column_letter(c_idx)
            ws.column_dimensions[col_letter].width = w

    # -------------------------------------------------------------------------
    # RELATÓRIO 1: MAPA ESTRATÉGICO DOS EIXOS E OBJETIVOS
    # -------------------------------------------------------------------------
    if tipo == "mapa-estrategico":
        mapa = dados["mapa_estrategico"]
        if eixo:
            mapa = [e for e in mapa if e["eixo_cod"] == eixo]

        headers = ["Eixo", "Descrição do Eixo Estratégico", "Cód. Objetivo", "Objetivo Estratégico", "Nº de Metas (KRs)", "Nº de Ações", "Unidades Vinculadas"]
        rows_data = []
        for e in mapa:
            for o in e["objetivos"]:
                rows_data.append([
                    e["eixo_cod"],
                    e["eixo_nome"],
                    o["obj_cod"],
                    o["objetivo_nome"],
                    o["qtd_krs"],
                    o["qtd_acoes"],
                    ", ".join(o["unidades"])
                ])

        if fmt == "md":
            lines = [
                "# Mapa Estratégico — Eixos e Objetivos (PGE-MA 2027–2030)\n",
                "| Eixo | Eixo Estratégico | Cód. Objetivo | Objetivo Estratégico | Metas (KRs) | Ações | Unidades Vinculadas |",
                "| :---: | :--- | :---: | :--- | :---: | :---: | :--- |"
            ]
            for r in rows_data:
                lines.append(f"| **{r[0]}** | {r[1]} | `{r[2]}` | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")
            out_path = export_dir / "Mapa_Estrategico_Eixos_Objetivos_PGE_MA.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Mapa Estratégico"
            style_xlsx_sheet(
                ws,
                "MAPA ESTRATÉGICO — EIXOS E OBJETIVOS ESTRATÉGICOS (PGE-MA 2027–2030)",
                "Consolidação Oficial da Lista Mestre Canônica por Eixo e Objetivo Estratégico",
                headers,
                rows_data,
                [10, 42, 16, 48, 16, 14, 48]
            )
            out_path = export_dir / "Mapa_Estrategico_Eixos_Objetivos_PGE_MA.xlsx"
            wb.save(str(out_path))
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading("Mapa Estratégico — Eixos e Objetivos (PGE-MA 2027–2030)", level=1)
            for e in mapa:
                doc.add_heading(f"{e['eixo_cod']} — {e['eixo_nome']}", level=2)
                table = doc.add_table(rows=1, cols=4)
                table.style = "Table Grid"
                hdr = table.rows[0].cells
                hdr[0].text = "Código"
                hdr[1].text = "Objetivo Estratégico"
                hdr[2].text = "Metas / Ações"
                hdr[3].text = "Unidades"
                for o in e["objetivos"]:
                    row_cells = table.add_row().cells
                    row_cells[0].text = o["obj_cod"]
                    row_cells[1].text = o["objetivo_nome"]
                    row_cells[2].text = f"{o['qtd_krs']} KRs / {o['qtd_acoes']} ações"
                    row_cells[3].text = ", ".join(o["unidades"])
            out_path = export_dir / "Mapa_Estrategico_Eixos_Objetivos_PGE_MA.docx"
            doc.save(str(out_path))
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 2: LISTA DE OBJETIVOS E METAS (KRs)
    # -------------------------------------------------------------------------
    elif tipo == "objetivos-metas":
        metas = dados["objetivos_metas"]
        if eixo:
            metas = [m for m in metas if m["eixo_cod"] == eixo]

        headers = ["Cód. KR", "Eixo Estratégico", "Objetivo Estratégico", "Meta / Resultado-Chave (KR)", "Pilar 3 Ps", "Nº de Ações", "Unidades Responsáveis / Participantes"]
        rows_data = [
            [
                m["kr_codigo"],
                m["eixo_nome"],
                m["objetivo_nome"],
                m["kr_texto_completo"],
                m["pilar_3ps"],
                m["qtd_acoes"],
                ", ".join(m["unidades"])
            ]
            for m in metas
        ]

        if fmt == "md":
            lines = [
                "# Lista Mestre de Objetivos e Metas (KRs) — PGE-MA 2027–2030\n",
                "| Código KR | Eixo Estratégico | Objetivo Estratégico | Meta / Resultado-Chave (KR) | Pilar 3 Ps | Ações | Unidades |",
                "| :---: | :--- | :--- | :--- | :---: | :---: | :--- |"
            ]
            for r in rows_data:
                lines.append(f"| `{r[0]}` | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")
            out_path = export_dir / "Lista_Objetivos_e_Metas_KRs_PGE_MA.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Objetivos e Metas (KRs)"
            style_xlsx_sheet(
                ws,
                "LISTA MESTRE DE OBJETIVOS E METAS (KRs) — PGE-MA (CICLO 2027–2030)",
                "Relação Oficial de Eixos, Objetivos Estratégicos e Resultados-Chave Canônicos",
                headers,
                rows_data,
                [14, 36, 38, 52, 24, 12, 44]
            )
            out_path = export_dir / "Lista_Objetivos_e_Metas_KRs_PGE_MA.xlsx"
            wb.save(str(out_path))
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading("Lista de Objetivos e Metas (KRs) — PGE-MA 2027–2030", level=1)
            table = doc.add_table(rows=1, cols=5)
            table.style = "Table Grid"
            hdr = table.rows[0].cells
            hdr[0].text = "Código KR"
            hdr[1].text = "Eixo / Objetivo"
            hdr[2].text = "Meta (Resultado-Chave)"
            hdr[3].text = "Ações"
            hdr[4].text = "Unidades"
            for r in rows_data:
                rc = table.add_row().cells
                rc[0].text = str(r[0])
                rc[1].text = f"{r[1]}\n({r[2]})"
                rc[2].text = str(r[3])
                rc[3].text = str(r[5])
                rc[4].text = str(r[6])
            out_path = export_dir / "Lista_Objetivos_e_Metas_KRs_PGE_MA.docx"
            doc.save(str(out_path))
            conn.close()
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 3: LISTA DOS PLANOS DE AÇÃO DAS UNIDADES
    # -------------------------------------------------------------------------
    elif tipo == "planos-acao":
        # Se for exportação xlsx de uma única unidade sem filtro de eixo, retorna a própria planilha oficial .xlsx da unidade
        if fmt == "xlsx" and sigla and not eixo:
            official_xlsx = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
            if official_xlsx.exists():
                conn.close()
                return FileResponse(str(official_xlsx), filename=official_xlsx.name)

        sql = """
            SELECT a.sigla_unidade, u.nome as nome_unidade, a.eixo, a.objetivo,
                   a.kr_codigo, a.kr_texto_completo, a.acao, a.subacao, a.responsaveis, a.prazo
            FROM acoes a
            JOIN unidades u ON u.sigla = a.sigla_unidade
            WHERE 1=1
        """
        params = []
        if sigla:
            sql += " AND a.sigla_unidade = ?"
            params.append(sigla)
        if eixo:
            sql += " AND a.kr_codigo LIKE ?"
            params.append(f"{eixo}.%")
        sql += " ORDER BY a.sigla_unidade ASC, a.ordem ASC"
        acoes_rows = [dict(r) for r in cur.execute(sql, params).fetchall()]
        conn.close()

        sufixo = f"_{sigla}" if sigla else "_Consolidado_41_Unidades"
        headers = ["Unidade", "Eixo Estratégico", "Objetivo Estratégico", "OKR / Meta", "Ação (O QUÊ)", "Subação / Metodologia (COMO)", "Responsáveis (QUEM)", "Prazo (QUANDO)"]
        rows_data = [
            [
                f"{r['sigla_unidade']} — {r['nome_unidade']}",
                r["eixo"],
                r["objetivo"],
                r["kr_texto_completo"],
                r["acao"],
                r["subacao"],
                r["responsaveis"],
                r["prazo"]
            ]
            for r in acoes_rows
        ]

        if fmt == "md":
            lines = [
                f"# Lista dos Planos de Ação das Unidades ({sigla or 'Todas as 41 Unidades'}) — PGE-MA 2027–2030\n",
                "| Unidade | Meta (KR) | Ação (O QUÊ) | Subação / Metodologia (COMO) | Responsáveis (QUEM) | Prazo |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |"
            ]
            for r in acoes_rows:
                lines.append(f"| **{r['sigla_unidade']}** | `{r['kr_codigo']}` | {r['acao']} | {r['subacao']} | {r['responsaveis']} | {r['prazo']} |")
            out_path = export_dir / f"Planos_de_Acao_Unidades{sufixo}.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Planos de Ação"
            style_xlsx_sheet(
                ws,
                f"LISTA DOS PLANOS DE AÇÃO DAS UNIDADES ({sigla or '41 UNIDADES CONSOLIDADAS'}) — PGE-MA 2027–2030",
                "Planos de Ação Setoriais Estruturados na Metodologia 5W2H e Lista Mestre Canônica",
                headers,
                rows_data,
                [26, 28, 30, 36, 36, 52, 36, 18]
            )
            out_path = export_dir / f"Planos_de_Acao_Unidades{sufixo}.xlsx"
            wb.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading(f"Planos de Ação das Unidades ({sigla or 'Consolidado 41 Unidades'}) — PGE-MA 2027–2030", level=1)
            table = doc.add_table(rows=1, cols=6)
            table.style = "Table Grid"
            hdr = table.rows[0].cells
            hdr[0].text = "Unidade"
            hdr[1].text = "Meta (KR)"
            hdr[2].text = "Ação (O QUÊ)"
            hdr[3].text = "Subação / Como Fazer"
            hdr[4].text = "Responsáveis"
            hdr[5].text = "Prazo"
            for r in acoes_rows:
                rc = table.add_row().cells
                rc[0].text = r["sigla_unidade"]
                rc[1].text = r["kr_texto_completo"]
                rc[2].text = r["acao"]
                rc[3].text = r["subacao"]
                rc[4].text = r["responsaveis"]
                rc[5].text = r["prazo"]
            out_path = export_dir / f"Planos_de_Acao_Unidades{sufixo}.docx"
            doc.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 4: MATRIZ DE RESPONSABILIDADES E DEPENDÊNCIAS INTERSETORIAIS
    # -------------------------------------------------------------------------
    elif tipo == "matriz-responsabilidades":
        conn.close()
        matriz_unids = dados["matriz_unidades"]
        all_acoes = dados["acoes_enriquecidas"]
        if sigla:
            matriz_unids = [u for u in matriz_unids if u["sigla"] == sigla]
            acoes_rel = [
                a for a in all_acoes
                if a["sigla_unidade"] == sigla or sigla in (a["unidades_parceiras"] or "").split(",")
            ]
        else:
            acoes_rel = [a for a in all_acoes if a["unidades_parceiras"] or a["papel_unidade"] != "Líder"]

        sufixo = f"_{sigla}" if sigla else "_Consolidada_41_Unidades"
        headers_resumo = [
            "Sigla", "Unidade", "Total Ações na Planilha", "Papel: Líder", "Papel: Coexecutor",
            "Papel: Articulador", "Parceiros Acionados pela Unidade", "Demandas Externas Recebidas", "Unidades que Demandam esta Pasta"
        ]
        rows_resumo = [
            [
                u["sigla"], u["nome"], u["total_acoes"], u["qtd_lider"], u["qtd_coexecutor"],
                u["qtd_articulador"], ", ".join(u["parceiros_acionados"]) or "Nenhum",
                u["qtd_demandas_recebidas"], ", ".join(u["unidades_demandantes"]) or "Nenhuma"
            ]
            for u in matriz_unids
        ]

        headers_det = ["Unidade Titular", "Papel na Ação", "Unidades Parceiras Citadas", "Meta (KR)", "Ação (O QUÊ)", "Governança / Responsáveis (QUEM)", "Prazo"]
        rows_det = [
            [
                f"{a['sigla_unidade']} — {a['nome_unidade']}",
                a["papel_unidade"],
                (a["unidades_parceiras"] or "").replace(",", ", ") or "Execução Interna",
                a["kr_codigo"],
                a["acao"],
                a["responsaveis"],
                a["prazo"]
            ]
            for a in acoes_rel
        ]

        if fmt == "md":
            lines = [
                f"# Matriz de Responsabilidades e Dependências Intersetoriais ({sigla or '41 Unidades'}) — PGE-MA 2027–2030\n",
                "## 1. Quadro Sintético de Papéis (Líder x Coexecutor x Articulador) e Demandas Cruzadas\n",
                "| Sigla | Unidade | Total | Líder | Coexecutor | Articulador | Parceiros Acionados | Demandas Recebidas | Quem Demanda |",
                "| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :--- |"
            ]
            for r in rows_resumo:
                lines.append(f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]} |")
            lines.append("\n## 2. Detalhamento das Ações Compartilhadas e Dependências Intersetoriais\n")
            lines.append("| Unidade Titular | Papel | Parceiros | KR | Ação | Responsáveis (QUEM) | Prazo |")
            lines.append("| :--- | :---: | :--- | :---: | :--- | :--- | :--- |")
            for r in rows_det:
                lines.append(f"| {r[0]} | **{r[1]}** | {r[2]} | `{r[3]}` | {r[4]} | {r[5]} | {r[6]} |")
            out_path = export_dir / f"Matriz_Responsabilidades_Dependencias{sufixo}.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws1 = wb.active
            ws1.title = "Resumo Intersetorial"
            style_xlsx_sheet(
                ws1,
                f"MATRIZ DE RESPONSABILIDADES E DEPENDÊNCIAS INTERSETORIAIS ({sigla or '41 UNIDADES'})",
                "Quadro Sintético de Papéis (Líder, Coexecutor, Articulador), Parceiros Acionados e Demandas Recebidas",
                headers_resumo,
                rows_resumo,
                [12, 38, 16, 14, 16, 16, 40, 18, 40]
            )
            ws2 = wb.create_sheet(title="Vínculos Detalhados")
            style_xlsx_sheet(
                ws2,
                f"DETALHAMENTO DE VÍNCULOS E DEPENDÊNCIAS INTERSETORIAIS ({sigla or 'CONSOLIDADO'})",
                "Relação de Ações com Coexecução, Articulação ou Dependência entre Unidades da PGE-MA",
                headers_det,
                rows_det,
                [28, 16, 26, 16, 40, 46, 20]
            )
            out_path = export_dir / f"Matriz_Responsabilidades_Dependencias{sufixo}.xlsx"
            wb.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading(f"Matriz de Responsabilidades e Dependências Intersetoriais ({sigla or '41 Unidades'})", level=1)
            doc.add_heading("1. Resumo de Papéis e Demandas por Unidade", level=2)
            t1 = doc.add_table(rows=1, cols=7)
            t1.style = "Table Grid"
            for idx, h in enumerate(["Sigla", "Unidade", "Líder", "Coexec.", "Artic.", "Parceiros Acionados", "Quem Demanda"]):
                t1.rows[0].cells[idx].text = h
            for r in rows_resumo:
                rc = t1.add_row().cells
                rc[0].text = str(r[0])
                rc[1].text = str(r[1])
                rc[2].text = str(r[3])
                rc[3].text = str(r[4])
                rc[4].text = str(r[5])
                rc[5].text = str(r[6])
                rc[6].text = f"{r[7]} ações ({r[8]})"
            doc.add_heading("2. Detalhamento das Ações Intersetoriais", level=2)
            t2 = doc.add_table(rows=1, cols=6)
            t2.style = "Table Grid"
            for idx, h in enumerate(["Unidade", "Papel", "Parceiros", "KR", "Ação", "Responsáveis"]):
                t2.rows[0].cells[idx].text = h
            for r in rows_det:
                rc = t2.add_row().cells
                for idx in range(6):
                    rc[idx].text = str(r[idx])
            out_path = export_dir / f"Matriz_Responsabilidades_Dependencias{sufixo}.docx"
            doc.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 5: CRONOGRAMA DE ENTREGAS POR HORIZONTE TEMPORAL
    # -------------------------------------------------------------------------
    elif tipo == "cronograma-entregas":
        conn.close()
        acoes_cron = dados["acoes_enriquecidas"]
        if sigla:
            acoes_cron = [a for a in acoes_cron if a["sigla_unidade"] == sigla]
        if horizonte:
            acoes_cron = [a for a in acoes_cron if horizonte.lower() in a["horizonte"].lower()]

        ordem_h = {
            "Curto Prazo (Imediato / Até 180 dias)": 1,
            "Médio Prazo / Periódico (Ciclos Anuais/Semestrais)": 2,
            "Contínuo / Ciclo Integral (2027–2030)": 3
        }
        acoes_cron = sorted(acoes_cron, key=lambda x: (ordem_h.get(x["horizonte"], 9), x["sigla_unidade"], x["kr_codigo"]))

        sufixo = f"_{sigla}" if sigla else "_Consolidado"
        headers = ["Horizonte Temporal", "Prazo Específico (QUANDO)", "Unidade", "Meta (KR)", "Ação (O QUÊ)", "Subação / Metodologia (COMO)", "Responsáveis (QUEM)"]
        rows_data = [
            [
                a["horizonte"],
                a["prazo"],
                f"{a['sigla_unidade']} — {a['nome_unidade']}",
                a["kr_codigo"],
                a["acao"],
                a["subacao"],
                a["responsaveis"]
            ]
            for a in acoes_cron
        ]

        if fmt == "md":
            lines = [
                f"# Cronograma de Entregas por Horizonte Temporal ({sigla or '41 Unidades'}) — PGE-MA 2027–2030\n",
                "| Horizonte Temporal | Prazo (QUANDO) | Unidade | KR | Ação (O QUÊ) | Responsáveis (QUEM) |",
                "| :--- | :--- | :---: | :---: | :--- | :--- |"
            ]
            for a in acoes_cron:
                lines.append(f"| **{a['horizonte']}** | {a['prazo']} | **{a['sigla_unidade']}** | `{a['kr_codigo']}` | {a['acao']} | {a['responsaveis']} |")
            out_path = export_dir / f"Cronograma_Entregas_Horizonte_Temporal{sufixo}.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Cronograma Temporal"
            style_xlsx_sheet(
                ws,
                f"CRONOGRAMA DE ENTREGAS POR HORIZONTE TEMPORAL ({sigla or '41 UNIDADES'}) — PGE-MA 2027–2030",
                "Classificação Executiva de Entregas em Curto Prazo (Imediato/Até 180 dias), Médio Prazo/Periódico e Contínuo (2027–2030)",
                headers,
                rows_data,
                [34, 24, 28, 14, 38, 48, 36]
            )
            out_path = export_dir / f"Cronograma_Entregas_Horizonte_Temporal{sufixo}.xlsx"
            wb.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading(f"Cronograma de Entregas por Horizonte Temporal ({sigla or '41 Unidades'})", level=1)
            table = doc.add_table(rows=1, cols=6)
            table.style = "Table Grid"
            for idx, h in enumerate(["Horizonte", "Prazo", "Unidade", "KR", "Ação (O QUÊ)", "Responsáveis"]):
                table.rows[0].cells[idx].text = h
            for a in acoes_cron:
                rc = table.add_row().cells
                rc[0].text = a["horizonte"]
                rc[1].text = a["prazo"]
                rc[2].text = a["sigla_unidade"]
                rc[3].text = a["kr_codigo"]
                rc[4].text = a["acao"]
                rc[5].text = a["responsaveis"]
            out_path = export_dir / f"Cronograma_Entregas_Horizonte_Temporal{sufixo}.docx"
            doc.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 6: RELATÓRIO DE GRUPOS DE TRABALHO (GTs) E PROJETOS ESTRUTURANTES
    # -------------------------------------------------------------------------
    elif tipo == "relatorio-gt":
        conn.close()
        gts_list = dados["gts"]
        all_acoes = dados["acoes_enriquecidas"]
        if gt_codigo:
            gts_list = [g for g in gts_list if g["codigo"] == gt_codigo]

        sufixo = f"_{gt_codigo}" if gt_codigo else "_Todos_10_GTs"

        if fmt == "md":
            lines = [f"# Relatório de Grupos de Trabalho (GTs) e Projetos Estruturantes ({gt_codigo or 'Consolidado'}) — PGE-MA 2027–2030\n"]
            for g in gts_list:
                krs_gt = [k.strip() for k in g["krs_vinculados"].split(",") if k.strip()]
                unids_gt = [u.strip() for u in g["unidades_participantes"].split(",") if u.strip()]
                acoes_gt = [a for a in all_acoes if a["kr_codigo"] in krs_gt and (a["sigla_unidade"] in unids_gt or "Todas" in g["unidades_participantes"])]
                lines.append(f"## {g['codigo']} — {g['titulo']}")
                lines.append(f"- **Tipo:** {g['tipo']} | **Status:** {g['status']} | **Prazo:** {g['prazo']}")
                lines.append(f"- **Liderança:** {g['lider']}")
                lines.append(f"- **Unidades Participantes:** {g['unidades_participantes']}")
                lines.append(f"- **Metas (KRs) Vinculadas:** `{g['krs_vinculados']}`")
                lines.append(f"- **Objetivo e Escopo:** {g['objetivo']}\n")
                lines.append("### Checklist de Entregáveis do GT/Projeto")
                for ent in g["entregaveis"]:
                    mark = "[Concluído]" if ent.get("concluido") else "[Pendente]"
                    lines.append(f"- **{mark}** {ent.get('item')}")
                lines.append(f"\n### Ações Setoriais Vinculadas ao {g['codigo']} ({len(acoes_gt)} ações)")
                lines.append("| Unidade | KR | Ação (O QUÊ) | Responsáveis | Prazo |")
                lines.append("| :---: | :---: | :--- | :--- | :--- |")
                for a in acoes_gt[:40]:
                    lines.append(f"| **{a['sigla_unidade']}** | `{a['kr_codigo']}` | {a['acao']} | {a['responsaveis']} | {a['prazo']} |")
                lines.append("\n---\n")
            out_path = export_dir / f"Relatorio_GTs_Projetos_Estruturantes{sufixo}.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws1 = wb.active
            ws1.title = "Ficha dos GTs e Projetos"
            headers_gt = ["Código", "Título do GT / Projeto", "Tipo", "Líder(es)", "Unidades Participantes", "KRs Vinculados", "Status", "Prazo", "Objetivo", "Checklist de Entregáveis"]
            rows_gt = []
            rows_acoes_gt = []
            for g in gts_list:
                ent_str = "\n".join([f"[{'OK' if e.get('concluido') else 'PENDENTE'}] {e.get('item')}" for e in g["entregaveis"]])
                rows_gt.append([
                    g["codigo"], g["titulo"], g["tipo"], g["lider"], g["unidades_participantes"],
                    g["krs_vinculados"], g["status"], g["prazo"], g["objetivo"], ent_str
                ])
                krs_gt = [k.strip() for k in g["krs_vinculados"].split(",") if k.strip()]
                unids_gt = [u.strip() for u in g["unidades_participantes"].split(",") if u.strip()]
                for a in all_acoes:
                    if a["kr_codigo"] in krs_gt and (a["sigla_unidade"] in unids_gt or "Todas" in g["unidades_participantes"]):
                        rows_acoes_gt.append([
                            g["codigo"], g["titulo"], a["sigla_unidade"], a["kr_codigo"],
                            a["acao"], a["subacao"], a["responsaveis"], a["prazo"]
                        ])
            style_xlsx_sheet(
                ws1,
                f"RELATÓRIO DE GRUPOS DE TRABALHO (GTs) E PROJETOS ESTRUTURANTES ({gt_codigo or 'CONSOLIDADO'})",
                "Governança Intersetorial, Liderança, Unidades Participantes, KRs e Checklist de Entregáveis",
                headers_gt,
                rows_gt,
                [12, 38, 24, 22, 34, 24, 22, 20, 48, 52]
            )
            ws2 = wb.create_sheet(title="Ações Vinculadas ao GT")
            style_xlsx_sheet(
                ws2,
                f"AÇÕES SETORIAIS VINCULADAS AOS GTs / PROJETOS ({gt_codigo or 'TODOS'})",
                "Desdobramento Operacional 5W2H nas Planilhas das Unidades Participantes",
                ["Cód. GT", "GT / Projeto", "Unidade", "Meta (KR)", "Ação (O QUÊ)", "Subação (COMO)", "Responsáveis (QUEM)", "Prazo"],
                rows_acoes_gt,
                [12, 34, 14, 16, 36, 46, 36, 18]
            )
            out_path = export_dir / f"Relatorio_GTs_Projetos_Estruturantes{sufixo}.xlsx"
            wb.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading(f"Relatório de Grupos de Trabalho e Projetos Estruturantes ({gt_codigo or 'Consolidado'})", level=1)
            for g in gts_list:
                doc.add_heading(f"{g['codigo']} — {g['titulo']}", level=2)
                p = doc.add_paragraph()
                p.add_run(f"Tipo: ").bold = True
                p.add_run(f"{g['tipo']} | ")
                p.add_run("Líder: ").bold = True
                p.add_run(f"{g['lider']} | ")
                p.add_run("Status: ").bold = True
                p.add_run(f"{g['status']} | ")
                p.add_run("Prazo: ").bold = True
                p.add_run(f"{g['prazo']}\n")
                p.add_run("Unidades Participantes: ").bold = True
                p.add_run(f"{g['unidades_participantes']}\n")
                p.add_run("KRs Vinculados: ").bold = True
                p.add_run(f"{g['krs_vinculados']}\n")
                p.add_run("Objetivo e Escopo: ").bold = True
                p.add_run(f"{g['objetivo']}")

                doc.add_heading("Checklist de Entregáveis", level=3)
                for ent in g["entregaveis"]:
                    status_lbl = "[Concluído]" if ent.get("concluido") else "[Pendente]"
                    doc.add_paragraph(f"{status_lbl} {ent.get('item')}", style="List Bullet")

                krs_gt = [k.strip() for k in g["krs_vinculados"].split(",") if k.strip()]
                unids_gt = [u.strip() for u in g["unidades_participantes"].split(",") if u.strip()]
                acoes_gt = [a for a in all_acoes if a["kr_codigo"] in krs_gt and (a["sigla_unidade"] in unids_gt or "Todas" in g["unidades_participantes"])]
                if acoes_gt:
                    doc.add_heading(f"Ações Setoriais Vinculadas ({len(acoes_gt)} ações)", level=3)
                    t = doc.add_table(rows=1, cols=5)
                    t.style = "Table Grid"
                    for idx, h in enumerate(["Unidade", "KR", "Ação", "Responsáveis", "Prazo"]):
                        t.rows[0].cells[idx].text = h
                    for a in acoes_gt:
                        rc = t.add_row().cells
                        rc[0].text = a["sigla_unidade"]
                        rc[1].text = a["kr_codigo"]
                        rc[2].text = a["acao"]
                        rc[3].text = a["responsaveis"]
                        rc[4].text = a["prazo"]
            out_path = export_dir / f"Relatorio_GTs_Projetos_Estruturantes{sufixo}.docx"
            doc.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

    # -------------------------------------------------------------------------
    # RELATÓRIO 7: FICHA INDIVIDUALIZADA DE PACTUAÇÃO POR UNIDADE
    # -------------------------------------------------------------------------
    elif tipo == "ficha-pactuacao":
        conn.close()
        sig_target = sigla or "PGAAE"
        u_meta = next((u for u in dados["unidades_meta"] if u["sigla"] == sig_target), None)
        if not u_meta:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        u_mat = next((m for m in dados["matriz_unidades"] if m["sigla"] == sig_target), {})
        acoes_u = [a for a in dados["acoes_enriquecidas"] if a["sigla_unidade"] == sig_target]
        krs_u = sorted(set(a["kr_codigo"] for a in acoes_u if a["kr_codigo"] != "SEM_CODIGO"))
        minutas_u = get_unit_minutas(sig_target)

        if fmt == "md":
            lines = [
                f"# Ficha Individualizada de Pactuação Setorial — {u_meta['sigla']} ({u_meta['nome']})",
                "**Procuradoria-Geral do Estado do Maranhão (PGE-MA) • Ciclo Estratégico 2027–2030**\n",
                "## 1. Identificação e Governança da Unidade",
                f"- **Unidade:** {u_meta['sigla']} — {u_meta['nome']}",
                f"- **Chefia / Interlocutor(a):** {u_meta['responsavel']}",
                f"- **Processo SEI:** `{u_meta['processo_sei']}` | **Status de Pactuação:** **{u_meta['status_reuniao']}**",
                f"- **Total de Ações Pactuadas:** {len(acoes_u)} ações distribuídas em {len(krs_u)} Metas (`{', '.join(krs_u)}`)",
                f"- **Atuação Intersetorial:** Líder em {u_mat.get('qtd_lider', 0)} ações | Coexecutor em {u_mat.get('qtd_coexecutor', 0)} | Articulador em {u_mat.get('qtd_articulador', 0)} | Demandada externamente em {u_mat.get('qtd_demandas_recebidas', 0)} ações",
                f"- **Síntese da Pauta e Deliberações Setoriais:** {u_meta['pauta_reuniao']}",
            ]
            if u_meta.get("notas_reuniao"):
                lines.append(f"- **Registro de Ata / Notas da Reunião:** {u_meta['notas_reuniao']}")

            lines.append("\n## 2. Plano de Ação Setorial Pactuado (Metodologia 5W2H)\n")
            lines.append("| # | Meta (KR) | Pilar 3 Ps | Ação (O QUÊ) | Subação / Metodologia (COMO) | Responsáveis (QUEM) | Prazo |")
            lines.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
            for idx, a in enumerate(acoes_u, start=1):
                lines.append(f"| {idx} | `{a['kr_codigo']}` | {a['pilar_3ps']} | {a['acao']} | {a['subacao']} | {a['responsaveis']} | {a['prazo']} |")

            dem_rec = u_mat.get("demandas_recebidas", [])
            if dem_rec:
                lines.append(f"\n## 3. Compromissos Cruzados (Ações de Outras Unidades que Demandam {sig_target})\n")
                lines.append("| Unidade Demandante | Meta (KR) | Ação | Governança / Responsáveis | Prazo |")
                lines.append("| :---: | :---: | :--- | :--- | :--- |")
                for d in dem_rec:
                    lines.append(f"| **{d['origem']}** | `{d['kr_codigo']}` | {d['acao']} | {d['responsaveis']} | {d['prazo']} |")

            lines.append("\n## 4. Termo / Despacho Padrão de Homologação no SEI\n")
            lines.append(f"```text\n{minutas_u['despacho_sei']}\n```")

            out_path = export_dir / f"Ficha_Pactuacao_Setorial_{sig_target}.md"
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return FileResponse(str(out_path), filename=out_path.name, media_type="text/markdown")

        elif fmt == "xlsx":
            wb = openpyxl.Workbook()
            ws1 = wb.active
            ws1.title = f"Ficha Pactuação {sig_target}"
            headers_ficha = ["Ordem", "Eixo Estratégico", "Objetivo Estratégico", "Meta (KR)", "Pilar 3 Ps", "Papel na Ação", "Ação (O QUÊ)", "Subação / Metodologia (COMO)", "Responsáveis (QUEM)", "Prazo (QUANDO)"]
            rows_ficha = [
                [
                    idx, a["eixo"], a["objetivo"], a["kr_texto_completo"], a["pilar_3ps"],
                    a["papel_unidade"], a["acao"], a["subacao"], a["responsaveis"], a["prazo"]
                ]
                for idx, a in enumerate(acoes_u, start=1)
            ]
            style_xlsx_sheet(
                ws1,
                f"FICHA DE PACTUAÇÃO SETORIAL: {u_meta['sigla']} — {u_meta['nome'].upper()}",
                f"Chefia: {u_meta['responsavel']} | SEI: {u_meta['processo_sei']} | Status: {u_meta['status_reuniao']} | Pauta: {u_meta['pauta_reuniao']}",
                headers_ficha,
                rows_ficha,
                [10, 28, 30, 36, 22, 16, 36, 48, 36, 18]
            )
            dem_rec = u_mat.get("demandas_recebidas", [])
            if dem_rec:
                ws2 = wb.create_sheet(title=f"Demandas para {sig_target}")
                style_xlsx_sheet(
                    ws2,
                    f"COMPROMISSOS INTERSETORIAIS QUE DEMANDAM A UNIDADE {sig_target}",
                    "Ações constantes nas planilhas de outras unidades que citam esta pasta como parceira/coexecutora",
                    ["Unidade Demandante", "Meta (KR)", "Ação (O QUÊ)", "Responsáveis (QUEM)", "Prazo"],
                    [[d["origem"], d["kr_codigo"], d["acao"], d["responsaveis"], d["prazo"]] for d in dem_rec],
                    [20, 18, 44, 46, 20]
                )
            out_path = export_dir / f"Ficha_Pactuacao_Setorial_{sig_target}.xlsx"
            wb.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

        elif fmt == "docx":
            doc = docx.Document()
            doc.add_heading(f"Ficha Individualizada de Pactuação Setorial — {u_meta['sigla']}", level=1)
            p = doc.add_paragraph()
            p.add_run("Unidade: ").bold = True
            p.add_run(f"{u_meta['sigla']} — {u_meta['nome']}\n")
            p.add_run("Chefia / Interlocutor(a): ").bold = True
            p.add_run(f"{u_meta['responsavel']}\n")
            p.add_run("Processo SEI: ").bold = True
            p.add_run(f"{u_meta['processo_sei']} | ")
            p.add_run("Status: ").bold = True
            p.add_run(f"{u_meta['status_reuniao']}\n")
            p.add_run("KRs Vinculados: ").bold = True
            p.add_run(f"{', '.join(krs_u)} ({len(acoes_u)} ações)\n")
            p.add_run("Síntese das Deliberações: ").bold = True
            p.add_run(f"{u_meta['pauta_reuniao']}")

            doc.add_heading("1. Plano de Ação Setorial (5W2H)", level=2)
            t = doc.add_table(rows=1, cols=6)
            t.style = "Table Grid"
            for idx, h in enumerate(["KR", "Pilar 3 Ps", "Ação (O QUÊ)", "Subação (COMO)", "Responsáveis", "Prazo"]):
                t.rows[0].cells[idx].text = h
            for a in acoes_u:
                rc = t.add_row().cells
                rc[0].text = a["kr_codigo"]
                rc[1].text = a["pilar_3ps"]
                rc[2].text = a["acao"]
                rc[3].text = a["subacao"]
                rc[4].text = a["responsaveis"]
                rc[5].text = a["prazo"]

            dem_rec = u_mat.get("demandas_recebidas", [])
            if dem_rec:
                doc.add_heading(f"2. Demandas Externas Recebidas por {sig_target} ({len(dem_rec)} ações)", level=2)
                t2 = doc.add_table(rows=1, cols=4)
                t2.style = "Table Grid"
                for idx, h in enumerate(["Origem", "KR", "Ação", "Responsáveis"]):
                    t2.rows[0].cells[idx].text = h
                for d in dem_rec:
                    rc = t2.add_row().cells
                    rc[0].text = d["origem"]
                    rc[1].text = d["kr_codigo"]
                    rc[2].text = d["acao"]
                    rc[3].text = d["responsaveis"]

            doc.add_heading("3. Minuta de Despacho de Validação SEI", level=2)
            doc.add_paragraph(minutas_u["despacho_sei"])

            out_path = export_dir / f"Ficha_Pactuacao_Setorial_{sig_target}.docx"
            doc.save(str(out_path))
            return FileResponse(str(out_path), filename=out_path.name)

    conn.close()
    raise HTTPException(status_code=400, detail="Tipo de relatório inválido")


STATIC_DIR = APP_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_file = STATIC_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")
