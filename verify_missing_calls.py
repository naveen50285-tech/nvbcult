with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find all function names defined in script
funcs_defined = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
funcs_assigned = set(re.findall(r'([a-zA-Z0-9_]+)\s*=\s*function', html))
funcs_arrow = set(re.findall(r'const\s+([a-zA-Z0-9_]+)\s*=\s*\(', html))
all_defined = funcs_defined | funcs_assigned | funcs_arrow

print(f"Total defined functions in JS: {len(all_defined)}")

# Find all onclick attributes
onclicks = re.findall(r'onclick=[\"\\\']([^\"\\\']+)[\"\\\']', html)
called_funcs = set()
for oc in onclicks:
    # extract func call like myFunc(...)
    matches = re.findall(r'([a-zA-Z0-9_]+)\s*\(', oc)
    for m in matches:
        called_funcs.add(m)

# Standard built-ins or DOM
built_ins = {'getElementById', 'stopPropagation', 'alert', 'confirm', 'prompt', 'preventDefault'}

missing = set()
for cf in called_funcs:
    if cf not in all_defined and cf not in built_ins:
        missing.add(cf)

print(f"\nCalled functions in onclicks: {len(called_funcs)}")
print("Missing functions:", missing)
