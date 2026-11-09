from scratch_sei_analise.saneamento_ascom_e_ti import load_rows, write_sheet_to_all_targets
from pathlib import Path

BASE_DIR = Path("Planilhas_Pos_Comparacao_Consolidadas")

for sigla in ["ASCOM", "OUV"]:
    p = BASE_DIR / f"Plano_Acao_Pos_Comparacao_{sigla}.xlsx"
    rows, t1, t2 = load_rows(p)
    changed = False
    for r in rows:
        if "E9.O2.KR1" in str(r[2] or ""):
            r[5] = f"Líder da Meta Institucional: Escola Superior da Advocacia Pública (ESAP) e SGRH; Demandante Setorial no PAC: {sigla}"
            changed = True
    if changed:
        write_sheet_to_all_targets(sigla, t1, t2, rows)
        print(f"{sigla} alinhada em E9.O2.KR1.")
