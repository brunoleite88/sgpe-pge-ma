import sqlite3
import json

conn = sqlite3.connect('sgpe_app/sgpe_pge_ma.db')
cursor = conn.cursor()

def search_text(keywords):
    results = []
    for kw in keywords:
        cursor.execute("""
            SELECT sigla_unidade, kr_codigo, acao, subacao, prazo, papel_unidade 
            FROM acoes 
            WHERE LOWER(acao) LIKE ? OR LOWER(subacao) LIKE ? OR LOWER(kr_texto_completo) LIKE ?
        """, (f"%{kw.lower()}%", f"%{kw.lower()}%", f"%{kw.lower()}%"))
        results.extend(cursor.fetchall())
    # deduplicate by (sigla, kr, acao)
    unique = {}
    for r in results:
        key = (r[0], r[1], r[2])
        if key not in unique:
            unique[key] = r
    return list(unique.values())

print("=== 1. HONORARIOS DATIVOS & RPV ===")
res1 = search_text(['dativo', 'bacelar', 'rpv'])
print(f"Total: {len(res1)}")
for r in res1[:10]:
    print(f"[{r[0]}] {r[1]} | {r[2][:60]} | {(r[3] or '')[:60]}")

print("\n=== 2. SPA, PJE, MNI, PRAZOS, D-3 ===")
res2 = search_text(['pje', 'delay', 'intima', 'preclus', 'prazo judicial', 'mni', 'd-3'])
print(f"Total: {len(res2)}")
for r in res2[:10]:
    print(f"[{r[0]}] {r[1]} | {r[2][:60]} | {(r[3] or '')[:60]}")

print("\n=== 3. INFRAESTRUTURA, ZABBIX, HYPERCONV, BACKUP, COREPLAN, ATI ===")
res3 = search_text(['zabbix', 'nutanix', 'vxrail', 'vmware', 'ati', 'coreplan', 'sala cofre', 'veeam', 'contingenc', 'disaster'])
print(f"Total: {len(res3)}")
for r in res3[:10]:
    print(f"[{r[0]}] {r[1]} | {r[2][:60]} | {(r[3] or '')[:60]}")

print("\n=== 4. SEGURANCA DA INFORMACAO, LGPD, IA SOBERANA, NIMBUS, ALEXANDRIA ===")
res4 = search_text(['lgpd', 'vlan', 'segurança da informação', 'privilégio mínimo', 'alexandria', 'nimbus', 'procuradoria-pdf', 'soberan'])
print(f"Total: {len(res4)}")
for r in res4[:10]:
    print(f"[{r[0]}] {r[1]} | {r[2][:60]} | {(r[3] or '')[:60]}")

print("\n=== 5. GESTAO DE CRISE, PROTOCOLO, POPS, GOVERNANCA DE TIC ===")
res5 = search_text(['crise', 'pop', 'procedimento operacional', 'governança de tic', 'comitê de governança'])
print(f"Total: {len(res5)}")
for r in res5[:10]:
    print(f"[{r[0]}] {r[1]} | {r[2][:60]} | {(r[3] or '')[:60]}")
