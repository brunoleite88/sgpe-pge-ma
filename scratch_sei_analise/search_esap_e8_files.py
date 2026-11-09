import os
from pathlib import Path

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".md", ".txt", ".json")):
            p = Path(root) / f
            try:
                txt = p.read_text(encoding="utf-8")
                if "ESAP" in txt and ("manifestação" in txt.lower() or "sei" in txt.lower() or "reunião" in txt.lower()):
                    lines = [l for l in txt.split("\n") if "ESAP" in l and any(k in l.lower() for k in ["eixo 8", "e8", "resíduos", "recicláveis", "equidade"])]
                    if lines:
                        print(f"File: {p} -> {len(lines)} matches:")
                        for l in lines[:5]:
                            print("   ", l.strip()[:120])
            except Exception:
                pass
