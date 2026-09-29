import os
import re

def fix():
    build_file = r"C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\build_nvb_store.py"
    with open(build_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace alert with backtick template string
    old_target = """            } else {
                alert("✦ TO INSTALL NVB CULT AS AN APP:\\n\\n1. Look for the 'Install App' icon (⊕) on the right side of your browser address bar.\\n2. Click 'Install' to add NVB Cult to your Windows Start Menu, Taskbar & Desktop!\\n\\nOr use the desktop shortcut created on your desktop: 'NVB Cult App'");
            }"""

    new_target = """            } else {
                alert(`✦ TO INSTALL NVB CULT AS AN APP:

1. Click the Install App icon on the right side of your browser address bar.
2. Click 'Install' to add NVB Cult to your Windows Start Menu, Taskbar & Desktop!

Or use the desktop shortcut created on your desktop: 'NVB Cult App'`);
            }"""

    if old_target in content:
        content = content.replace(old_target, new_target)
        print("[OK] Replaced old alert in build_nvb_store.py with backtick template string")
    else:
        # Regex replacement if whitespace slightly differs
        content = re.sub(
            r'alert\("✦ TO INSTALL NVB CULT AS AN APP:.*?\'NVB Cult App\'"\);',
            r'''alert(`✦ TO INSTALL NVB CULT AS AN APP:\n\n1. Click the Install App icon in the browser address bar.\n2. Click 'Install' to add NVB Cult to your Windows Start Menu & Desktop!\n\nOr use the desktop shortcut on your Desktop: 'NVB Cult App'`);''',
            content,
            flags=re.DOTALL
        )
        print("[OK] Applied regex replacement for alert")

    with open(build_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    fix()
