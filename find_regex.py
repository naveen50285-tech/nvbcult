with open('static_script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/' in line and ('replace(' in line or 'match(' in line or 'test(' in line or 'RegExp' in line or '//' not in line.strip()[:2]):
        # check if it looks like a regex
        if 'replace(' in line or 'match(' in line:
            print(f"Line {i+1}: {line.strip()}")
