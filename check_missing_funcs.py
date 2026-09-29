import re

with open('static/index.html', encoding='utf-8') as f:
    html = f.read()

# Find all inline JS calls in onclick, onchange, onsubmit, oninput
handlers = re.findall(r'on(?:click|change|submit|input)=["\']([^"\']+)["\']', html)
funcs_called = set()
for h in handlers:
    # extract function names
    calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', h)
    for c in calls:
        if c not in ('event', 'window', 'document', 'console', 'parseInt', 'parseFloat', 'Math', 'alert', 'confirm', 'prompt', 'Boolean', 'String'):
            funcs_called.add(c)

# Find all function definitions in <script>
script_tags = re.findall(r'<script.*?>([\s\S]*?)</script>', html)
script_body = '\n'.join(script_tags)

funcs_defined = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', script_body))
# also check var/let/const func =
funcs_defined.update(re.findall(r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', script_body))

print("Total inline handler function calls found:", len(funcs_called))
missing = funcs_called - funcs_defined
print("Missing functions:", missing)
for m in sorted(list(missing)):
    print(" -", m)
