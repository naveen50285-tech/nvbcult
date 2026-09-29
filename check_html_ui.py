import re

with open('static/index.html', encoding='utf-8') as f:
    html = f.read()

overlays = re.findall(r'<div[^>]*id="[^"]*modal[^"]*"[^>]*>', html)
for o in overlays:
    print("Modal:", o)

drawers = re.findall(r'<div[^>]*id="[^"]*drawer[^"]*"[^>]*>', html)
for d in drawers:
    print("Drawer:", d)

# Check inline onclick handlers
onclicks = re.findall(r'onclick="([^"]+)"', html)
print(f"Total onclick handlers: {len(onclicks)}")
print("Unique handlers:", set([c.split('(')[0] for c in onclicks]))
