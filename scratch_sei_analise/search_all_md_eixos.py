import glob

old_titles = [
    "Incrementar a arrecadação e otimizar a cobrança da dívida ativa",
    "Incrementar a recuperação de créditos e a defesa do erário",
    "Incrementar e executar integralmente o orçamento institucional",
    "Melhorar a experiência do usuário dos serviços da PGE",
    "Alcançar maior eficiência e resolutividade nos processos internos e externos",
    "Aperfeiçoar a atuação contenciosa e consultiva com foco na resolutividade",
    "Fortalecer a imagem institucional e a comunicação com a sociedade",
    "Promover a transformação digital e a inovação tecnológica",
    "Fomentar a sustentabilidade, a integridade e a responsabilidade social",
    "Valorizar, integrar e qualificar servidores e procuradores"
]

for fpath in glob.glob("*.md"):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    found = [t for t in old_titles if t in content]
    if found:
        print(f"{fpath}: {len(found)} ocorrências encontradas -> {found}")
