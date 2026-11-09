import pypdf

reader = pypdf.PdfReader(r"Escola Superior da Advocacia Pública (ESAP)/Escola Superior da Advocacia Pública (ESAP) - Eixos Objetivos e Metas (KRs).pdf")
print(f"Total pages: {len(reader.pages)}")
for idx, page in enumerate(reader.pages):
    print(f"--- Page {idx+1} ---")
    print(page.extract_text())
