import os

for fname in os.listdir('.'):
    if fname.endswith('.py') or fname.endswith('.html') or fname.endswith('.bak'):
        try:
            with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
                if 'cart-drawer' in c or 'details-modal' in c or 'ai-chat-drawer' in c:
                    print(f"{fname}: has cart-drawer={'cart-drawer' in c}, details-modal={'details-modal' in c}, ai-chat={'ai-chat-drawer' in c}, len={len(c)}")
        except Exception as e:
            pass
