import json

transcript_path = r"C:\Users\brunogomes\.gemini\antigravity\brain\7c9c86a8-2a95-4d77-b258-f3fede0ce248\.system_generated\logs\transcript.jsonl"

steps_to_check = [195, 199, 242, 252, 270, 288, 322, 325, 341]

with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in steps_to_check:
            data = json.loads(line)
            print(f"\n{'='*20} STEP {idx} ({data.get('type')}, {data.get('source')}) {'='*20}")
            content = data.get('content', '')
            if isinstance(content, str):
                print(content[:500])
            else:
                print(str(content)[:500])
