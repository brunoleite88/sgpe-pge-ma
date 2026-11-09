import openpyxl

def inspect_wb(path, name):
    print(f"\n{'='*20} {name} {'='*20}")
    wb = openpyxl.load_workbook(path, data_only=True)
    print("Sheets:", wb.sheetnames)
    for sname in wb.sheetnames:
        ws = wb[sname]
        print(f"\n--- Aba: {sname} (max_row={ws.max_row}, max_col={ws.max_column}) ---")
        for r in range(1, min(ws.max_row + 1, 15)):
            row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column + 1, 10))]
            if any(row_vals):
                print(f"Row {r}: {row_vals}")

inspect_wb(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193070_7c5de750.xlsx", "XLSX ASCOM")
inspect_wb(r"C:/Users/brunogomes/.gemini/antigravity/brain/7c9c86a8-2a95-4d77-b258-f3fede0ce248/.user_uploaded/media_1794232193094_723ee57e.xlsx", "XLSX OUVIDORIA")
