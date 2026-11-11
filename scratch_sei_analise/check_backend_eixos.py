import re

with open('sgpe_app/backend.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'Eixo[^"\n\']+', text)
print('Matches in backend.py:')
for m in set(matches):
    if any(f"Eixo {i}" in m or f"Eixo Estratégico {i}" in m for i in range(1, 10)):
        print(f"  {m}")
