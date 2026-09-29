with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace AddProductRequest
idx_apr = code.find('class AddProductRequest')
idx_apr_end = code.find('\n\n@app.', idx_apr)

new_add_prod_class = '''class AddProductRequest(BaseModel):
    title: str
    brand: Optional[str] = "NVB Vision"
    category: Optional[str] = None
    category_id: Optional[int] = None
    subcategory: Optional[str] = "General"
    price: float
    mrp: Optional[float] = None
    discount: Optional[int] = None
    stock: Optional[int] = 25
    low_stock_threshold: Optional[int] = 10
    sku: Optional[str] = None
    images: Optional[List[str]] = None
    image_url: Optional[str] = None
    additional_images: Optional[List[str]] = None
    video_url: Optional[str] = ""
    tags: Optional[str] = ""
    specs: Optional[Dict[str, Any]] = None
    specifications: Optional[Dict[str, Any]] = None
    variants: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = ""
    short_description: Optional[str] = ""
    seller_name: Optional[str] = "NVB Direct Official"
    seller_id: Optional[str] = "seller-1"
    status: Optional[str] = "Published"
    is_featured: Optional[bool] = False
    is_flash_sale: Optional[bool] = False
    is_deal_of_day: Optional[bool] = False
    deal_of_the_day: Optional[bool] = False'''

code = code[:idx_apr] + new_add_prod_class + code[idx_apr_end:]
print("AddProductRequest replaced")

# Replace create_product function
idx_cp = code.find('@app.post("/api/admin/products")\ndef create_product')
idx_cp_end = code.find('\n\n@app.put("/api/admin/products/{product_id}/stock")', idx_cp)

new_create_prod = '''@app.post("/api/admin/products")
def create_product(prod: AddProductRequest):
    conn = get_db(); c = conn.cursor()
    # Resolve category
    category_name = prod.category or "Electronics"
    if prod.category_id and not prod.category:
        c.execute("SELECT name FROM categories WHERE id = ?", (prod.category_id,))
        row = c.fetchone()
        if row: category_name = row["name"]
    
    # Resolve images
    imgs = prod.images or []
    if not imgs and prod.additional_images:
        imgs = prod.additional_images
    if not imgs and prod.image_url:
        imgs = [prod.image_url]
    if not imgs:
        imgs = ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"]

    specs_obj = prod.specs or prod.specifications or {}
    vars_obj = prod.variants or []
    mrp_val = prod.mrp or (prod.price * 1.25)
    disc = prod.discount if prod.discount is not None else (int(round(((mrp_val - prod.price) / mrp_val) * 100)) if mrp_val > prod.price else 0)
    deal_val = 1 if (prod.is_deal_of_day or prod.deal_of_the_day) else 0

    clean_title = re.sub(r'[^a-zA-Z0-9]+', '-', prod.title.lower()).strip('-')[:25]
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
    ))
    conn.commit(); conn.close()
    return {"id": pid, "status": "CREATED", "message": f"Product \'{prod.title}\' added successfully."}'''

code = code[:idx_cp] + new_create_prod + code[idx_cp_end:]
print("create_product replaced")

# Also add @app.post("/api/products/{prod_id}/reviews") to add_review
old_review_head = '@app.post("/api/reviews")\ndef add_review(rev: ReviewRequest):'
new_review_head = '''@app.post("/api/reviews")
@app.post("/api/products/{prod_id}/reviews")
def add_review(rev: ReviewRequest, prod_id: Optional[str] = None):
    conn = get_db(); c = conn.cursor()
    rid = f"rev-{uuid.uuid4().hex[:8]}"
    p_id = rev.product_id or prod_id or ""
    author_name = rev.user_name or rev.author or "Verified Customer"
    c.execute(\'\'\'INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?)\'\'\',
              (rid, p_id, author_name, rev.rating, rev.title, rev.comment, datetime.now().strftime("%Y-%m-%d")))
    c.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?", (p_id,))
    row = c.fetchone()
    avg_r = row[0] or 5.0
    count_r = row[1] or 1
    c.execute("UPDATE products SET rating = ?, review_count = ? WHERE id = ?", (round(avg_r, 1), count_r, p_id))
    conn.commit(); conn.close()
    return {"id": rid, "status": "APPROVED", "message": "Review posted successfully!"}'''

idx_rev = code.find(old_review_head)
if idx_rev != -1:
    idx_rev_end = code.find('\n\n@app.post("/api/reviews/{review_id}/helpful")', idx_rev)
    code = code[:idx_rev] + new_review_head + code[idx_rev_end:]
    print("add_review updated")
else:
    print("Warning: old_review_head not found")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("patch_server2 complete!")
