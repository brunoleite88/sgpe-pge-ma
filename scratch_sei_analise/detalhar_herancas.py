import sqlite3
import pandas as pd

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')

def inspect_actions(title, query):
    print(f"\n{'='*20} {title} {'='*20}")
    df = pd.read_sql_query(query, conn)
    for idx, r in df.iterrows():
        print(f"[{r['sigla_unidade']}] {r['kr_codigo']} | {r['papel_unidade']} | Ação #{r['ordem']}: {r['acao'][:80]} | Sub: {str(r['subacao'])[:50]}")

# 1. ESAP detailed actions outside education (E3, E6, E7, E8, E9.O1)
inspect_actions("ESAP NO EIXO 8 E EIXO 9.O1 E EIXO 6", 
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE sigla_unidade = 'ESAP' AND (eixo LIKE '%8%' OR kr_codigo LIKE 'E9.O1%' OR kr_codigo LIKE 'E6%') ORDER BY kr_codigo, ordem")

# 2. Conselho Superior (CS) actions
inspect_actions("CONSELHO SUPERIOR (CS) - TODAS AS AÇÕES",
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE sigla_unidade = 'CS' ORDER BY kr_codigo, ordem")

# 3. UGAM in Eixo 8
inspect_actions("UGAM NO EIXO 8",
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE sigla_unidade = 'UGAM' AND eixo LIKE '%8%' ORDER BY kr_codigo, ordem")

# 4. CEQUIDADE in Eixo 8
inspect_actions("CEQUIDADE NO EIXO 8",
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE sigla_unidade = 'CEQUIDADE' AND eixo LIKE '%8%' ORDER BY kr_codigo, ordem")

# 5. PRI e PRT actions in E4, E5.O3, E5.O6, E7
inspect_actions("PRI E PRT EM E4, E5.O3, E5.O6, E7 (AMOSTRA)",
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE sigla_unidade IN ('PRI', 'PRT') AND (kr_codigo LIKE 'E4%' OR kr_codigo IN ('E5.O3.KR2', 'E5.O6.KR1', 'E7.O1.KR1', 'E7.O3.KR1')) ORDER BY sigla_unidade, kr_codigo, ordem")

# 6. E6.O2.KR1 - who has it and what is it?
inspect_actions("E6.O2.KR1 - QUEM TEM E QUAL O TEXTO",
    "SELECT sigla_unidade, kr_codigo, papel_unidade, ordem, acao, subacao FROM acoes WHERE kr_codigo = 'E6.O2.KR1' ORDER BY sigla_unidade, ordem")
