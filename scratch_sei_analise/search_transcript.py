import json

transcript_path = r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.system_generated\logs\transcript.jsonl"

matches = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        content = str(data.get('content', ''))
        thinking = str(data.get('thinking', ''))
        
        terms = [
            'riscos institucionais',
            'relatório prévio sobre riscos',
            'daniel blume',
            'rocha júnior',
            'adi 7506',
            'adi nº 7506',
            '10/10/2024',
            '10 de março de 2026'
        ]
        
        found = [t for t in terms if t in content.lower() or t in thinking.lower()]
        if found:
            matches.append((idx, data.get('type'), data.get('source'), found))

print(f"Total de steps com menções: {len(matches)}")
for m in matches[:20]:
    print(m)
