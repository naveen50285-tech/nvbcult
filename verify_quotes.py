import re

with open('static/index.html', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print('Script blocks found:', len(scripts))
js = scripts[0]

# Check for syntax errors by checking if any lines have unmatched quotes outside template literals
lines = js.splitlines()
in_template = False
errors = []
for i, line in enumerate(lines):
    s = line.strip()
    if s.count('`') % 2 != 0:
        in_template = not in_template
        continue
    if in_template:
        continue
    if s.startswith('//'):
        continue
    # check quotes
    q_double = s.count('"')
    if q_double % 2 != 0 and '\\"' not in s:
        errors.append((i+1, "unmatched double quote", s))
    q_single = s.count("'")
    if q_single % 2 != 0 and "\\'" not in s:
        errors.append((i+1, "unmatched single quote", s))

print(f"Total potential quote errors: {len(errors)}")
for e in errors[:5]:
    print("Line", e[0], e[1], ":", e[2][:60].encode('ascii', 'replace').decode('ascii'))
