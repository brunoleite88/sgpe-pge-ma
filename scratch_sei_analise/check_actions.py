import urllib.request
import json
import time

def check():
    url = f'https://brunoleite88.github.io/sgpe-pge-ma/index.html?v={int(time.time())}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            has_badge = 'v2.1 Saneado' in content
            print('Live index.html check -> v2.1 Saneado presente?', has_badge)
            return has_badge
    except Exception as e:
        print('Erro no check:', e)
        return False

for i in range(6):
    if check():
        print('PÁGINA DO GITHUB ATUALIZADA COM SUCESSO!')
        break
    print(f'Aguardando deploy do GitHub Pages (tentativa {i+1}/6)...')
    time.sleep(10)
