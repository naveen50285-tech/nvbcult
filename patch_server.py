import re

with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update parse_product
old_parse = '''def parse_product(r):
    return {
        "id": r["id"], "title": r["title"], "brand": r["brand"],
        "category": r["category"], "subcategory": r["subcategory"],
        "price": r["price"], "mrp": r["mrp"], "discount": r["discount"],
        "rating": r["rating"], "review_count": r["review_count"],
        "stock": r["stock"], "low_stock_threshold": r["low_stock_threshold"],
        "sku": r["sku"], "images": json.loads(r["images"]),
        "video_url": r["video_url"], "tags": r["tags"],
        "is_featured": bool(r["is_featured"]), "is_bestseller": bool(r["is_bestseller"]),
        "is_new": bool(r["is_new"]), "is_flash_sale": bool(r["is_flash_sale"]),
        "is_deal_of_day": bool(r["is_deal_of_day"]),
        "flash_stock_limit": r["flash_stock_limit"], "flash_sold": r["flash_sold"],
        "specs": json.loads(r["specs"]), "variants": json.loads(r["variants"]),
        "description": r["description"], "short_description": r["short_description"],
        "seller_name": r["seller_name"], "seller_id": r["seller_id"],
        "status": r["status"], "created_at": r["created_at"]
    }'''

new_parse = '''def parse_product(r):
    imgs = json.loads(r["images"]) if r["images"] else []
    specs_obj = json.loads(r["specs"]) if r["specs"] else {}
    vars_obj = json.loads(r["variants"]) if r["variants"] else []
    return {
        "id": r["id"], "title": r["title"], "brand": r["brand"],
        "category": r["category"], "category_name": r["category"], "subcategory": r["subcategory"],
        "price": r["price"], "mrp": r["mrp"], "discount": r["discount"], "discount_percent": r["discount"],
        "rating": r["rating"], "review_count": r["review_count"],
        "stock": r["stock"], "low_stock_threshold": r["low_stock_threshold"],
        "sku": r["sku"], "images": imgs,
        "image_url": imgs[0] if imgs else "",
        "video_url": r["video_url"], "tags": r["tags"],
        "is_featured": bool(r["is_featured"]), "is_bestseller": bool(r["is_bestseller"]),
        "is_new": bool(r["is_new"]), "is_flash_sale": bool(r["is_flash_sale"]),
        "is_deal_of_day": bool(r["is_deal_of_day"]), "deal_of_the_day": bool(r["is_deal_of_day"]),
        "flash_stock_limit": r["flash_stock_limit"], "flash_sold": r["flash_sold"],
        "specs": specs_obj, "specifications": specs_obj,
        "variants": vars_obj,
        "description": r["description"], "short_description": r["short_description"],
        "seller_name": r["seller_name"], "seller_id": r["seller_id"],
        "status": r["status"], "created_at": r["created_at"]
    }'''

if old_parse in code:
    code = code.replace(old_parse, new_parse)
    print("Updated parse_product successfully")
else:
    print("Warning: old_parse pattern not found exactly")

# 2. Update AI Assistant return dict
old_ai_return = 'return {"text": resp_text, "products": matched}'
new_ai_return = 'return {"text": resp_text, "response": resp_text, "products": matched, "recommended_products": matched}'
if old_ai_return in code:
    code = code.replace(old_ai_return, new_ai_return)
    print("Updated AI return successfully")

# 3. Update admin_stats return
old_admin_stats = '''    return {
        "revenue": (rev or 0.0) + 1284500.0, "orders_count": (total_orders or 0) + 314,
        "customers_count": 4270, "sellers_count": sellers, "total_products": total_products,
        "pending_orders": pending, "low_stock": low_stock, "out_of_stock": out_of_stock,
        "category_breakdown": cats,
        "sales_trend": [
            {"period": "Mon", "sales": 184000, "orders": 42},
            {"period": "Tue", "sales": 210000, "orders": 55},
            {"period": "Wed", "sales": 195000, "orders": 48},
            {"period": "Thu", "sales": 260000, "orders": 64},
            {"period": "Fri", "sales": 320000, "orders": 82},
            {"period": "Sat", "sales": 410000, "orders": 110},
            {"period": "Sun", "sales": 395000, "orders": 98}
        ]
    }'''

new_admin_stats = '''    total_rev = (rev or 0.0) + 1284500.0
    total_ord = (total_orders or 0) + 314
    trend = [
        {"period": "Mon", "sales": 184000, "orders": 42},
        {"period": "Tue", "sales": 210000, "orders": 55},
        {"period": "Wed", "sales": 195000, "orders": 48},
        {"period": "Thu", "sales": 260000, "orders": 64},
        {"period": "Fri", "sales": 320000, "orders": 82},
        {"period": "Sat", "sales": 410000, "orders": 110},
        {"period": "Sun", "sales": 395000, "orders": 98}
    ]
    return {
        "revenue": total_rev,
        "total_gmv": total_rev,
        "orders_count": total_ord,
        "total_orders": total_ord,
        "avg_order_value": round(total_rev / max(1, total_ord), 2),
        "customers_count": 4270,
        "sellers_count": sellers,
        "total_products": total_products,
        "pending_orders": pending,
        "low_stock": low_stock,
        "low_stock_count": low_stock,
        "out_of_stock": out_of_stock,
        "category_breakdown": cats,
        "category_distribution": [{"name": c["category"], "count": c["count"]} for c in cats],
        "sales_trend": trend,
        "revenue_chart": trend
    }'''

if old_admin_stats in code:
    code = code.replace(old_admin_stats, new_admin_stats)
    print("Updated admin_stats successfully")

# 4. Make ReviewRequest and Review endpoint flexible
old_review_class = '''class ReviewRequest(BaseModel):
    product_id: str
    user_name: str
    rating: int
    title: str
    comment: str'''

new_review_class = '''class ReviewRequest(BaseModel):
    product_id: Optional[str] = None
    user_name: Optional[str] = None
    author: Optional[str] = None
    rating: int
    title: Optional[str] = "Customer Review"
    comment: str
    verified_purchase: Optional[bool] = True'''

if old_review_class in code:
    code = code.replace(old_review_class, new_review_class)
    print("Updated ReviewRequest class successfully")

old_review_endpoint = '''@app.post("/api/reviews")
def add_review(rev: ReviewRequest):
    conn = get_db(); c = conn.cursor()
    rid = f"rev-{uuid.uuid4().hex[:8]}"
    c.execute(\'\'\'INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?)\'\'\',
              (rid, rev.product_id, rev.user_name, rev.rating, rev.title, rev.comment, datetime.now().strftime("%Y-%m-%d")))
    c.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?", (rev.product_id,))
    avg_r, count_r = c.fetchone()
    c.execute("UPDATE products SET rating = ?, review_count = ? WHERE id = ?", (round(avg_r, 1), count_r, rev.product_id))
    conn.commit(); conn.close()
    return {"id": rid, "status": "APPROVED", "message": "Review posted successfully!"}'''

new_review_endpoint = '''@app.post("/api/reviews")
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

if old_review_endpoint in code:
    code = code.replace(old_review_endpoint, new_review_endpoint)
    print("Updated review endpoint successfully")

# 5. Make AddProductRequest and create_product flexible
old_add_prod_class = '''class AddProductRequest(BaseModel):
    title: str
    brand: str
    category: str
    subcategory: str
    price: float
    mrp: float
    discount: Optional[int] = None
    stock: int
    low_stock_threshold: Optional[int] = 10
    sku: Optional[str] = None
    images: List[str]
    video_url: Optional[str] = ""
    tags: Optional[str] = ""
    specs: Dict[str, Any]
    variants: List[Dict[str, Any]]
    description: str
    short_description: str
    seller_name: Optional[str] = "NVB Direct Official"
    seller_id: Optional[str] = "seller-1"
    status: Optional[str] = "Published"
    is_featured: Optional[bool] = False
    is_flash_sale: Optional[bool] = False
    is_deal_of_day: Optional[bool] = False'''

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

if old_add_prod_class in code:
    code = code.replace(old_add_prod_class, new_add_prod_class)
    print("Updated AddProductRequest class successfully")

old_create_prod = '''@app.post("/api/admin/products")
def create_product(prod: AddProductRequest):
    conn = get_db(); c = conn.cursor()
    clean_title = prod.title.lower().replace(' ', '-')[:25]
    pid = f"nvb-{clean_title}-{uuid.uuid4().hex[:4]}"
    sku = prod.sku or f"SKU-{uuid.uuid4().hex[:8].upper()}"
    disc = prod.discount if prod.discount is not None else (int(round(((prod.mrp - prod.price) / prod.mrp) * 100)) if prod.mrp > prod.price else 0)
    c.execute(\'\'\'
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 50, 0, ?, ?, ?, ?, ?, ?, ?, ?)
    \'\'\', (
        pid, prod.title, prod.brand, prod.category, prod.subcategory, prod.price, prod.mrp,
        disc, prod.stock, prod.low_stock_threshold, sku, json.dumps(prod.images),
        prod.video_url, prod.tags, int(prod.is_featured), 0, 1, int(prod.is_flash_sale),
        int(prod.is_deal_of_day), json.dumps(prod.specs), json.dumps(prod.variants),
        prod.description, prod.short_description, prod.seller_name, prod.seller_id,
        prod.status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit(); conn.close()
    return {"id": pid, "status": "CREATED", "message": f"Product \'{prod.title}\' added successfully."}'''

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

if old_create_prod in code:
    code = code.replace(old_create_prod, new_create_prod)
    print("Updated create_product successfully")

# 6. Make bulk upload support both routes and accept dict or list
old_bulk = '''@app.post("/api/admin/bulk-upload")
def bulk_upload(products: List[Dict[str, Any]]):'''

new_bulk = '''@app.post("/api/admin/bulk-upload")
@app.post("/api/admin/bulk-import")
def bulk_upload(payload: Any = Body(...)):
    products = payload.get("products", []) if isinstance(payload, dict) else payload
    if not isinstance(products, list):
        raise HTTPException(status_code=400, detail="Invalid products payload format")'''

if old_bulk in code:
    code = code.replace(old_bulk, new_bulk)
    print("Updated bulk_upload endpoint successfully")

# 7. Add flexible order status routes
old_order_status = '''@app.put("/api/admin/orders/{order_id}/status")
def update_order_status(order_id: str, status: str):'''

new_order_status = '''@app.put("/api/admin/orders/{order_id}/status")
@app.patch("/api/admin/orders/{order_id}/status")
@app.put("/api/orders/{order_id}/status")
@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status: str):'''

if old_order_status in code:
    code = code.replace(old_order_status, new_order_status)
    print("Updated order status endpoints successfully")

# Write updated server.py
with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("server.py patch completed!")
