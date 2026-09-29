with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script>')
end = html.find('</script>', start)
js = html[start+8:end]
print(f"Total JS length: {len(js)} chars, {len(js.splitlines())} lines")

with open('static_script.js', 'w', encoding='utf-8') as f:
    f.write(js)
