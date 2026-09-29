import re

files_to_check = ['build_nvb_store.py', 'server.py', 'seed_nvb_cult_catalog.py', 'static/index.html']
for fn in files_to_check:
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            text = f.read()
        matches = set(re.findall(r'https?://[^\s\"\'\`<>]+', text))
        demo_urls = [u for u in matches if 'unsplash' in u or 'placeholder' in u or 'example.com' in u]
        print(f"=== {fn} (found {len(demo_urls)} demo URLs) ===")
        for u in demo_urls[:5]:
            print("  -", u)
    except Exception as e:
        print(f"Error {fn}: {e}")
