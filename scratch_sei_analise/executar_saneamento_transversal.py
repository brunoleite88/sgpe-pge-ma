# -*- coding: utf-8 -*-
"""
Script de Saneamento Transversal da Metodologia do SGPE PGE-MA
Aplica as diretrizes acordadas:
1. CS assume liderança exclusiva de E9.O3.KR1 (Honorários). As outras 14 unidades tornam-se Fornecedor de Insumo/Apoio.
2. ASCOM assume liderança exclusiva de E6.O1.KR2 (Redes Sociais). As 15 unidades tornam-se Fornecedor de Insumo.
3. PGAAE assume liderança de E7.O3.KR1 (Projetos Estratégicos). As 16 unidades tornam-se Apoio / Usuário Piloto.
4. PGAAJ e PB assumem liderança de E5.O2.KR2 (Recursos Tribunais Superiores). As 13 unidades tornam-se Apoio / Triagem na Origem.
5. GAB, PGA e SGRH lideram E5.O7.KR1/KR2 (Concursos). UGAM torna-se Apoio de Levantamento.
6. SI reclassifica Data Center de E5.O1.KR1 para E7.O2.KR2.
7. ESAP e SGRH lideram E9.O2.KR1 (Capacitação 40%). As outras 40 unidades tornam-se Demandante Setorial no PAC.
8. OUV assume liderança de E4.O1.KR3 (Ouvidoria). Outras unidades atuam como apoio.
9. Incorpora propostas formais da ASCOM (Manifestação 20) e Ouvidoria (Manifestação 19).
10. Regrava todas as 41 planilhas via write_sheet_to_all_targets.
"""
import os
import re
import openpyxl
from pathlib import Path
from scratch_sei_analise.saneamento_ascom_e_ti import UNIT_FOLDERS, load_rows, write_sheet_to_all_targets

BASE_DIR = Path(__file__).resolve().parent.parent
CONS_DIR = BASE_DIR / "Planilhas_Pos_Comparacao_Consolidadas"
ASCOM_UPLOAD = Path(r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.user_uploaded\media_1794232193070_7c5de750.xlsx")
OUV_UPLOAD = Path(r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.user_uploaded\media_1794232193094_723ee57e.xlsx")

def executar_saneamento():
    print("Iniciando Saneamento Transversal de Metodologia...")
    modificados = {}

    # 1. Tratar ASCOM a partir da Manifestação 20
    print("\n--- 1. Atualizando ASCOM (Manifestação 20) ---")
    wb_a = openpyxl.load_workbook(ASCOM_UPLOAD)
    ws_a = wb_a["Plano de Ação"]
    rows_ascom = []
    for r in range(6, ws_a.max_row + 1):
        vals = [ws_a.cell(r, c).value for c in range(1, 8)]
        if any(vals):
            rows_ascom.append([str(v or "").strip() for v in vals])
    t1_a = "PROPOSTA DE PLANO DE AÇÃO – ASSESSORIA DE COMUNICAÇÃO (ASCOM)"
    t2_a = "Adequada ao Plano de Ação Estratégico (Manifestação SEI nº 20/2026)"
    write_sheet_to_all_targets("ASCOM", t1_a, t2_a, rows_ascom)
    modificados["ASCOM"] = len(rows_ascom)
    print(f"ASCOM regravada com {len(rows_ascom)} ações.")

    # 2. Tratar OUVIDORIA a partir da Manifestação 19
    print("\n--- 2. Atualizando OUVIDORIA (Manifestação 19) ---")
    wb_o = openpyxl.load_workbook(OUV_UPLOAD)
    ws_o = wb_o["Plano de Ação"]
    rows_ouv = []
    for r in range(6, ws_o.max_row + 1):
        vals = [ws_o.cell(r, c).value for c in range(1, 8)]
        if any(vals):
            rows_ouv.append([str(v or "").strip() for v in vals])
    t1_o = "PROPOSTA DE PLANO DE AÇÃO – OUVIDORIA (REVISADA)"
    t2_o = "Adequada ao Plano de Ação Estratégico (Manifestação SEI nº 19/2026)"
    write_sheet_to_all_targets("OUV", t1_o, t2_o, rows_ouv)
    modificados["OUV"] = len(rows_ouv)
    print(f"OUVIDORIA regravada com {len(rows_ouv)} ações.")

    # 3. Tratar CONSELHO SUPERIOR (CS) - Adicionar liderança exclusiva de E9.O3.KR1
    print("\n--- 3. Atualizando CONSELHO SUPERIOR (CS) ---")
    p_cs = CONS_DIR / "Plano_Acao_Pos_Comparacao_CS.xlsx"
    rows_cs, t1_cs, t2_cs = load_rows(p_cs)
    tem_honorarios = any("E9.O3.KR1" in str(r[2]) for r in rows_cs)
    if not tem_honorarios:
        nova_acao_cs = [
            "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
            "O3: Fortalecer a governança e a gestão de receitas de honorários",
            "[E9.O3.KR1] KR1: Aumentar em 15% a arrecadação de honorários sucumbenciais até 2029",
            "Deliberar sobre diretrizes institucionais e regulamentação da arrecadação e destinação de honorários sucumbenciais",
            "Fixar diretrizes normativas no âmbito do Conselho Superior para acompanhamento do fundo de honorários, critérios de rateio, fomento à execução de verbas sucumbenciais e monitoramento da meta global de incremento de 15% até 2029.",
            "Líder: Conselho Superior da PGE (CS); Apoio Operacional: Procuradoria da Dívida Ativa (PDA), PERJP, PGAAE, PGA",
            "Ciclo Anual até 2029"
        ]
        rows_cs.append(nova_acao_cs)
        write_sheet_to_all_targets("CS", t1_cs, t2_cs, rows_cs)
        modificados["CS"] = len(rows_cs)
        print(f"CS atualizado: adicionada liderança exclusiva de E9.O3.KR1 (total: {len(rows_cs)} ações).")

    # 4. Tratar SUPERVISÃO DE INFORMÁTICA (SI) - Data Center para E7.O2.KR2 e RPA como Apoio
    print("\n--- 4. Atualizando SUPERVISÃO DE INFORMÁTICA (SI) ---")
    p_si = CONS_DIR / "Plano_Acao_Pos_Comparacao_SI.xlsx"
    rows_si, t1_si, t2_si = load_rows(p_si)
    for r in rows_si:
        # Data center
        if "Data Center" in str(r[3]) or "Data Center Nutanix" in str(r[4]):
            if "E5.O1.KR1" in str(r[2]):
                r[0] = "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica"
                r[1] = "O2: Garantir a infraestrutura, segurança da informação e continuidade dos serviços de TIC"
                r[2] = "[E7.O2.KR2] KR2: Garantir 99,5% de disponibilidade dos sistemas críticos da PGE (PJe, SPA, Portal) até 2027"
                r[5] = "Líder de Infraestrutura Física: Supervisão de Informática (SI); Instância Decisória: Procurador-Geral do Estado"
                print("  SI: Ação de Data Center reclassificada para E7.O2.KR2.")
        # Robôs de automação
        if "robôs de automação" in str(r[3]).lower() or "ambiente de hospedagem para execução de robôs" in str(r[3]).lower():
            r[5] = "Líder da Meta: Assessoria em TIC da PGAAE / INOVA; Suporte de Infraestrutura Física: Supervisão de Informática (SI)"
            print("  SI: Ação de RPA ajustada com liderança da TIC/INOVA e Suporte da SI.")
    write_sheet_to_all_targets("SI", t1_si, t2_si, rows_si)
    modificados["SI"] = len(rows_si)

    # 5. Percorrer todas as demais unidades para ajustar papéis de apoio, insumo e liderança
    print("\n--- 5. Saneando papéis de governança em todas as unidades ---")
    todas_siglas = sorted(UNIT_FOLDERS.keys())
    for sigla in todas_siglas:
        if sigla in ["ASCOM", "OUV"]:
            continue # Já tratados com as manifestações integrais
        xlsx_path = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
        if not xlsx_path.exists():
            continue
        rows, t1, t2 = load_rows(xlsx_path)
        changed = False

        for r in rows:
            kr = str(r[2] or "")
            acao = str(r[3] or "")
            resp = str(r[5] or "")

            # A. E9.O3.KR1 (Honorários) nas unidades secundárias (exceto CS)
            if "E9.O3.KR1" in kr and sigla != "CS":
                if "Líder da Meta: Conselho Superior" not in resp:
                    r[5] = f"Líder da Meta: Conselho Superior da PGE (CS); Fornecedor de Insumo / Execução Setorial: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

            # B. E6.O1.KR2 (Redes Sociais) nas unidades setoriais (exceto ASCOM)
            if "E6.O1.KR2" in kr and sigla != "ASCOM":
                if "Líder da Meta: Assessoria de Comunicação" not in resp:
                    r[5] = f"Líder da Meta: Assessoria de Comunicação (ASCOM); Fornecedor de Insumo / Apoio Operacional: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

            # C. E7.O3.KR1 (Projetos Estratégicos) nas unidades setoriais (exceto PGAAE)
            if "E7.O3.KR1" in kr and sigla != "PGAAE":
                if "Líder da Meta: PGAAE" not in resp:
                    r[5] = f"Líder da Meta: Procurador-Geral Adjunta para Assuntos Estratégicos (PGAAE); Apoio / Usuário Piloto: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

            # D. E5.O2.KR2 (Recursos Tribunais Superiores) nas especializadas (exceto PGAAJ e PB)
            if "E5.O2.KR2" in kr and sigla not in ["PGAAJ", "PB"]:
                if "Líderes da Meta: PGAAJ e PB" not in resp:
                    r[5] = f"Líderes da Meta: PGAAJ e Procuradoria de Brasília (PB); Apoio Operacional / Triagem na Origem: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

            # E. E5.O7.KR1 / KR2 (Concursos) na UGAM
            if sigla == "UGAM" and ("E5.O7.KR1" in kr or "E5.O7.KR2" in kr):
                if "Líderes da Meta: Gabinete" not in resp:
                    r[5] = "Líderes da Meta: Gabinete do Procurador-Geral (GAB), PGA e SGRH; Apoio de Levantamento e Dimensionamento: UGAM"
                    changed = True

            # F. E9.O2.KR1 (Capacitação 40% / PAC) nas unidades demandantes (exceto ESAP e SGRH)
            if "E9.O2.KR1" in kr and sigla not in ["ESAP", "SGRH"]:
                if "Líderes da Meta: ESAP e SGRH" not in resp:
                    r[5] = f"Líderes da Meta: Escola Superior da Advocacia Pública (ESAP) e SGRH; Demandante Setorial / Mapeamento: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

            # G. E4.O1.KR3 (Ouvidoria) nas unidades de apoio (exceto OUV)
            if "E4.O1.KR3" in kr and sigla != "OUV":
                if "Líder da Meta: Ouvidoria" not in resp:
                    r[5] = f"Líder da Meta: Ouvidoria (OUV); Apoio / Fornecedor de Resposta: {UNIT_FOLDERS.get(sigla, sigla)} ({sigla})"
                    changed = True

        if changed or sigla == "CS":
            write_sheet_to_all_targets(sigla, t1, t2, rows)
            modificados[sigla] = len(rows)
            print(f"  Unidade {sigla} saneada e regravada ({len(rows)} ações).")

    print(f"\nSaneamento das planilhas concluído! {len(modificados)} unidades atualizadas.")
    return modificados

if __name__ == "__main__":
    executar_saneamento()
