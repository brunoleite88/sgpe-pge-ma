import re

with open('docs/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'Eixo Estratégico \d[^<"\']+', text)
print('Matches in docs/index.html:')
for m in set(matches):
    print(f"  {m}")
