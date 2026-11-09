# -*- coding: utf-8 -*-
"""
Script de Saneamento Rigoroso de Heranças Indevidas de Minutas Preliminares:
1. ESAP: Elimina Eixo 8 (9 ações), Eixo 9.O1 (11 ações) e duplicatas PGAAE em E6.O2.KR1 (7 ações).
2. PRI e PRT: Elimina E4.O1.KR1 (6 ações), E4.O1.KR3 (2 ações), E7.O1.KR1 (4 ações), E7.O3.KR1 (2 ações),
   e 3 ações centralizadas de SPA/distribuição em E5.O6.KR1. Reclassifica E5.O3.KR2 e E5.O6.KR1 (geral) para Coexecutor.
3. PGA: Elimina E8.O1.KR1 (8 ações) e E9.O1 (16 ações). Reclassifica ações concorrentes com PGAAE/SI para Apoio/Coexecutor.
4. Conselho Superior (CS): Reclassifica E5.O5.KR3 e E8.O1.KR2 para Coexecutor. Mantém E9.O3.KR1 como LÍDER (exceção deferida).
5. UGAM: Elimina 2 ações de resíduos sólidos em E8.O1.KR1.
6. CEQUIDADE: Elimina 4 ações de resíduos sólidos e campanha ambiental em E8.O1.KR1.
7. PJEFP: Ajusta responsabilidade da ação de enlace do Fórum Sarney em E7.O2.KR2 para Apoio Operacional.
8. Regrava todas as planilhas via write_sheet_to_all_targets.
9. Sincroniza o banco de dados SQLite sgpe_pge_ma.db.
"""
import os
import re
import sys
import openpyxl
from pathlib import Path

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
CONS_DIR = BASE_DIR / "Planilhas_Pos_Comparacao_Consolidadas"

sys.path.insert(0, str(BASE_DIR / "scratch_sei_analise"))
from saneamento_ascom_e_ti import UNIT_FOLDERS, load_rows, write_sheet_to_all_targets

def executar_saneamento():
    print("="*70)
    print("INICIANDO EXECUÇÃO DO SANEAMENTO DE HERANÇAS INDEVIDAS")
    print("="*70)

    # 1. ESAP
    xlsx_esap = CONS_DIR / "Plano_Acao_Pos_Comparacao_ESAP.xlsx"
    rows_esap, t1_esap, t2_esap = load_rows(xlsx_esap)
    new_rows_esap = []
    
    # Ações da PGAAE duplicadas em E6.O2.KR1 que devem sair da ESAP:
    dups_pgaae_e6 = [
        "Instituir carteira institucional de parcerias estratégicas",
        "Mapear e qualificar parcerias já iniciadas em 2025",
        "Criar fluxo padrão para celebração e acompanhamento de acordos de cooperação",
        "Fixar metas anuais intermediárias para o atingimento dos 10 projetos até 2030",
        "Priorizar projetos com entrega institucional mensurável",
        "Criar painel executivo de parcerias, intercâmbios e projetos derivados",
        "Produzir relatório semestral de cooperação estratégica e inovação aplicada"
    ]

    for r in rows_esap:
        eixo = str(r[0] or "")
        kr = str(r[2] or "")
        acao = str(r[3] or "").strip()

        # Remove Eixo 8
        if "Eixo Estratégico 8" in eixo or "E8." in kr:
            continue
        # Remove Eixo 9.O1
        if "E9.O1" in kr:
            continue
        # Remove duplicatas corporativas em E6.O2.KR1
        if "E6.O2.KR1" in kr and any(d.lower() in acao.lower() for d in dups_pgaae_e6):
            continue

        new_rows_esap.append(r)

    print(f"ESAP: {len(rows_esap)} -> {len(new_rows_esap)} ações (removidas {len(rows_esap) - len(new_rows_esap)})")
    write_sheet_to_all_targets("ESAP", t1_esap, t2_esap, new_rows_esap)

    # 2. PRI e PRT
    for sigla in ["PRI", "PRT"]:
        xlsx_reg = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
        rows_reg, t1_reg, t2_reg = load_rows(xlsx_reg)
        new_rows_reg = []

        acoes_centrais_e56 = [
            "distribuição eletrônica de processos",
            "captura de expedientes do pje",
            "corrigir dashboards das especializadas"
        ]

        for r in rows_reg:
            kr = str(r[2] or "")
            acao = str(r[3] or "").strip()

            # Remove E4.O1.KR1 e E4.O1.KR3
            if "E4.O1.KR1" in kr or "E4.O1.KR3" in kr:
                continue
            # Remove E7.O1.KR1 e E7.O3.KR1
            if "E7.O1.KR1" in kr or "E7.O3.KR1" in kr:
                continue
            # Remove acoes centralizadas de SPA/distribuicao em E5.O6.KR1
            if "E5.O6.KR1" in kr and any(ac.lower() in acao.lower() for ac in acoes_centrais_e56):
                continue

            # Reclassifica liderança indevida em E5.O3.KR2 para Coexecutor
            if "E5.O3.KR2" in kr:
                r[5] = f"Líder: PGAAE / Especializadas Temáticas; Coexecutores: Procuradoria Regional de {('Imperatriz (PRI)' if sigla == 'PRI' else 'Timon (PRT)')}"

            # Reclassifica liderança indevida em E5.O6.KR1 (ações corporativas) para Coexecutor
            if "E5.O6.KR1" in kr:
                if "Instituir programa" in acao:
                    r[5] = f"Líder Executivo: Subprocuradoria-Geral Adjunta (SGA); Coexecutores: Procuradoria Regional de {('Imperatriz (PRI)' if sigla == 'PRI' else 'Timon (PRT)')}"
                elif "Levantar a linha de base" in acao:
                    r[5] = f"Líder: Corregedoria-Geral (CG); Coexecutores: Procuradoria Regional de {('Imperatriz (PRI)' if sigla == 'PRI' else 'Timon (PRT)')}"
                elif "Mapear integralmente a jornada" in acao:
                    r[5] = f"Líder: Corregedoria-Geral / SGA; Coexecutores: Procuradoria Regional de {('Imperatriz (PRI)' if sigla == 'PRI' else 'Timon (PRT)')}"
                elif "Implantar conferência diária" in acao:
                    # Conferência diária local da Regional: Mantém Líder local
                    r[5] = f"Líder: Procuradoria Regional de {('Imperatriz (PRI)' if sigla == 'PRI' else 'Timon (PRT)')}; Apoio: Triagem e Distribuição / SGA"

            new_rows_reg.append(r)

        print(f"{sigla}: {len(rows_reg)} -> {len(new_rows_reg)} ações (removidas {len(rows_reg) - len(new_rows_reg)})")
        write_sheet_to_all_targets(sigla, t1_reg, t2_reg, new_rows_reg)

    # 3. PGA
    xlsx_pga = CONS_DIR / "Plano_Acao_Pos_Comparacao_PGA.xlsx"
    rows_pga, t1_pga, t2_pga = load_rows(xlsx_pga)
    new_rows_pga = []

    for r in rows_pga:
        eixo = str(r[0] or "")
        kr = str(r[2] or "")
        acao = str(r[3] or "").strip()

        # Remove E8.O1.KR1
        if "E8.O1.KR1" in kr:
            continue
        # Remove E9.O1
        if "E9.O1" in kr:
            continue

        # Reclassifica liderança corporativa onde PGAAE/SI lideram:
        if "E2.O1.KR2" in kr and "painel de disponibilidade" in acao.lower():
            r[5] = "Líder: Supervisão de Informática (SI) e TIC/PGAAE; Apoio: Procuradoria-Geral Adjunta (PGA)"
        elif "E5.O3.KR2" in kr:
            r[5] = "Líder: PGAAE / Especializadas Temáticas; Coexecutores: Procuradoria-Geral Adjunta (PGA)"
        elif "E5.O5.KR1" in kr:
            r[5] = "Líder: PGAAE / Laboratório INOVA; Apoio Superior: Procuradoria-Geral Adjunta (PGA)"
        elif "E5.O5.KR3" in kr:
            r[5] = "Líder: PGAAE; Apoio Superior: Procuradoria-Geral Adjunta (PGA)"
        elif "E5.O7.KR1" in kr or "E5.O7.KR2" in kr:
            r[5] = "Líder: Gabinete do Procurador-Geral e SGRH; Coexecutores: Procuradoria-Geral Adjunta (PGA), PGAAE"
        elif "E7.O1.KR1" in kr and any(k in acao.lower() for k in ["trilha prioritária", "ambiente de automação", "consultoria de transformação", "acordos trabalhistas", "painel institucional"]):
            r[5] = "Líder: PGAAE / Laboratório INOVA; Apoio Superior: Procuradoria-Geral Adjunta (PGA)"
        elif "E7.O2.KR2" in kr:
            r[5] = "Líder: Supervisão de Informática (SI); Apoio Superior: Procuradoria-Geral Adjunta (PGA)"

        new_rows_pga.append(r)

    print(f"PGA: {len(rows_pga)} -> {len(new_rows_pga)} ações (removidas {len(rows_pga) - len(new_rows_pga)})")
    write_sheet_to_all_targets("PGA", t1_pga, t2_pga, new_rows_pga)

    # 4. PGAAE: ajustar E7.O2.KR2 para que SI seja o Líder único de infraestrutura/backup
    xlsx_pgaae = CONS_DIR / "Plano_Acao_Pos_Comparacao_PGAAE.xlsx"
    rows_pgaae, t1_pgaae, t2_pgaae = load_rows(xlsx_pgaae)
    for r in rows_pgaae:
        kr = str(r[2] or "")
        if "E7.O2.KR2" in kr:
            r[5] = "Líder: Supervisão de Informática (SI); Apoio Institucional: PGAAE"
    write_sheet_to_all_targets("PGAAE", t1_pgaae, t2_pgaae, rows_pgaae)
    print("PGAAE: E7.O2.KR2 alinhado com SI como Líder exclusivo de infraestrutura/backup.")

    # 5. Conselho Superior (CS)
    xlsx_cs = CONS_DIR / "Plano_Acao_Pos_Comparacao_CS.xlsx"
    rows_cs, t1_cs, t2_cs = load_rows(xlsx_cs)
    for r in rows_cs:
        kr = str(r[2] or "")
        acao = str(r[3] or "").strip()
        # E5.O5.KR3: Coexecutor
        if "E5.O5.KR3" in kr:
            r[5] = "Líder: PGAAE; Coexecutores: Conselho Superior (CS) no âmbito do Colegiado"
        # E8.O1.KR2: Coexecutor
        elif "E8.O1.KR2" in kr:
            r[5] = "Líder: Gabinete do Procurador-Geral e Comitê de Equidade; Coexecutores: Conselho Superior (CS)"
        # E9.O3.KR1: MANTÉM COMO LÍDER (Exceção deferida pelo usuário)
        elif "E9.O3.KR1" in kr:
            r[5] = "Líder: Conselho Superior da PGE-MA (Deliberação e Regulamentação Colegiada); Coexecutores: Especializadas Contenciosas, PROFI, Gabinete"
    write_sheet_to_all_targets("CS", t1_cs, t2_cs, rows_cs)
    print("CS: Papéis saneados (E5.O5.KR3 e E8.O1.KR2 como Coexecutor; E9.O3.KR1 preservado como Líder).")

    # 6. UGAM
    xlsx_ugam = CONS_DIR / "Plano_Acao_Pos_Comparacao_UGAM.xlsx"
    rows_ugam, t1_ugam, t2_ugam = load_rows(xlsx_ugam)
    new_rows_ugam = [r for r in rows_ugam if "E8.O1.KR1" not in str(r[2] or "")]
    print(f"UGAM: {len(rows_ugam)} -> {len(new_rows_ugam)} ações (removidas {len(rows_ugam) - len(new_rows_ugam)})")
    write_sheet_to_all_targets("UGAM", t1_ugam, t2_ugam, new_rows_ugam)

    # 7. CEQUIDADE
    xlsx_ceq = CONS_DIR / "Plano_Acao_Pos_Comparacao_CEQUIDADE.xlsx"
    rows_ceq, t1_ceq, t2_ceq = load_rows(xlsx_ceq)
    new_rows_ceq = [r for r in rows_ceq if "E8.O1.KR1" not in str(r[2] or "")]
    print(f"CEQUIDADE: {len(rows_ceq)} -> {len(new_rows_ceq)} ações (removidas {len(rows_ceq) - len(new_rows_ceq)})")
    write_sheet_to_all_targets("CEQUIDADE", t1_ceq, t2_ceq, new_rows_ceq)

    # 8. PJEFP
    xlsx_pjefp = CONS_DIR / "Plano_Acao_Pos_Comparacao_PJEFP.xlsx"
    rows_pjefp, t1_pjefp, t2_pjefp = load_rows(xlsx_pjefp)
    for r in rows_pjefp:
        kr = str(r[2] or "")
        acao = str(r[3] or "").strip()
        if "E7.O2.KR2" in kr and "Fórum" in acao:
            r[5] = "Líder: Assessoria em TIC da PGAAE / INOVA; Apoio Operacional e Demanda: PJEFP; Suporte de Infraestrutura: Supervisão de Informática (SI); Canal de Avisos: SGRH"
    write_sheet_to_all_targets("PJEFP", t1_pjefp, t2_pjefp, rows_pjefp)
    print("PJEFP: Ação de integração do Fórum ajustada para Apoio Operacional em E7.O2.KR2.")

    print("\nSaneamento das planilhas concluído com sucesso!")

if __name__ == "__main__":
    executar_saneamento()
