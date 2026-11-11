# -*- coding: utf-8 -*-
"""
Script de Padronização dos Eixos Estratégicos (Opção 2 - Orientada a Valor e Impacto):
1. Eixo 1: Eixo Estratégico 1 – Otimização da Arrecadação e Recuperação da Dívida Ativa
2. Eixo 2: Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais (Mantido)
3. Eixo 3: Eixo Estratégico 3 – Sustentabilidade Orçamentária e Captação de Recursos
4. Eixo 4: Eixo Estratégico 4 – Excelência no Atendimento e Satisfação do Usuário
   - Objetivo O1: O1: Aperfeiçoar o atendimento e a experiência do usuário dos serviços da PGE (Desvinculado do nome do eixo)
5. Eixo 5: Eixo Estratégico 5 – Eficiência Processual, Resolutividade e Defesa Estratégica
6. Eixo 6: Eixo Estratégico 6 – Fortalecimento da Imagem Institucional e Transparência
7. Eixo 7: Eixo Estratégico 7 – Transformação Digital e Inovação Tecnológica
8. Eixo 8: Eixo Estratégico 8 – Governança Ética, Integridade e Sustentabilidade
9. Eixo 9: Eixo Estratégico 9 – Valorização Profissional e Desenvolvimento de Pessoas

Aplica em:
- 41 planilhas consolidadas e setoriais
- Banco de dados SQLite sgpe_pge_ma.db
- Relatórios markdown (Cotejamento e 3 Ps)
"""
import re
import sys
from pathlib import Path

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
CONS_DIR = BASE_DIR / "Planilhas_Pos_Comparacao_Consolidadas"

sys.path.insert(0, str(BASE_DIR / "scratch_sei_analise"))
from saneamento_ascom_e_ti import UNIT_FOLDERS, load_rows, write_sheet_to_all_targets

CANONICAL_EIXOS = {
    "E1": "Eixo Estratégico 1 – Otimização da Arrecadação e Recuperação da Dívida Ativa",
    "E2": "Eixo Estratégico 2 – Eficiência Administrativa e Redução de Custos Operacionais",
    "E3": "Eixo Estratégico 3 – Sustentabilidade Orçamentária e Captação de Recursos",
    "E4": "Eixo Estratégico 4 – Excelência no Atendimento e Satisfação do Usuário",
    "E5": "Eixo Estratégico 5 – Eficiência Processual, Resolutividade e Defesa Estratégica",
    "E6": "Eixo Estratégico 6 – Fortalecimento da Imagem Institucional e Transparência",
    "E7": "Eixo Estratégico 7 – Transformação Digital e Inovação Tecnológica",
    "E8": "Eixo Estratégico 8 – Governança Ética, Integridade e Sustentabilidade",
    "E9": "Eixo Estratégico 9 – Valorização Profissional e Desenvolvimento de Pessoas",
}

def extract_eixo_prefix(kr_str: str, eixo_str: str) -> str:
    m = re.search(r"\[(E\d)\.", str(kr_str or ""))
    if m:
        return m.group(1)
    m2 = re.search(r"\b(E\d)\.", str(kr_str or ""))
    if m2:
        return m2.group(1)
    m3 = re.search(r"Eixo\s+(?:Estratégico\s+)?(\d)", str(eixo_str or ""), re.IGNORECASE)
    if m3:
        return f"E{m3.group(1)}"
    return ""

def executar_padronizacao():
    print("="*70)
    print("INICIANDO PADRONIZAÇÃO DOS EIXOS ESTRATÉGICOS (OPÇÃO 2)")
    print("="*70)

    total_planilhas = 0
    total_linhas_atualizadas = 0

    for sigla in sorted(UNIT_FOLDERS.keys()):
        xlsx_path = CONS_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
        if not xlsx_path.exists():
            print(f"Aviso: Planilha não encontrada para {sigla}: {xlsx_path}")
            continue

        rows, t1, t2 = load_rows(xlsx_path)
        new_rows = []
        modificado = False

        for r in rows:
            eixo_orig = str(r[0] or "").strip()
            obj_orig = str(r[1] or "").strip()
            kr_orig = str(r[2] or "").strip()

            prefix = extract_eixo_prefix(kr_orig, eixo_orig)
            if prefix in CANONICAL_EIXOS:
                canonical_eixo = CANONICAL_EIXOS[prefix]
                if r[0] != canonical_eixo:
                    r[0] = canonical_eixo
                    modificado = True

                # Ajuste de O1 em Eixo 4 para eliminar duplicação
                if prefix == "E4":
                    novo_obj = "O1: Aperfeiçoar o atendimento e a experiência do usuário dos serviços da PGE"
                    if r[1] != novo_obj:
                        r[1] = novo_obj
                        modificado = True

                total_linhas_atualizadas += 1
            else:
                print(f"  [AVISO] Linha sem prefixo reconhecido em {sigla}: Eixo='{eixo_orig}', KR='{kr_orig}'")

            new_rows.append(r)

        write_sheet_to_all_targets(sigla, t1, t2, new_rows)
        total_planilhas += 1

    print(f"\nPlanilhas atualizadas: {total_planilhas}")
    print(f"Linhas checadas/padronizadas: {total_linhas_atualizadas}")

    # Atualizar arquivos markdown de documentação
    print("\nAtualizando arquivos de documentação Markdown...")
    
    # 1. Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md
    cotejamento_path = BASE_DIR / "Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md"
    if cotejamento_path.exists():
        text_cot = cotejamento_path.read_text(encoding="utf-8")
        # Substituições das linhas da tabela
        substituicoes = [
            ("Incrementar a arrecadação e otimizar a cobrança da dívida ativa", "Otimização da Arrecadação e Recuperação da Dívida Ativa"),
            ("Incrementar e executar integralmente o orçamento institucional", "Sustentabilidade Orçamentária e Captação de Recursos"),
            ("Melhorar a experiência do usuário dos serviços da PGE", "Excelência no Atendimento e Satisfação do Usuário"),
            ("Alcançar maior eficiência e resolutividade nos processos internos e externos", "Eficiência Processual, Resolutividade e Defesa Estratégica"),
            ("Fortalecer a imagem institucional e a comunicação com a sociedade", "Fortalecimento da Imagem Institucional e Transparência"),
            ("Promover a transformação digital e a inovação tecnológica", "Transformação Digital e Inovação Tecnológica"),
            ("Fomentar a sustentabilidade, a integridade e a responsabilidade social", "Governança Ética, Integridade e Sustentabilidade"),
            ("Valorizar, integrar e qualificar servidores e procuradores", "Valorização Profissional e Desenvolvimento de Pessoas"),
        ]
        for antigo, novo in substituicoes:
            text_cot = text_cot.replace(antigo, novo)
        cotejamento_path.write_text(text_cot, encoding="utf-8")
        print("  Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md atualizado.")

    # 2. Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md
    transversal_path = BASE_DIR / "Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md"
    if transversal_path.exists():
        text_trans = transversal_path.read_text(encoding="utf-8")
        text_trans = text_trans.replace("Melhorar a experiência do usuário dos serviços da PGE", "Excelência no Atendimento e Satisfação do Usuário")
        transversal_path.write_text(text_trans, encoding="utf-8")
        print("  Consolidacao_Transversal_3_Ps_Prazo_Presenca_Padronizacao.md atualizado.")

if __name__ == "__main__":
    executar_padronizacao()
