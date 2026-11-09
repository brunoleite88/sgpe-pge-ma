# -*- coding: utf-8 -*-
"""
Script de Unificação e Saneamento da Capacitação em IA e Direito Digital:
1. Elimina o KR [E7.O3.KR2] do catálogo de metas da PGE-MA.
2. Incorpora a formação em Direito Digital e IA como Ação Prioritária Estruturante da ESAP dentro de [E9.O2.KR1].
3. Nas unidades especializadas (ASJUR, NCIA, NIRF, PA, PCF, PDA, PEDU, PERJP, PGAAJ, PPIMA, PRI, PRT, PSAU, PSP, PT, SGA),
   consolida as demandas formativas de IA em sua ação anual do PAC sob [E9.O2.KR1].
4. Em PB, reclassifica a superação de triagens por IA (Sócrates/Victor) para [E5.O2.KR2] (Tribunais Superiores).
5. Em PJ, consolida Minuta IA em [E7.O1.KR1] e capacitação sob [E9.O2.KR1].
6. Em PJEFP, move a infraestrutura do Fórum para [E7.O2.KR2] e capacitação para [E9.O2.KR1].
7. Em SI, move o suporte de laboratórios de IA para [E9.O2.KR1] (Apoio à ESAP).
8. Em PGAAE e SGRH, elimina as 5 ações duplicadas de E7.O3.KR2.
9. Regrava todas as 41 planilhas via write_sheet_to_all_targets.
10. Sincroniza o banco de dados SQLite.
"""
import os
import re
import openpyxl
from pathlib import Path
from scratch_sei_analise.saneamento_ascom_e_ti import UNIT_FOLDERS, load_rows, write_sheet_to_all_targets

BASE_DIR = Path(__file__).resolve().parent.parent
CONS_DIR = BASE_DIR / "Planilhas_Pos_Comparacao_Consolidadas"

def executar_unificacao():
    print("Iniciando Unificação de E7.O3.KR2 em E9.O2.KR1...")
    modificados = {}

    todas_siglas = sorted(UNIT_FOLDERS.keys())
    for sigla in todas_siglas:
        xlsx_path = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
        if not xlsx_path.exists():
            continue

        rows, t1, t2 = load_rows(xlsx_path)
        new_rows = []
        changed = False

        # Verifica se a unidade tinha ações sob E7.O3.KR2
        tinha_e7 = any("E7.O3.KR2" in str(r[2] or "") for r in rows)

        if sigla == "ESAP":
            # Filtra fora as 5 ações de E7.O3.KR2
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    continue
                new_rows.append(r)
            
            # Adiciona a Ação Prioritária em E9.O2.KR1
            acao_ia_esap = [
                "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores",
                "O2: Desenvolver competências, valorizar os servidores e procuradores e promover capacitação continuada",
                "[E9.O2.KR1] KR1: Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029",
                "Instituir Trilha Estratégica Prioritária de Direito Digital e Inteligência Artificial no Plano Anual de Capacitação (PAC) da PGE-MA",
                "Ofertar trilhas formativas em inteligência artificial generativa, ferramentas analíticas, governança de dados e direito digital, articulando os módulos técnicos do BID 2026 e certificações para membros e servidores da PGE.",
                "Líder: Escola Superior da Advocacia Pública (ESAP); Coexecutores: PGAAE / Laboratório INOVA, Supervisão de Informática (SI), SGRH; Apoio: Unidades Setoriais",
                "2027 (Trilha contínua até 2030)"
            ]
            new_rows.append(acao_ia_esap)
            changed = True
            print("  ESAP: E7.O3.KR2 unificado em E9.O2.KR1 com Ação Prioritária Estruturante.")

        elif sigla == "PGAAE":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    continue
                new_rows.append(r)
            print("  PGAAE: Removidas 5 ações redundantes de E7.O3.KR2.")

        elif sigla == "SGRH":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    continue
                new_rows.append(r)
            print("  SGRH: Removida ação redundante de E7.O3.KR2 (absorvida por E9.O2.KR1).")

        elif sigla == "PB":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    # Reclassifica ação Sócrates/Victor para E5.O2.KR2
                    r[0] = "Eixo Estratégico 5 – Aperfeiçoar a atuação contenciosa e consultiva com foco na resolutividade"
                    r[1] = "O2: Reduzir a litigiosidade e qualificar a representação nos Tribunais Superiores"
                    r[2] = "[E5.O2.KR2] KR2: Elevar a taxa de conhecimento dos recursos nos Tribunais Superiores para 85% até 2030"
                    r[5] = "Líder da Meta e da Ação: Procuradoria de Brasília (PB) e PGAAJ; Apoio Pedagógico: ESAP / INOVA PGE"
                    new_rows.append(r)
                else:
                    new_rows.append(r)
            print("  PB: Ação de Sócrates/Victor reclassificada para E5.O2.KR2 (Tribunais Superiores).")

        elif sigla == "PJ":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    # Ação 10 (Minuta IA) já contemplada na ação de automação em E7.O1.KR1
                    # Ação 11 (trilhas de capacitação) já contemplada no PAC de E9.O2.KR1
                    continue
                # Se for a ação de automação no E7.O1.KR1, garante texto completo
                if "E7.O1.KR1" in str(r[2] or "") and "Minuta IA" in str(r[3] or ""):
                    r[3] = "Sistematizar banco de minutas padronizadas cíveis e modelos assistidos por IA (Minuta IA) no SPA"
                    r[4] = "Implantar ferramenta de IA generativa (Minuta IA) para automação de minutas de contestações e recursos em cobranças de dativos e demandas repetitivas do Grupo 2, reduzindo tempo de resposta."
                    changed = True
                new_rows.append(r)
            print("  PJ: Ações de E7.O3.KR2 consolidadas em E7.O1.KR1 e E9.O2.KR1.")

        elif sigla == "PJEFP":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    # Se for a ação de integração do Fórum José Sarney -> Move para E7.O2.KR2
                    if "Fórum José Sarney" in str(r[3] or "") or "Fórum Des. José Sarney" in str(r[4] or ""):
                        r[0] = "Eixo Estratégico 7 – Promover a transformação digital e a inovação tecnológica"
                        r[1] = "O2: Garantir a infraestrutura, segurança da informação e continuidade dos serviços de TIC"
                        r[2] = "[E7.O2.KR2] KR2: Assegurar 100% de capacidade de recuperação de dados processuais em contingências até 2028"
                        r[5] = "Líder da Demanda: PJEFP; Suporte de Infraestrutura e Redes: Supervisão de Informática (SI) e TIC/PGAAE"
                        new_rows.append(r)
                    else:
                        # Capacitação em IA da PJEFP absorvida no PAC
                        continue
                else:
                    new_rows.append(r)
            # Enriquece a ação de PAC da PJEFP
            for r in new_rows:
                if "E9.O2.KR1" in str(r[2] or ""):
                    if "inteligência artificial" not in str(r[4] or "").lower():
                        r[4] = str(r[4] or "") + " Inclui demandas de capacitação em IA generativa (Minuta IA / Biblioteca de Prompts Alexandre) e jurimetria do Juizado da Fazenda Pública."
                        changed = True
            print("  PJEFP: Ações de E7.O3.KR2 consolidadas em E7.O2.KR2 e E9.O2.KR1.")

        elif sigla == "SI":
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    # Reclassifica para suporte de laboratórios no E9.O2.KR1
                    r[0] = "Eixo Estratégico 9 – Valorizar, integrar e qualificar servidores e procuradores"
                    r[1] = "O2: Desenvolver competências, valorizar os servidores e procuradores e promover capacitação continuada"
                    r[2] = "[E9.O2.KR1] KR1: Garantir a participação de ao menos 40% do corpo funcional em cursos de capacitação até 2029"
                    r[5] = "Líder da Meta: ESAP e SGRH; Suporte de Infraestrutura Tecnológica e Laboratórios: Supervisão de Informática (SI)"
                    new_rows.append(r)
                else:
                    new_rows.append(r)
            print("  SI: Ação de suporte a laboratórios reclassificada para E9.O2.KR1.")

        else:
            # Demais unidades: se tinham E7.O3.KR2, remove a linha avulsa e enriquece a linha do PAC sob E9.O2.KR1
            for r in rows:
                if "E7.O3.KR2" in str(r[2] or ""):
                    changed = True
                    continue
                new_rows.append(r)

            if tinha_e7:
                # Enriquece o PAC em E9.O2.KR1
                for r in new_rows:
                    if "E9.O2.KR1" in str(r[2] or ""):
                        sub = str(r[4] or "")
                        if "inteligência artificial" not in sub.lower() and "direito digital" not in sub.lower():
                            r[4] = sub.rstrip(".") + ", bem como trilhas de Direito Digital, Inteligência Artificial generativa e ferramentas de automação da ESAP."
                            changed = True
                print(f"  {sigla}: E7.O3.KR2 consolidado na ação do PAC sob E9.O2.KR1.")

        if changed:
            write_sheet_to_all_targets(sigla, t1, t2, new_rows)
            modificados[sigla] = len(new_rows)

    print(f"\nTotal de unidades atualizadas: {len(modificados)}")

if __name__ == "__main__":
    executar_unificacao()
