# -*- coding: utf-8 -*-
"""
Prepara a aplicação SGPE PGE-MA para publicação na Web via GitHub Pages (pasta docs/)
e repositórios Cloud (Render/Railway), mantendo 100% de compatibilidade com o modo local FastAPI.
"""
import json
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from sgpe_app.backend import app, BASE_DIR, CONS_DIR, APP_DIR

DOCS_DIR = BASE_DIR / "docs"
DOCS_PLANILHAS = DOCS_DIR / "planilhas"
DOCS_EXPORTS = DOCS_DIR / "exports"


def build_github_pages_bundle():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_PLANILHAS.mkdir(parents=True, exist_ok=True)
    DOCS_EXPORTS.mkdir(parents=True, exist_ok=True)

    client = TestClient(app)

    overview = client.get("/api/overview").json()
    acoes = client.get("/api/acoes").json()
    matriz_3ps = client.get("/api/3ps").json()
    relacoes = client.get("/api/relacoes").json()
    gts = client.get("/api/gts").json()
    relatorios = client.get("/api/relatorios/dados").json()

    minutas_por_unidade = {}
    for u in overview["unidades"]:
        sig = u["sigla"]
        minutas_por_unidade[sig] = client.get(f"/api/unidades/{sig}/minutas").json()

    bundle = {
        "overview": overview,
        "acoes": acoes,
        "matriz_3ps": matriz_3ps,
        "relacoes": relacoes,
        "gts": gts,
        "relatorios": relatorios,
        "minutas": minutas_por_unidade,
    }

    # Salvar bundle JSON em sgpe_app/static e em docs/
    static_json = APP_DIR / "static" / "dados_sgpe.json"
    docs_json = DOCS_DIR / "dados_sgpe.json"
    json_bytes = json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
    static_json.write_bytes(json_bytes)
    docs_json.write_bytes(json_bytes)

    # Copiar as 41 planilhas .xlsx consolidadas para docs/planilhas/
    count_xlsx = 0
    for f in CONS_DIR.glob("Plano_Acao_Pos_Comparacao_*.xlsx"):
        shutil.copy2(f, DOCS_PLANILHAS / f.name)
        count_xlsx += 1

    # Pré-gerar os principais relatórios em docs/exports/ para download instantâneo no GitHub Pages
    tipos_rel = [
        "mapa-estrategico",
        "objetivos-metas",
        "planos-acao",
        "matriz-responsabilidades",
        "cronograma-entregas",
        "relatorio-gt",
    ]
    for t in tipos_rel:
        for fmt in ("xlsx", "docx", "md"):
            res = client.get(f"/api/export/{t}?fmt={fmt}")
            if res.status_code == 200:
                (DOCS_EXPORTS / f"{t}.{fmt}").write_bytes(res.content)

    # Pré-gerar fichas de pactuação das 41 unidades em .xlsx, .docx e .md
    DOCS_FICHAS = DOCS_EXPORTS / "fichas"
    DOCS_FICHAS.mkdir(parents=True, exist_ok=True)
    for u in overview["unidades"]:
        sig = u["sigla"]
        for fmt in ("xlsx", "docx", "md"):
            res = client.get(f"/api/export/ficha-pactuacao?fmt={fmt}&sigla={sig}")
            if res.status_code == 200:
                (DOCS_FICHAS / f"Ficha_Pactuacao_Setorial_{sig}.{fmt}").write_bytes(res.content)

    # Copiar index.html atualizado para docs/index.html e criar .nojekyll
    shutil.copy2(APP_DIR / "static" / "index.html", DOCS_DIR / "index.html")
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")

    # Criar requirements.txt na raiz para deploy opcional em Render/Railway/PythonAnywhere
    (BASE_DIR / "requirements.txt").write_text(
        "fastapi>=0.110.0\nuvicorn>=0.28.0\nopenpyxl>=3.1.2\npython-docx>=1.1.0\npydantic>=2.6.0\n",
        encoding="utf-8"
    )

    print(f"Bundle JSON gerado ({len(json_bytes)//1024} KB), {count_xlsx} planilhas e relatórios exportados em docs/!")


if __name__ == "__main__":
    build_github_pages_bundle()
