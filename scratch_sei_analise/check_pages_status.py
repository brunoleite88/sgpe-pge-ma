with open('docs/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'dados_sgpe\.json[^\"]*', text)
print('dados_sgpe references in docs/index.html:', matches)

if "papel_unidade === 'Líder'" in text:
    print("Filter papel_unidade === Líder IS in docs/index.html")
else:
    print("WARNING: Filter papel_unidade === Líder is NOT in docs/index.html!")

# Check if browser cache-busting is present
print("\n--- Checking fetch in docs/index.html ---")
for line in text.split("\n"):
    if "dados_sgpe.json" in line or "api/relatorios/dados" in line:
        print("  ", line.strip())
