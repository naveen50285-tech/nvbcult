with open('dom_dump.html', 'r', encoding='utf-8') as f:
    dom = f.read()

import re
grid = re.search(r'id=[\"\']products-grid[\"\'][^>]*>(.*?)</div>\s*</div>', dom, re.DOTALL)
if grid:
    content = grid.group(1).strip()
    print("products-grid inner length:", len(content))
    cards = re.findall(r'class=[\"\'][^\"\']*product-card[^\"\']*[\"\']', content)
    print(f"Rendered product cards count: {len(cards)}")
    if len(cards) == 0:
        print("First 500 chars of grid:", content[:500])
else:
    print("products-grid NOT FOUND in DOM dump!")
