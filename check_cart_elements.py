with open('build_nvb_store.py', 'r', encoding='utf-8') as f:
    text = f.read()

for el in ['cart-items-container', 'cart-total-payable', 'cart-drawer-overlay', 'det-modal-title', 'product-details-modal']:
    print(f"{el}: {el in text}")
