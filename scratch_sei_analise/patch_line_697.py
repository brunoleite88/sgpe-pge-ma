with open('sgpe_app/backend.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, l in enumerate(lines):
    if 'm_lider = re.search(' in l:
        lines[idx] = '        m_lider = re.search(r"L[íi]der(?:es)?(?:\\s+[^:;]+)?:\\s*([^;|\\n]+)", t, re.IGNORECASE)\n'
        print(f"Patched line {idx+1}")
        break

with open('sgpe_app/backend.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Saved!")
