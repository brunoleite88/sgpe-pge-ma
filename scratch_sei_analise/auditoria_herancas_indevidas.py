import sqlite3
import pandas as pd
from collections import defaultdict

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
c = conn.cursor()

# Get all units and their types
c.execute("SELECT sigla, nome, tipo, bloco_3ps FROM unidades ORDER BY sigla")
unidades = {r[0]: {"nome": r[1], "tipo": r[2], "bloco": r[3]} for r in c.fetchall()}

# Query all actions
c.execute("""
    SELECT sigla_unidade, ordem, eixo, objetivo, kr_codigo, kr_texto_completo, acao, subacao, responsaveis, papel_unidade
    FROM acoes
    ORDER BY sigla_unidade, ordem
""")
all_acoes = c.fetchall()

print(f"Total de ações no banco: {len(all_acoes)}")

# Map KRs by unit and role
unit_krs = defaultdict(lambda: defaultdict(list))
kr_units = defaultdict(lambda: defaultdict(list))

for r in all_acoes:
    sigla, ordem, eixo, obj, kr_cod, kr_full, acao, subacao, resp, papel = r
    unit_krs[sigla][kr_cod].append({
        "ordem": ordem, "acao": acao, "subacao": subacao, "resp": resp, "papel": papel
    })
    kr_units[kr_cod][papel].append((sigla, ordem, acao))

# Let's inspect anomalous Eixo combinations
print("\n" + "="*80)
print("AUDITORIA 1: UNIDADES E SEUS KRS NO EIXO 8 (Sustentabilidade, Equidade, Integridade)")
print("="*80)
for sigla, krs in sorted(unit_krs.items()):
    e8_krs = {k: v for k, v in krs.items() if k.startswith("E8")}
    if e8_krs:
        print(f"\n[{sigla}] {unidades[sigla]['nome']} ({unidades[sigla]['tipo']}):")
        for kr, acts in e8_krs.items():
            for a in acts:
                print(f"   - {kr} ({a['papel']}): #{a['ordem']} {a['acao'][:60]}")

print("\n" + "="*80)
print("AUDITORIA 2: UNIDADES E SEUS KRS NO EIXO 9 (Pessoas, Clima, Ergonomia, Copas)")
print("="*80)
for sigla, krs in sorted(unit_krs.items()):
    e9_krs = {k: v for k, v in krs.items() if k.startswith("E9.O1")}
    if e9_krs:
        print(f"\n[{sigla}] {unidades[sigla]['nome']} ({unidades[sigla]['tipo']}):")
        for kr, acts in e9_krs.items():
            for a in acts:
                print(f"   - {kr} ({a['papel']}): #{a['ordem']} {a['acao'][:60]}")

print("\n" + "="*80)
print("AUDITORIA 3: UNIDADES E SEUS KRS NO EIXO 3 (Orçamento, Captação, PROFISCO III)")
print("="*80)
for sigla, krs in sorted(unit_krs.items()):
    e3_krs = {k: v for k, v in krs.items() if k.startswith("E3")}
    if e3_krs:
        print(f"\n[{sigla}] {unidades[sigla]['nome']} ({unidades[sigla]['tipo']}):")
        for kr, acts in e3_krs.items():
            for a in acts:
                print(f"   - {kr} ({a['papel']}): #{a['ordem']} {a['acao'][:60]}")
