import urllib.request
import json
import time

url = f"https://brunoleite88.github.io/sgpe-pge-ma/dados_sgpe.json?v=test_{int(time.time())}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    acoes = data.get("acoes", [])
    pda_e9 = [a for a in acoes if a.get("kr_codigo") == "E9.O3.KR1" and a.get("sigla_unidade") == "PDA"]
    print("PDA papel em E9.O3.KR1:", pda_e9[0].get("papel_unidade") if pda_e9 else "Nao tem")
    print("PDA acao:", pda_e9[0].get("acao") if pda_e9 else "")
    print("PDA resp:", pda_e9[0].get("responsaveis") if pda_e9 else "")

    pda_e6 = [a for a in acoes if a.get("kr_codigo") == "E6.O1.KR2" and a.get("sigla_unidade") == "PDA"]
    print("\nPDA papel em E6.O1.KR2 (Redes Sociais):", pda_e6[0].get("papel_unidade") if pda_e6 else "Nao tem")

    ascom_e6 = [a for a in acoes if a.get("kr_codigo") == "E6.O1.KR2" and a.get("sigla_unidade") == "ASCOM"]
    print("ASCOM papel em E6.O1.KR2:", ascom_e6[0].get("papel_unidade") if ascom_e6 else "Nao tem")
