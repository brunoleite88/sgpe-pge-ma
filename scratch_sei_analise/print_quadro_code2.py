with open('sgpe_app/backend.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 122179
print(text[pos-2500:pos-1000])
