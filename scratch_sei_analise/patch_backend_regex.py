p = "sgpe_app/backend.py"
with open(p, "rb") as f:
    data = f.read()

target = b'm_lider = re.search(r"L[\xc3\xad\xc3\x8di]der(?:es)?(?:\s+da\s+Meta)?:\s*([^;|\n]+)", t, re.IGNORECASE)'
# Let's check with str
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

old_s = 'm_lider = re.search(r"L[íi]der(?:es)?(?:\s+da\s+Meta)?:\s*([^;|\n]+)", t, re.IGNORECASE)'
new_s = 'm_lider = re.search(r"L[íi]der(?:es)?(?:\s+[^:;]+)?:\s*([^;|\n]+)", t, re.IGNORECASE)'

assert old_s in text, "old_s not found"
text = text.replace(old_s, new_s, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("backend regex patched successfully!")
