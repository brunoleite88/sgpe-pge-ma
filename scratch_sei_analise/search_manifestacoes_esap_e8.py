import re
import os
from pathlib import Path
import pypdf

# Check all text in scratch_sei_analise/ascom_manifestacao_text.txt and ouv_manifestacao_text.txt
for fname in ["ascom_manifestacao_text.txt", "ouv_manifestacao_text.txt"]:
    p = Path("scratch_sei_analise") / fname
    if p.exists():
        t = p.read_text(encoding="utf-8")
        matches = [line for line in t.split("\n") if "ESAP" in line.upper() or "ESCOLA" in line.upper()]
        print(f"\n=== Menções à ESAP em {fname} ({len(matches)} linhas) ===")
        for m in matches[:10]:
            print("  *", m.strip())

# Check all user uploaded files in the conversation artifacts
user_up = Path(r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.user_uploaded")
if user_up.exists():
    for f in user_up.glob("*"):
        print(f"Uploaded file: {f.name}")
        if f.suffix == ".pdf":
            try:
                reader = pypdf.PdfReader(f)
                txt = " ".join(page.extract_text() or "" for page in reader.pages)
                m = re.findall(r'.{0,80}(?:ESAP|Escola Superior).{0,80}', txt, re.IGNORECASE)
                if m:
                    print(f"  -> {len(m)} menções à ESAP em {f.name}:")
                    for match in m[:5]:
                        print("     -", match.strip())
            except Exception as e:
                pass
