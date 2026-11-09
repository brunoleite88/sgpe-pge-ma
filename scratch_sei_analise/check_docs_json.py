import json

with open('docs/dados_sgpe.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Overview total acoes:', d['overview']['total_acoes'])
print('Acoes array length:', len(d['acoes']))

esap_acoes = [a for a in d['acoes'] if a['sigla_unidade'] == 'ESAP']
print('ESAP acoes:', len(esap_acoes))
esap_e8 = [a for a in esap_acoes if 'E8' in a['kr_codigo']]
print('ESAP E8:', len(esap_e8))

cs_acoes = [a for a in d['acoes'] if a['sigla_unidade'] == 'CS']
print('CS acoes:', len(cs_acoes))
for a in cs_acoes:
    print(f"  {a['kr_codigo']} | {a['papel_unidade']} | {a['acao'][:40]}")

pri_acoes = [a for a in d['acoes'] if a['sigla_unidade'] == 'PRI']
print('PRI acoes:', len(pri_acoes))
