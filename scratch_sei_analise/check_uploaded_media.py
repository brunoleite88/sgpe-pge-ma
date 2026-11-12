from pypdf import PdfReader

for fname in ['media_1794232193095_ff3ec6d2.pdf', 'media_1794232193094_28987d20.pdf']:
    path = f"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/{fname}"
    reader = PdfReader(path)
    print(f"=== {fname} ({len(reader.pages)} páginas) ===")
    text = reader.pages[0].extract_text()
    print(text[:300])
