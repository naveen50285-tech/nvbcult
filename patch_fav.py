with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_fav = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><defs><linearGradient id=\'g\' x1=\'0%\' y1=\'0%\' x2=\'100%\' y2=\'100%\'><stop offset=\'0%\' stop-color=\'%233b82f6\'/><stop offset=\'100%\' stop-color=\'%2306b6d4\'/></linearGradient></defs><rect width=\'100\' height=\'100\' rx=\'25\' fill=\'%230b1120\'/><path d=\'M25 75 L45 25 L55 25 L75 75 L62 75 L50 42 L38 75 Z\' fill=\'url(%23g)\'/><circle cx=\'50\' cy=\'32\' r=\'5\' fill=\'%2338bdf8\'/></svg>">'

new_fav = '''<link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="apple-touch-icon" href="/static/favicon.png">'''

if old_fav in html:
    html = html.replace(old_fav, new_fav)
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Replaced SVG favicon with official Next Vision Brand PNG favicon!")
else:
    print("Warning: old_fav not matched exactly")
