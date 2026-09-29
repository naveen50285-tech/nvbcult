with open('build_nvb_store.py', 'r', encoding='utf-8') as f:
    code = f.read()

ids_to_check = [
    'cart-drawer', 'cart-backdrop', 'cart-badge', 'cart-badge-mobile',
    'cart-items', 'cart-subtotal', 'cart-tax', 'cart-total',
    'details-modal', 'checkout-modal', 'login-modal', 'portal-view',
    'user-view', 'ai-chat-drawer', 'ai-chat-messages'
]

print("=== Checking build_nvb_store.py ===")
for el_id in ids_to_check:
    count = code.count(f'id="{el_id}"') + code.count(f"id='{el_id}'")
    print(f"ID '{el_id}': occurrences = {count}")
