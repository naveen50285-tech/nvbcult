with open("seed_nvb_cult_catalog.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace all unsplash image lists
replacements = {
    'nvb-tee-dream-plan-achieve': '/static/products/nvb-tee-dream-plan-achieve.jpg',
    'nvb-tee-golden-eye-horus': '/static/products/nvb-tee-golden-eye-horus.jpg',
    'nvb-tee-supima-obsidian-luxury': '/static/products/nvb-tee-supima-obsidian-luxury.jpg',
    'nvb-tee-cyberpunk-analog-drop': '/static/products/nvb-tee-cyberpunk-analog-drop.jpg',
    'nvb-elec-cyberdeck-anc-earbuds': '/static/products/nvb-elec-cyberdeck-anc-earbuds.jpg',
    'nvb-elec-magfast-65w-gan': '/static/products/nvb-elec-magfast-65w-gan.jpg',
    'nvb-elec-creator-soundtrack-mic': '/static/products/nvb-elec-creator-soundtrack-mic.jpg',
    'nvb-elec-chronosync-amoled-watch': '/static/products/nvb-elec-chronosync-amoled-watch.jpg'
}

import re
for pid, img_path in replacements.items():
    pattern = rf'("{pid}"[\s\S]*?"images":\s*\[)([\s\S]*?)(\])'
    match = re.search(pattern, text)
    if match:
        new_block = f'{match.group(1)}\n                "{img_path}"\n            {match.group(3)}'
        text = text[:match.start()] + new_block + text[match.end():]
        print(f"Patched {pid}")
    else:
        print(f"Could not find pattern for {pid}")

with open("seed_nvb_cult_catalog.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved updated seed_nvb_cult_catalog.py")
