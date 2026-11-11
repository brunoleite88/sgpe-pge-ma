with open('Cotejamento_Consolidado_Metas_Acoes_PGE_MA.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.split('\n')
for idx, line in enumerate(lines):
    if any(f"Eixo Estratégico {i}" in line or f"**Eixo {i}**" in line for i in range(1, 10)):
        print(f"Line {idx+1}: {line}")
