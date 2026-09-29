with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure build_ui.py has the same content or rebuild script
with open('build_ui.py', 'w', encoding='utf-8') as f:
    f.write('parts = [' + repr(html) + ']\n\nwith open("static/index.html", "w", encoding="utf-8") as out:\n    out.write("".join(parts))\nprint("Rebuilt static/index.html cleanly")\n')

print("build_ui.py updated to maintain exact synchronized state.")
