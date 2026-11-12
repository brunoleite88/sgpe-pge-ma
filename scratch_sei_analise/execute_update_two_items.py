import sqlite3
import sys
sys.path.insert(0, '.')
from sgpe_app.backend import sync_unit_to_xlsx

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# =========================================================================
# ITEM 1: REGRA D-3 (SEI 2026.11103.08358) NOS PRAZOS PROCESSUAIS (E5.O6.KR1)
# =========================================================================

# 1. SGA - Normatização e Auditoria MNI
c.execute("""
    UPDATE acoes 
    SET acao = 'Instituir o Programa Institucional de Prevenção de Perda de Prazos e a Diretriz Operacional D-3 (SEI 2026.11103.08358)',
        subacao = 'Coordenar ato normativo corporativo transversal fixando a Diretriz Operacional Vinculante D-3 (protocolo de manifestações judiciais com antecedência mínima de 3 dias úteis do limite do SPA - Processo SEI 2026.11103.08358), redesenhar fluxos no SPA, aprimorar a governança da fila de expedientes e instituir selos de qualidade e conformidade.'
    WHERE id = 13497
""")

c.execute("""
    UPDATE acoes 
    SET acao = 'Saneamento e checagem cruzada dos sistemas de protocolo (SPA x PJe) e auditoria MNI/TJMA',
        subacao = 'Atuar junto à Assessoria em TIC da PGAAE / INOVA e SI para auditar nós de integração do MNI junto ao TJMA (Chamado TJMA nº 233881), mitigar delays de captura do PJe para o SPA, registrar indisponibilidades e redistribuir divergências de leitura de ciência em processos SEI específicos.'
    WHERE id = 13498
""")

# 2. PGAAE - Barramento SPA e Alertas D-3
c.execute("""
    UPDATE acoes 
    SET acao = 'Sanear o barramento do SPA e auditar nós do MNI com o TJMA (Chamado TJMA nº 233881)',
        subacao = 'Executar calibração técnica no barramento MNI do SPA junto à TI do TJMA para harmonizar regras de negócio e contagem de prazos, sanar o atraso de 5 a 7 dias úteis e instituir alertas preventivos do regime D-3 (SEI nº 2026.11103.08358).'
    WHERE id = 13181
""")

c.execute("""
    UPDATE acoes 
    SET acao = 'Implantar notificação diária de intimações, divergências e conformidade D-3',
        subacao = 'Configurar rotina automatizada de alertas preventivos sobre inconsistências na leitura de ciência do MNI, monitorando e sinalizando o cumprimento das manifestações judiciais no regime D-3 (SEI nº 2026.11103.08358).'
    WHERE id = 13182
""")

# 3. PJ - Diretriz D-3
c.execute("""
    UPDATE acoes 
    SET acao = 'Implantar diretriz obrigatória de protocolo antecipado em regime D-3 (SEI nº 2026.11103.08358)',
        subacao = 'Fixar diretriz interna vinculante para que contestações e recursos sejam protocolados no PJe com pelo menos 3 dias úteis de antecedência (regime D-3) em relação ao prazo fatal do SPA, blindando a PGE contra preclusão por divergências entre sistemas decorrentes do MNI.'
    WHERE id = 13275
""")

# 4. SDD - Triagem e tratamento de divergências
c.execute("""
    UPDATE acoes 
    SET acao = 'Implantar rotina de identificação e tratamento de divergências de prazos e triagem D-3',
        subacao = 'Confrontar registros do PJe, Domicílio Judicial Eletrônico e SPA; classificar divergências de leitura de ciência do MNI; apoiar a triagem no regime D-3 (SEI 2026.11103.08358) e acionar suporte/TJMA para apuração técnica mantendo rastreabilidade.'
    WHERE id = 13483
""")

# 5. Especializadas Finalísticas - Cumprimento D-3 na conferência diária
especializadas_updates = {
    12803: "Instituir checagem diária dos expedientes em aberto no SPA e PJe, operando no regime de segurança D-3 (protocolo com antecedência mínima de 3 dias úteis do limite do SPA - SEI 2026.11103.08358) e escalonamento imediato à chefia.", # PA
    12859: "Realizar dupla checagem das intimações judiciais disponibilizadas nos sistemas dos Tribunais, assegurando a tempestividade de contestações, apelações e agravos com cumprimento no regime D-3 (SEI 2026.11103.08358).", # PCF
    12914: "Criar rotina de verificação diária de expedientes pendentes com travas de segurança, cumprimento no regime D-3 (SEI 2026.11103.08358) e alertas escalonados de vencimento à chefia.", # PDA
    12939: "Executar conferência diária SPA–PJe com observância obrigatória à diretriz operacional D-3 (cumprimento 3 dias úteis antes do limite do SPA - SEI 2026.11103.08358), mantendo alertas preventivos e validação da chefia.", # PEDU
    12968: "Criar rotina diária em agenda/caixa de processos do procurador e supervisão imediata pela chefia para garantir cumprimento tempestivo de todos os prazos em regime D-3 (SEI 2026.11103.08358).", # PERJP
    13291: "Estabelecer protocolo diário de verificação de pendências críticas no painel do SPA e no PJe com foco no regime D-3 (SEI 2026.11103.08358), documentando ocorrências de lentidão e alinhando com a PGAAE/INOVA comunicados prévios a alterações no sistema.", # PJEFP
    13313: "Implantar conferência diária cruzada de prazos processuais com protocolo prioritário em regime D-3 (SEI 2026.11103.08358) e instituir escala obrigatória de redistribuição de carteiras em afastamentos.", # PPIMA
    13352: "Criar rotina diária em agenda/caixa de processos do procurador e supervisão imediata pela chefia, assegurando protocolo das manifestações com margem de segurança D-3 (SEI 2026.11103.08358).", # PRI
    13388: "Criar rotina diária em agenda/caixa de processos do procurador e supervisão imediata pela chefia, assegurando protocolo das manifestações com margem de segurança D-3 (SEI 2026.11103.08358).", # PRT
    13399: "Realizar batimento diário obrigatório entre as intimações do PJe e os lançamentos do SPA, operando em regime de protocolo antecipado D-3 (SEI 2026.11103.08358) para assegurar que nenhum prazo judicial seja precluso por falhas de integração.", # PSAU
    13419: "Administrativos conferem diariamente intimações nos sistemas; operacionalizar fluxo no regime D-3 (cumprimento com antecedência mínima de 3 dias úteis do limite do SPA - SEI 2026.11103.08358), com alertas escalonados e procurador validando atos privativos.", # PSP
    13450: "Realizar conferência diária entre o sistema corporativo e o painel eletrônico do TRT16 (1º e 2º graus), aplicando a diretriz D-3 (SEI 2026.11103.08358) para neutralizar os efeitos do delay de 5 a 7 dias entre SPA e PJe.", # PT
    12738: "Executar rotina matinal e vespertina de conferência direta nos painéis do PJe e do SPA sobre expedientes distribuídos, operando no regime de segurança D-3 (SEI 2026.11103.08358) para blindagem contra inconsistências sistêmicas.", # NCIA
}

for aid, sub in especializadas_updates.items():
    c.execute("UPDATE acoes SET subacao = ? WHERE id = ?", (sub, aid))

# =========================================================================
# ITEM 2: TRANSIÇÃO VXRAIL / NUTANIX & PROTOCOLO DE CRISE 3 NÍVEIS (E7.O2.KR2)
# =========================================================================

# 1. SI (Supervisão de Informática)
c.execute("""
    UPDATE acoes 
    SET acao = 'Manter a soberania do Data Center, contingência do SPA e gestão da transição de hiperconvergência (SEI 2026.11103.06878)',
        subacao = 'Executar o Plano de Contingência do SPA (SEI nº 2026.11103.06878); gerir a transição da infraestrutura de hiperconvergência legada (Dell VxRail/VMware) para Nutanix HCI via PROFISCO III e Estudo de Alternativas Tecnológicas (EAT); manter redundância na Sala Cofre da ATI e observabilidade contínua por Zabbix; fiscalizar rigidamente os SLAs da COREPLAN (Contrato nº 25/2023) e vedar a absorção indevida de sistemas externos.'
    WHERE id = 13571
""")

c.execute("""
    UPDATE acoes 
    SET acao = 'Instituir testes práticos de contingência e o Protocolo de Crise de TIC em 3 Níveis Operacionais',
        subacao = 'Realizar simulações periódicas semestrais de Disaster Recovery (RTO/RPO); operar o fluxo de resposta a incidentes de TIC em 3 níveis operacionais (Nível 1 - Controlável; Nível 2 - Relevante; Nível 3 - Crise Crítica), com alertas Zabbix, ativação de ambiente redundante na Sala Cofre da ATI em caso de desastre e reporte direto ao Comitê de Crise e ao Gabinete do PGE.'
    WHERE id = 13577
""")

# 2. PGAAE (Procuradoria Geral Adjunta para Assuntos Estratégicos)
c.execute("""
    UPDATE acoes 
    SET acao = 'Projetar arquitetura de contingência do SPA, observabilidade Zabbix e transição de hiperconvergência',
        subacao = 'Normatizar a política de contingência do SPA (Processo SEI nº 2026.11103.06878), arquitetura de observabilidade ativa (Zabbix), redundância na Sala Cofre da ATI, transição da hiperconvergência legada Dell VxRail para Nutanix HCI e governança técnica sobre contratos de sustentação (COREPLAN).'
    WHERE id = 13210
""")

c.execute("""
    UPDATE acoes 
    SET acao = 'Instituir calendário de testes de contingência e o Protocolo de Crise Institucional em 3 Níveis',
        subacao = 'Formalizar por portaria o rito de resposta a crises em 3 níveis operacionais (Incidente Controlável, Incidente Relevante e Crise Institucional Crítica), integrando o Comitê de Governança de TIC e o Comitê de Crise sob coordenação da PGAAE com reporte direto ao Procurador-Geral do Estado.'
    WHERE id = 13213
""")

conn.commit()
print("Banco SQLite atualizado com sucesso!")

# Lista de unidades afetadas para sincronizar planilhas XLSX
unidades_afetadas = sorted(list(set([
    'SGA', 'PGAAE', 'PJ', 'SDD', 'PA', 'PCF', 'PDA', 'PEDU', 
    'PERJP', 'PJEFP', 'PPIMA', 'PRI', 'PRT', 'PSAU', 'PSP', 'PT', 'NCIA', 'SI'
])))

print(f"\nSincronizando planilhas XLSX para {len(unidades_afetadas)} unidades...")
for sigla in unidades_afetadas:
    sync_unit_to_xlsx(sigla)
    print(f"  [OK] Planilhas sincronizadas: {sigla}")

print("\nTodas as planilhas e base de dados foram atualizadas com sucesso!")
conn.close()
