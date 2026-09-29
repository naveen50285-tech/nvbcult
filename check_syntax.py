import re

def check_html_js():
    with open('static/index.html', encoding='utf-8') as f:
        content = f.read()

    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    print(f"Found {len(scripts)} script block(s)")
    for idx, s in enumerate(scripts):
        lines = s.splitlines()
        for i, line in enumerate(lines):
            # Check for unterminated string literals like alert("... without close quote
            if 'alert("' in line and not line.rstrip().endswith('");') and not line.rstrip().endswith('",'):
                print(f"Potentially unterminated alert on line {i+1}: {line}")

if __name__ == "__main__":
    check_html_js()
