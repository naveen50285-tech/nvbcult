with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/api/' in l and '@app.' in l:
        print(f"{i+1}: {l.strip()}")
