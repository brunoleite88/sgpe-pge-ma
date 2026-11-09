import pypdf

def extract_all(path):
    reader = pypdf.PdfReader(path)
    return "\n".join(page.extract_text() for page in reader.pages)

t_ascom = extract_all(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193095_ff3ec6d2.pdf")
t_ouv = extract_all(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193094_28987d20.pdf")

with open("scratch_sei_analise/ascom_manifestacao_text.txt", "w", encoding="utf-8") as f:
    f.write(t_ascom)

with open("scratch_sei_analise/ouv_manifestacao_text.txt", "w", encoding="utf-8") as f:
    f.write(t_ouv)

print("Text files saved successfully!")
