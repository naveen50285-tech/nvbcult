with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_insert = '''    clean_title = re.sub(r'[^a-zA-Z0-9]+', '-', prod.title.lower()).strip('-')[:25]
    pid = f"nvb-{clean_title}-{uuid.uuid4().hex[:4]}"
    sku = prod.sku or f"NVB-{uuid.uuid4().hex[:6].upper()}"

    c.execute(\'\'\'
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 50, 0, ?, ?, ?, ?, ?, ?, ?, ?)
    \'\'\', (
        pid, prod.title, prod.brand, category_name, prod.subcategory, prod.price, mrp_val,
        disc, prod.stock, prod.low_stock_threshold, sku, json.dumps(imgs),
        prod.video_url or "", prod.tags or "", int(prod.is_featured or False), 0, 1, int(prod.is_flash_sale or False),
        deal_val, json.dumps(specs_obj), json.dumps(vars_obj),
        prod.description or prod.short_description or "", prod.short_description or "",
        prod.seller_name, prod.seller_id, prod.status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))'''

new_insert = '''    clean_title = re.sub(r'[^a-zA-Z0-9]+', '-', prod.title.lower()).strip('-')[:25]
    pid = f"nvb-{clean_title}-{uuid.uuid4().hex[:4]}"
    base_sku = prod.sku or f"NVB-{uuid.uuid4().hex[:6].upper()}"
    sku = base_sku

    # Check if SKU exists and make unique if needed
    c.execute("SELECT COUNT(*) FROM products WHERE sku = ?", (sku,))
    if c.fetchone()[0] > 0:
        sku = f"{base_sku}-{uuid.uuid4().hex[:4].upper()}"

    c.execute(\'\'\'
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 50, 0, ?, ?, ?, ?, ?, ?, ?, ?)
    \'\'\', (
        pid, prod.title, prod.brand, category_name, prod.subcategory, prod.price, mrp_val,
        disc, prod.stock, prod.low_stock_threshold, sku, json.dumps(imgs),
        prod.video_url or "", prod.tags or "", int(prod.is_featured or False), 0, 1, int(prod.is_flash_sale or False),
        deal_val, json.dumps(specs_obj), json.dumps(vars_obj),
        prod.description or prod.short_description or "", prod.short_description or "",
        prod.seller_name, prod.seller_id, prod.status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))'''

if old_insert in text:
    text = text.replace(old_insert, new_insert)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated create_product SKU uniqueness handling")
else:
    print("Warning: old_insert pattern not found")
