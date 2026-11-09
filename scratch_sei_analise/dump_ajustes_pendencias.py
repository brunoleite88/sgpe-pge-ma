import openpyxl

def dump_sheet(path, sname):
    print(f"\n{'='*20} {path} -> {sname} {'='*20}")
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
        if any(vals):
            print(f"L{r}: {vals}")

dump_sheet(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193070_7c5de750.xlsx", "Ajustes e Pendências")
dump_sheet(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193094_723ee57e.xlsx", "Ajustes e Pendências")
dump_sheet(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193094_723ee57e.xlsx", "Inclusões a deliberar")
