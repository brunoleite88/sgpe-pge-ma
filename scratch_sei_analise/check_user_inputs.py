import json

transcript_path = r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.system_generated\logs\transcript.jsonl"

user_inputs = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT':
            content = data.get('content', '')
            media = data.get('media', [])
            user_inputs.append((idx, content[:150], [m.get('uri') for m in media] if media else []))

print(f"Total user inputs: {len(user_inputs)}")
for idx, text, media in user_inputs:
    print(f"Step {idx}: {text!r} | Media: {media}")
