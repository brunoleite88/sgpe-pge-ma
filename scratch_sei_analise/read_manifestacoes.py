import pypdf

def read_pdf(path, label):
    print(f"\n{'='*20} {label} {'='*20}")
    reader = pypdf.PdfReader(path)
    print(f"Total páginas: {len(reader.pages)}")
    full_text = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"--- Página {idx+1} ---")
        print(text)
        full_text.append(text)
    return "\n".join(full_text)

pdf_ascom = r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193095_ff3ec6d2.pdf"
pdf_ouv = r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193094_28987d20.pdf"

read_pdf(pdf_ascom, "MANIFESTAÇÃO 20 - ASCOM")
read_pdf(pdf_ouv, "MANIFESTAÇÃO 19 - OUVIDORIA")
