import re

p = "sgpe_app/backend.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    '"pauta_reuniao": "Coordenação do Plano Anual de Capacitação (PAC - E9.O2.KR1), incluindo oficinas práticas de Oratória Forense e Simulação de Tribuna (demanda PJ/PB), Escuta Ativa e CNV (demanda OUV), Media Training (demanda ASCOM) e Direito Digital/IA (E7.O3.KR2)."',
    '"pauta_reuniao": "Coordenação do Plano Anual de Capacitação (PAC - E9.O2.KR1), incluindo oficinas práticas de Oratória Forense e Simulação de Tribuna (demanda PJ/PB), Escuta Ativa e CNV (demanda OUV), Media Training (demanda ASCOM) e Trilha Estratégica Prioritária de Direito Digital/IA (E9.O2.KR1)."'
)

text = text.replace(
    '"krs_vinculados": "E2.O1.KR2, E5.O5.KR1, E7.O3.KR2, E9.O1.KR1"',
    '"krs_vinculados": "E2.O1.KR2, E5.O5.KR1, E9.O2.KR1, E9.O1.KR1"'
)

text = text.replace(
    '"krs_vinculados": "E9.O2.KR1, E7.O3.KR2"',
    '"krs_vinculados": "E9.O2.KR1"'
)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("backend.py updated successfully!")
