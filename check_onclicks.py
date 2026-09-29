with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Find all onclick attributes
onclicks = re.findall(r'onclick=[\"\\\']([^\"\\\']+)[\"\\\']', html)
print(f"Total onclick handlers in HTML: {len(onclicks)}")
unique_onclicks = sorted(list(set(onclicks)))
for oc in unique_onclicks:
    print(f"  - {oc}")

# Find all script functions
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js_code = script_match.group(1)
    with open('extracted_check.js', 'w', encoding='utf-8') as js_out:
        js_out.write(js_code)
    print("\nSaved extracted JS to extracted_check.js")
