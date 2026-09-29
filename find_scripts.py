with open('build_nvb_store.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all script tag content in build_nvb_store.py
scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
print(f"Found {len(scripts)} script tags")
for i, s in enumerate(scripts):
    print(f"Script {i} length: {len(s)}")
    # Find all function definitions in the script
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', s)
    print(f"Functions defined in script {i}: {funcs}")
