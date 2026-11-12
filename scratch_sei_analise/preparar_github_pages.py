# -*- coding: utf-8 -*-
"""
Prepara a aplicação SGPE PGE-MA para publicação na Web via GitHub Pages (pasta docs/)
e repositórios Cloud (Render/Railway), mantendo 100% de compatibilidade com o modo local FastAPI.
"""
import sys
sys.path.insert(0, '.')
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

    with open(static_json, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    with open(docs_json, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print(f"[OK] Bundle de dados exportado para:\n  - {static_json}\n  - {docs_json}")

    # Sincronizar index.html
    shutil.copy(APP_DIR / "static" / "index.html", DOCS_DIR / "index.html")
    print(f"[OK] index.html copiado para docs/")

    # Copiar planilhas consolidadas
    for f in CONS_DIR.glob("*.xlsx"):
        shutil.copy(f, DOCS_PLANILHAS / f.name)
    print(f"[OK] 41 planilhas consolidadas copiadas para docs/planilhas/")

    # Copiar exportações existentes
    app_exports = APP_DIR / "exports"
    if app_exports.exists():
        for f in app_exports.glob("*.*"):
            if f.is_file():
                shutil.copy(f, DOCS_EXPORTS / f.name)
            elif f.is_dir():
                dest_sub = DOCS_EXPORTS / f.name
                if dest_sub.exists():
                    shutil.rmtree(dest_sub)
                shutil.copytree(f, dest_sub)
        print(f"[OK] Exportações sincronizadas com docs/exports/")

    print("\n[SUCESSO] Build do GitHub Pages concluído com sucesso!")


if __name__ == "__main__":
    build_github_pages_bundle()
