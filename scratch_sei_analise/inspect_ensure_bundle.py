with open('sgpe_app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function ensureStaticBundle')
print(text[idx-50:idx+600])
