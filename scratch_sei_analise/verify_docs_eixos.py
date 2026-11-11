import json

with open('docs/dados_sgpe.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Overview total acoes:', d['overview']['total_acoes'])

eixos = set(a['eixo'] for a in d['acoes'])
print(f'Distinct eixos count: {len(eixos)}')
for e in sorted(eixos):
    print(f'  {e}')

e4_objs = set(a['objetivo'] for a in d['acoes'] if 'E4' in a['kr_codigo'])
print('E4 objetivos:', e4_objs)
