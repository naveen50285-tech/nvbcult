with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids_to_check = [
    'hero-tee-count', 'hero-elec-count', 'total-count-badge', 
    'products-grid', 'nvb-company-story', 'backend-status-pill',
    'cart-drawer', 'cart-backdrop', 'cart-badge', 'cart-badge-mobile',
    'cart-items', 'cart-subtotal', 'cart-tax', 'cart-total',
    'details-modal', 'checkout-modal', 'login-modal', 'portal-view',
    'user-view', 'ai-chat-drawer', 'ai-chat-messages'
]

for el_id in ids_to_check:
    found = f'id="{el_id}"' in html or f"id='{el_id}'" in html
    print(f"Element id='{el_id}': {'FOUND' if found else '*** MISSING ***'}")
