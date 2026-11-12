import os
import glob

search_terms = [
    'RELATÓRIO PRÉVIO SOBRE RISCOS INSTITUCIONAIS',
    'Relatório Prévio sobre Riscos Institucionais',
    'Daniel Blume',
    'Antonio Carlos da Rocha Júnior',
    'ADI 7506',
    'ADI nº 7506',
    'GPS do Expediente',
    'Hora Extra Especial para voluntários do INOVA',
    '10 de Março de 2026',
    '10/10/2024',
    'FAPEMA para auxílio na gestão documental',
    'paridade de gênero nas eleições de 2024',
    'nomear 11 procuradores do concurso de 2017'
]

matches = {}
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.md', '.txt', '.py', '.json', '.docx')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for term in search_terms:
                        if term.lower() in content.lower():
                            if term not in matches:
                                matches[term] = []
                            matches[term].append(filepath)
            except Exception:
                pass

print('Resultados encontrados no workspace:')
for term, fpaths in matches.items():
    print(f'Termo "{term}":')
    for fp in list(set(fpaths))[:10]:
        print(f'  - {fp}')
if not matches:
    print('Nenhum termo encontrado no workspace!')
