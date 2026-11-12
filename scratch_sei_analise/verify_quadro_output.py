with open('docs/exports/Quadro_Eixos_Objetivos_Metas_PCF.md', 'r', encoding='utf-8') as f:
    text_pcf = f.read()

print("=== QUADRO DE METAS PCF ===")
print("E5.O5 no Quadro PCF?", "E5.O5" in text_pcf)
lines_pcf = [l for l in text_pcf.split('\n') if '| E' in l]
print(f"Total metas no quadro da PCF: {len(lines_pcf)}")
for l in lines_pcf:
    print(" ", l[:90])

with open('docs/exports/Quadro_Eixos_Objetivos_Metas_PDA.md', 'r', encoding='utf-8') as f:
    text_pda = f.read()

print("\n=== QUADRO DE METAS PDA ===")
print("E5.O5 no Quadro PDA?", "E5.O5" in text_pda)
lines_pda = [l for l in text_pda.split('\n') if '| E' in l]
print(f"Total metas no quadro da PDA: {len(lines_pda)}")
for l in lines_pda:
    print(" ", l[:90])
