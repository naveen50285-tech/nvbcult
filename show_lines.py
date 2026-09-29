with open('build_nvb_store.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'cart-drawer' in l or 'details-modal' in l or 'portal-view' in l or 'ai-chat' in l:
        print(f"{i+1}: {l.strip()[:100]}")
