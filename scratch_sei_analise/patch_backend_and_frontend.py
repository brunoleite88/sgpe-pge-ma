# -*- coding: utf-8 -*-
"""
Patch backend.py and index.html to align Relatório 8 (Quadro de Eixos, Objetivos e Metas)
with the new methodology:
- Primary leading units only in executive report
- Distinction of Líder vs Apoio/Coexecução
- Update UNIT_META and extract_relations
"""
from pathlib import Path
import re

BACKEND_PATH = Path("sgpe_app/backend.py")
INDEX_PATH = Path("sgpe_app/static/index.html")

def patch_backend():
    print("Patching backend.py...")
    txt = BACKEND_PATH.read_text(encoding="utf-8")

    # 1. Add CS, UGAM, NC, CEQUIDADE to UNIT_META
    meta_addition = '''    "CS": {
        "nome": "Conselho Superior da PGE",
        "tipo": "Órgão Deliberativo Superior",
        "bloco_3ps": "Governança Superior",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Presidente e Membros do Conselho Superior",
        "pauta_reuniao": "Deliberação e regulamentação da arrecadação e destinação de honorários sucumbenciais (E9.O3.KR1 - liderança exclusiva), apreciação de normas de equidade e promoção na carreira (E8.O1.KR2/KR3), pauta 100% eletrônica e sustentabilidade (E8.O1.KR1)."
    },
    "UGAM": {
        "nome": "Unidade Gestora de Atividade Meio",
        "tipo": "Unidade Administrativa",
        "bloco_3ps": "Gestão Administrativa",
        "status_reuniao": "Respondido no SEI",
        "processo_sei": "2026.11103.07211",
        "responsavel": "Chefia da UGAM",
        "pauta_reuniao": "Coordenação executiva dos serviços administrativos de apoio, almoxarifado, patrimônio e compras (Eixo 2), apoio ao dimensionamento funcional para concursos (E5.O7.KR1) e sustentabilidade predial (Eixo 8)."
    },
    "NC": {
        "nome": "Núcleo de Cálculos",
        "tipo": "Núcleo Técnico Contábil",
        "bloco_3ps": "Cálculos e Perícias",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Chefia do Núcleo de Cálculos",
        "pauta_reuniao": "Liderança técnica na redução de 90% em bloqueios e duplicidades de RPVs (E1.O1.KR2), pareceres de liquidação e expurgo de excesso de execução (E5.O5.KR3 e E1.O1.KR1) e automação com SPA/IA."
    },
    "CEQUIDADE": {
        "nome": "Comitê de Diversidade e Equidade",
        "tipo": "Órgão Colegiado",
        "bloco_3ps": "Equidade e Direitos Humanos",
        "status_reuniao": "Reunião Realizada",
        "processo_sei": "Verificar SEI",
        "responsavel": "Coordenação do Comitê de Equidade",
        "pauta_reuniao": "Políticas de inclusão, equidade de gênero e raça (E8.O1.KR2/KR3), coexecução das ações anuais de prevenção ao assédio (c/ Ouvidoria) e campanhas de sustentabilidade (E8.O1.KR1)."
    },
'''
    if '"CS": {' not in txt:
        txt = txt.replace('UNIT_META = {', 'UNIT_META = {\n' + meta_addition)

    # 2. Replace extract_relations with refined extract_relations_v2
    new_extract_relations = r'''UNIT_ALIASES = {
    "ASCOM": ["ASCOM", "Assessoria de Comunicação", "Comunicação"],
    "ASJUR": ["ASJUR", "Assessoria Jurídica", "Consultoria Geral", "Consultoria-Geral", "Assessoria Especial"],
    "CEQUIDADE": ["CEQUIDADE", "CDE", "Comitê de Equidade", "Equidade"],
    "CG": ["CG", "Corregedoria-Geral", "Corregedoria"],
    "CS": ["CS", "Conselho Superior da PGE", "Conselho Superior", "Conselho"],
    "CSL": ["CSL", "Comissão Setorial de Licitação", "Licitação"],
    "ESAP": ["ESAP", "Escola Superior da Advocacia Pública", "Escola Superior"],
    "GAB": ["GAB", "Gabinete do Procurador-Geral", "Gabinete"],
    "NC": ["NC", "NCALC", "Núcleo de Cálculos", "Cálculos"],
    "NCIA": ["NCIA", "Núcleo de Combate à Improbidade Administrativa", "Improbidade Administrativa"],
    "NIRF": ["NIRF", "Núcleo de Inteligência e Recuperação Fiscal", "Recuperação Fiscal"],
    "OUV": ["OUV", "Ouvidoria-Geral", "Ouvidoria"],
    "PA": ["PA", "Procuradoria Administrativa", "Administrativa"],
    "PB": ["PB", "Procuradoria de Brasília", "Brasília", "Brasilia"],
    "PCF": ["PCF", "Procuradoria do Contencioso Fiscal", "Contencioso Fiscal"],
    "PDA": ["PDA", "Procuradoria da Dívida Ativa", "Dívida Ativa"],
    "PEDU": ["PEDU", "Procuradoria da Educação", "Educação"],
    "PERJP": ["PERJP", "Procuradoria de Execuções", "Requisições Judiciais de Pagamento", "Execuções"],
    "PGA": ["PGA", "Procurador-Geral Adjunto", "Assuntos Administrativos"],
    "PGAAE": ["PGAAE", "Assuntos Estratégicos", "Assessoria em TIC da PGAAE", "INOVA"],
    "PGAAJ": ["PGAAJ", "Assuntos Jurídicos"],
    "PGARI": ["PGARI", "Relacionamento Institucional"],
    "PJ": ["PJ", "Procuradoria Judicial", "Judicial"],
    "PJEFP": ["PJEFP", "Juizados Especiais", "Turmas Recursais"],
    "PPIMA": ["PPIMA", "Patrimônio Imobiliário", "Meio Ambiente"],
    "PRI": ["PRI", "Regional de Imperatriz", "Imperatriz"],
    "PRT": ["PRT", "Regional de Timon", "Timon"],
    "PSAU": ["PSAU", "Procuradoria da Saúde", "Saúde"],
    "PSP": ["PSP", "Segurança Pública", "Segurança"],
    "PT": ["PT", "Procuradoria Trabalhista", "Trabalhista"],
    "SCC": ["SCC", "Controle de Contratos", "Contratos e Convênios"],
    "SCCF": ["SCCF", "Controle Contábil-Financeiro", "Controle Financeiro"],
    "SDD": ["SDD", "Digitalização e Distribuição"],
    "SEO": ["SEO", "Execução Orçamentária"],
    "SGA": ["SGA", "Subprocuradoria-Geral Adjunta"],
    "SGRH": ["SGRH", "Recursos Humanos"],
    "SGT": ["SGT", "Serviços Gerais e Transportes"],
    "SI": ["SI", "Supervisão de Informática", "Suporte de Infraestrutura: SI"],
    "SMP": ["SMP", "Material e Patrimônio"],
    "UGAM": ["UGAM", "Atividade Meio", "Unidade Gestora"],
    "USF": ["USF", "Unidade Setorial de Finanças", "Finanças"]
}


def extract_relations(sigla_origem: str, resp_text: str):
    """
    Analisa o campo 'Responsáveis (QUEM - Governança Saneada)' e extrai:
    - papel_unidade ('Líder', 'Articulador', 'Coexecutor', 'Fornecedor de Insumo / Apoio', 'Apoio / Usuário Piloto', 'Apoio Operacional')
    - lista de siglas relacionadas (unidades parceiras).
    """
    t = str(resp_text or "")
    aliases_origem = UNIT_ALIASES.get(sigla_origem, [sigla_origem])

    # 1. Articulador (ex: PGARI)
    if re.search(r"Articulador[a]?:\s*.*" + re.escape(sigla_origem), t, re.I) or (sigla_origem == "PGARI" and "Articulador" in t):
        papel = "Articulador"
    else:
        # Procurar menção a Líder
        m_lider = re.search(r"L[íi]der(?:es)?(?:\s+da\s+Meta)?:\s*([^;|\n]+)", t, re.IGNORECASE)
        if m_lider:
            lider_part = m_lider.group(1)
            # Verificar se a unidade de origem é quem lidera
            is_lider = any(
                re.search(rf"\b{re.escape(alias)}\b", lider_part, re.IGNORECASE) or (len(alias) > 4 and alias.lower() in lider_part.lower())
                for alias in aliases_origem
            )
            if is_lider:
                papel = "Líder"
            else:
                # Não é o líder principal: classificar papel secundário
                if any(k in t.lower() for k in ["fornecedor de insumo", "fornecedor de resposta", "insumo", "apoio operacional"]):
                    papel = "Fornecedor de Insumo / Apoio"
                elif any(k in t.lower() for k in ["usuário piloto", "usuario piloto", "demandante", "triagem na origem", "levantamento"]):
                    papel = "Apoio / Usuário Piloto"
                elif any(k in t.lower() for k in ["coexecutor", "coordenação", "coexecutores"]):
                    papel = "Coexecutor"
                else:
                    papel = "Apoio Operacional"
        else:
            # Sem campo Líder formal
            if any(k in t.lower() for k in ["coexecutores:", "coexecutor:"]):
                papel = "Coexecutor"
            elif any(k in t.lower() for k in ["fornecedor"]):
                papel = "Fornecedor de Insumo / Apoio"
            elif any(k in t.lower() for k in ["apoio"]):
                papel = "Apoio Operacional"
            else:
                papel = "Líder"

    # Mapear parceiros citados
    parceiros = []
    for sig, aliases in UNIT_ALIASES.items():
        if sig == sigla_origem:
            continue
        for al in aliases:
            if re.search(rf"\b{re.escape(al)}\b", t, re.IGNORECASE) or (len(al) > 4 and al.lower() in t.lower()):
                parceiros.append(sig)
                break

    return papel, sorted(set(parceiros))
'''
    txt = re.sub(r'def extract_relations\(.*?\n(?=def init_db_and_sync_from_xlsx|\n# FastAPI App)', lambda m: new_extract_relations + '\n\n', txt, flags=re.DOTALL)

    # 3. Patch get_relatorios_dados to include unidades_lideres and unidades_apoio
    old_metas_query = '''    # 2. Lista de Objetivos e Metas (KRs)
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
        })'''

    new_metas_query = '''    # 2. Lista de Objetivos e Metas (KRs)
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
            GROUP_CONCAT(DISTINCT CASE WHEN papel_unidade = 'Líder' THEN sigla_unidade END) as unidades_lideres,
            GROUP_CONCAT(DISTINCT CASE WHEN papel_unidade != 'Líder' THEN sigla_unidade END) as unidades_apoio,
            GROUP_CONCAT(DISTINCT sigla_unidade) as unidades
        FROM acoes
        WHERE kr_codigo != 'SEM_CODIGO'
        GROUP BY kr_codigo
        ORDER BY kr_codigo ASC
    """).fetchall()

    objetivos_metas = []
    for r in metas_raw:
        unids = sorted(set((r["unidades"] or "").split(","))) if r["unidades"] else []
        lids = sorted(set((r["unidades_lideres"] or "").split(","))) if r["unidades_lideres"] else []
        apos = sorted(set((r["unidades_apoio"] or "").split(","))) if r["unidades_apoio"] else []
        objetivos_metas.append({
            "eixo_cod": r["eixo_cod"],
            "obj_cod": r["obj_cod"],
            "kr_codigo": r["kr_codigo"],
            "eixo_nome": r["eixo_nome"],
            "objetivo_nome": r["objetivo_nome"],
            "kr_texto_completo": r["kr_texto_completo"],
            "pilar_3ps": r["pilar_3ps"],
            "qtd_acoes": r["qtd_acoes"],
            "unidades": unids,
            "unidades_lideres": lids,
            "unidades_apoio": apos
        })'''

    if old_metas_query in txt:
        txt = txt.replace(old_metas_query, new_metas_query)

    # 4. Patch exportar_relatorio(tipo == "quadro-metas-unidade")
    # In quadro-metas-unidade, ensure acoes_u filters for papel_unidade == "Líder"
    old_quadro = '''        if sigla:
            u_info = next((u for u in unidades_meta if u["sigla"] == sigla), None)
            u_nome = u_info["nome"] if u_info else sigla
            acoes_u = [a for a in all_acoes if a["sigla_unidade"] == sigla]

            krs_dict = {}'''

    new_quadro = '''        if sigla:
            u_info = next((u for u in unidades_meta if u["sigla"] == sigla), None)
            u_nome = u_info["nome"] if u_info else sigla
            # Metodologia Saneada: Relatório 8 exibe exclusivamente Metas (KRs) com Liderança Direta da unidade
            acoes_u = [a for a in all_acoes if a["sigla_unidade"] == sigla and a["papel_unidade"] == "Líder"]
            if not acoes_u:
                acoes_u = [a for a in all_acoes if a["sigla_unidade"] == sigla]

            krs_dict = {}'''

    if old_quadro in txt:
        txt = txt.replace(old_quadro, new_quadro)

    # Also in Consolidado Geral of quadro-metas-unidade, clarify Unidades Líderes
    old_quadro_geral = '''        else:
            headers = [
                "Eixo Estratégico", "Cód. Objetivo", "Objetivo Estratégico",
                "Cód. KR", "Meta / Resultado-Chave (KR)",
                "Total de Ações", "Unidades Vinculadas"
            ]
            rows_data = [
                [
                    f"{m['eixo_cod']} – {m['eixo_nome']}",
                    m["obj_cod"],
                    m["objetivo_nome"],
                    m["kr_codigo"],
                    m["kr_texto_completo"],
                    m["qtd_acoes"],
                    ", ".join(m["unidades"])
                ]
                for m in metas_master
            ]'''

    new_quadro_geral = '''        else:
            headers = [
                "Eixo Estratégico", "Cód. Objetivo", "Objetivo Estratégico",
                "Cód. KR", "Meta / Resultado-Chave (KR)",
                "Total de Ações", "Unidade(s) Líder(es)", "Unidades de Apoio / Coexecução"
            ]
            rows_data = [
                [
                    f"{m['eixo_cod']} – {m['eixo_nome']}",
                    m["obj_cod"],
                    m["objetivo_nome"],
                    m["kr_codigo"],
                    m["kr_texto_completo"],
                    m["qtd_acoes"],
                    ", ".join(m.get("unidades_lideres", [])) or ", ".join(m["unidades"]),
                    ", ".join(m.get("unidades_apoio", [])) or "Nenhuma (Execução Direta)"
                ]
                for m in metas_master
            ]'''

    if old_quadro_geral in txt:
        txt = txt.replace(old_quadro_geral, new_quadro_geral)

    BACKEND_PATH.write_text(txt, encoding="utf-8")
    print("backend.py successfully patched.")


def patch_frontend():
    print("Patching index.html...")
    txt = INDEX_PATH.read_text(encoding="utf-8")

    old_preview_quadro = '''          const uInfo = unidsMeta.find(u => u.sigla === sigla) || {};
          const acoesU = allAcoes.filter(a => a.sigla_unidade === sigla);

          const krsDict = {};'''

    new_preview_quadro = '''          const uInfo = unidsMeta.find(u => u.sigla === sigla) || {};
          // Metodologia Saneada: Exibir no Quadro de Metas apenas KRs de Liderança Direta da unidade
          let acoesU = allAcoes.filter(a => a.sigla_unidade === sigla && a.papel_unidade === 'Líder');
          if (acoesU.length === 0) {
            acoesU = allAcoes.filter(a => a.sigla_unidade === sigla);
          }

          const krsDict = {};'''

    if old_preview_quadro in txt:
        txt = txt.replace(old_preview_quadro, new_preview_quadro)

    old_sub_title = "subEl.textContent = `Estrutura Estratégica: ${krsList.length} Metas (KRs) Vinculadas`;"
    new_sub_title = "subEl.textContent = `Estrutura Estratégica: ${krsList.length} Metas Finalísticas (Liderança Direta da Unidade)`;"
    if old_sub_title in txt:
        txt = txt.replace(old_sub_title, new_sub_title)

    INDEX_PATH.write_text(txt, encoding="utf-8")
    print("index.html successfully patched.")

if __name__ == "__main__":
    patch_backend()
    patch_frontend()
