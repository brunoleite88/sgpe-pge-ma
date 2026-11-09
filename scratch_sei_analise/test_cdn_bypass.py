import urllib.request
import json

url = f"https://brunoleite88.github.io/sgpe-pge-ma/dados_sgpe.json?v=test_{int(urllib.request.time.time())}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        for h, v in resp.headers.items():
            if h.lower() in ['last-modified', 'etag', 'age']:
                print(f"{h}: {v}")
        acoes = data.get("acoes", [])
        print("Total acoes:", len(acoes))
        cs_e9 = [a for a in acoes if a.get("kr_codigo") == "E9.O3.KR1" and a.get("sigla_unidade") == "CS"]
        print("CS tem E9.O3.KR1?", len(cs_e9) > 0)
except Exception as e:
    print(e)
