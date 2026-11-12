import os
from pypdf import PdfReader

# Extract text of current PDF
pdf_path = r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.user_uploaded\media_1794487753003_24ff6296.pdf"
reader = PdfReader(pdf_path)
pdf_text = ""
for page in reader.pages:
    pdf_text += page.extract_text() + "\n"

# Distinct specific snippets from the PDF:
snippets = [
    "Relatório Prévio sobre Riscos Institucionais",
    "atualização do relatório de riscos institucionais apresentado no dia 10/10/2024",
    "GPS do Expediente",
    "Processo Administrativo no SPA por atraso",
    "treinamentos técnicos realizados pela COREPLAN",
    "cláusula contratual de transferência de conhecimento",
    "defasagem de 5 a 7 dias úteis e duplicidade de intimações",
    "índice de arrecadação da dívida ativa é um dos mais altos do país (3,02%)",
    "acordo de cooperação com a FAPEMA para auxílio na gestão documental",
    "mais de mil petições cadastradas em um mês no setor de Execuções",
    "PDF-PGE e CHAT-PGE",
    "unidade denominada “Arquivo” (ARQ/PGE)",
    "orçamento de R$ 100 mil é considerado insuficiente (cobre menos de 20 computadores)",
    "Hora Extra Especial para voluntários do INOVA",
    "sugeriram objetos de parceria com UEMA, UNDB e ATI",
    "paridade de gênero nas eleições de 2024 para possibilitar maior representatividade das mulheres no Conselho Superior",
    "banner institucional com QR Code",
    "proteger comitê e laboratórios",
    "limitada por lei a um teto salarial de R$ 3.000,00",
    "aumento para R$ 4.800,00",
    "nomear 11 procuradores do concurso de 2017",
    "parceria com a UEMA para obter a IA de precedentes judiciais",
    "Monitor PGE 1.0 para processos estratégicos",
    "ADI nº 7506",
    "PGE será responsável por processar o pagamento do RPV"
]

print(f"Total snippets to test: {len(snippets)}")

# Check in all md and txt files in the workspace
found_in_workspace = {}
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.md', '.txt', '.py', '.json', '.docx')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for snip in snippets:
                        if snip.lower() in content.lower():
                            if snip not in found_in_workspace:
                                found_in_workspace[snip] = []
                            found_in_workspace[snip].append(filepath)
            except Exception:
                pass

print(f"\nSnippets encontrados no workspace: {len(found_in_workspace)}")
for snip, files in found_in_workspace.items():
    print(f"\nSnippet: '{snip}'")
    for fp in list(set(files))[:5]:
        print(f"  -> {fp}")
