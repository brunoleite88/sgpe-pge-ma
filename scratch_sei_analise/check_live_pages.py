import urllib.request
import json

url = "https://brunoleite88.github.io/sgpe-pge-ma/dados_sgpe.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("HTTP Status: 200")
        acoes = data.get("acoes", [])
        print("Total acoes on github.io:", len(acoes))
        # Check E9.O3.KR1 in acoes on github.io
        cs_e9 = [a for a in acoes if a.get("kr_codigo") == "E9.O3.KR1" and a.get("sigla_unidade") == "CS"]
        print("CS tem E9.O3.KR1 no github.io?", len(cs_e9) > 0)
        pda_e9 = [a for a in acoes if a.get("kr_codigo") == "E9.O3.KR1" and a.get("sigla_unidade") == "PDA"]
        if pda_e9:
            print("PDA papel em E9.O3.KR1 no github.io:", pda_e9[0].get("papel_unidade"))
except Exception as e:
    print("Error fetching github.io:", e)
