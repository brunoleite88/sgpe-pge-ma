import urllib.request

url = "https://brunoleite88.github.io/sgpe-pge-ma/dados_sgpe.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Status:", resp.status)
        for h, v in resp.headers.items():
            if h.lower() in ['last-modified', 'etag', 'age', 'cache-control', 'x-github-request-id']:
                print(f"{h}: {v}")
except Exception as e:
    print(e)
