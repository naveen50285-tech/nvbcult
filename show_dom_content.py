with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
pos = html.find('addEventListener("DOMContentLoaded"')
if pos != -1:
    print(html[pos:pos+1500])
else:
    pos2 = html.find("DOMContentLoaded")
    print("Found DOMContentLoaded at", pos2)
    if pos2 != -1:
        print(html[pos2-30:pos2+1000])
