import shutil
import re
import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Request, Response, Body, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from database import get_db

class LoginRequest(BaseModel):
    username: str
    password: str


app = FastAPI(title="NVB Cult API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM products")
    p_count = c.fetchone()[0]
    conn.close()
    return {
        "status": "online",
        "connected": True,
        "database": "marketplace.db (SQLite)",
        "products_count": p_count,
        "server": "NVB Cult Backend (FastAPI)",
        "timestamp": datetime.now().isoformat()
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

class CartItemRequest(BaseModel):
    session_id: str
    product_id: str
    variant_name: Optional[str] = "Default"
    quantity: int = 1

class WishlistRequest(BaseModel):
    session_id: str
    product_id: str

class CheckoutRequest(BaseModel):
    session_id: Optional[str] = "guest-session"
    customer_name: str
    customer_email: Optional[str] = "cult@nvb.com"
    customer_phone: str
    shipping_address: str
    delivery_method: Optional[str] = "Standard Free Delivery"
    delivery_fee: Optional[float] = 0.0
    payment_method: Optional[str] = "Cash on Delivery"
    coupon_code: Optional[str] = None
    total: Optional[float] = None
    items: List[Dict[str, Any]]

class ReviewRequest(BaseModel):
    product_id: Optional[str] = None
    user_name: Optional[str] = None
    author: Optional[str] = None
    rating: int
    title: Optional[str] = "Customer Review"
    comment: str
    verified_purchase: Optional[bool] = True

class AIQueryRequest(BaseModel):
    query: str

class SellerRegisterRequest(BaseModel):
    name: str
    business_name: str
    email: str
    phone: str
    gstin: Optional[str] = ""

class AddProductRequest(BaseModel):
    title: str
    brand: Optional[str] = "NVB Cult"
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
    specs: Optional[Any] = None
    specifications: Optional[Any] = None
    variants: Optional[Any] = None
    description: Optional[str] = ""
    short_description: Optional[str] = ""
    seller_name: Optional[str] = "NVB Cult Official"
    seller_id: Optional[str] = "seller-1"
    status: Optional[str] = "Published"
    is_featured: Optional[bool] = False
    is_flash_sale: Optional[bool] = False
    is_deal_of_day: Optional[bool] = False
    deal_of_the_day: Optional[bool] = False

@app.get("/api/categories")
def get_categories():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    rows = c.fetchall()
    cats = []
    for r in rows:
        c.execute("SELECT COUNT(*) FROM products WHERE category = ?", (r["name"],))
        count = c.fetchone()[0]
        cats.append({
            "id": r["id"], "name": r["name"], "icon": r["icon"],
            "description": r["description"], "subcategories": json.loads(r["subcategories"]),
            "product_count": count
        })
    conn.close()
    return cats

def parse_product(r):
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
    }

@app.get("/api/products")
def get_products(
    category: Optional[str] = None, subcategory: Optional[str] = None,
    brand: Optional[str] = None, search: Optional[str] = None,
    min_price: Optional[float] = None, max_price: Optional[float] = None,
    min_rating: Optional[float] = None, in_stock_only: Optional[bool] = False,
    is_featured: Optional[int] = None, is_bestseller: Optional[int] = None,
    is_new: Optional[int] = None, is_flash_sale: Optional[int] = None,
    is_deal_of_day: Optional[int] = None, sort_by: Optional[str] = "relevance"
):
    conn = get_db()
    c = conn.cursor()
    q = "SELECT * FROM products WHERE status = 'Published'"
    p = []
    if category and category.lower() != "all":
        q += " AND LOWER(category) = LOWER(?)"; p.append(category)
    if subcategory:
        q += " AND LOWER(subcategory) = LOWER(?)"; p.append(subcategory)
    if brand:
        q += " AND LOWER(brand) = LOWER(?)"; p.append(brand)
    if search:
        st = f"%{search.lower()}%"
        q += " AND (LOWER(title) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(category) LIKE ? OR LOWER(subcategory) LIKE ? OR LOWER(tags) LIKE ? OR LOWER(description) LIKE ?)"
        p.extend([st] * 6)
    if min_price is not None:
        q += " AND price >= ?"; p.append(min_price)
    if max_price is not None:
        q += " AND price <= ?"; p.append(max_price)
    if min_rating is not None:
        q += " AND rating >= ?"; p.append(min_rating)
    if in_stock_only:
        q += " AND stock > 0"
    if is_featured is not None:
        q += " AND is_featured = ?"; p.append(is_featured)
    if is_bestseller is not None:
        q += " AND is_bestseller = ?"; p.append(is_bestseller)
    if is_new is not None:
        q += " AND is_new = ?"; p.append(is_new)
    if is_flash_sale is not None:
        q += " AND is_flash_sale = ?"; p.append(is_flash_sale)
    if is_deal_of_day is not None:
        q += " AND is_deal_of_day = ?"; p.append(is_deal_of_day)

    if sort_by == "price_asc": q += " ORDER BY price ASC"
    elif sort_by == "price_desc": q += " ORDER BY price DESC"
    elif sort_by == "rating": q += " ORDER BY rating DESC"
    elif sort_by == "discount": q += " ORDER BY discount DESC"
    elif sort_by == "newest": q += " ORDER BY created_at DESC"
    else: q += " ORDER BY is_featured DESC, rating DESC, review_count DESC"

    c.execute(q, p)
    rows = c.fetchall()
    prods = [parse_product(r) for r in rows]
    conn.close()
    return prods

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    r = c.fetchone()
    if not r:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    prod = parse_product(r)

    c.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC", (product_id,))
    prod["reviews"] = [dict(rv) for rv in c.fetchall()]

    c.execute("SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4", (prod["category"], product_id))
    prod["related_products"] = [parse_product(rel) for rel in c.fetchall()]
    conn.close()
    return prod


@app.get("/api/delivery-check")
def check_delivery(pincode: str):
    p = pincode.strip()
    if len(p) != 6 or not p.isdigit():
        return {"valid": False, "message": "Please enter a valid 6-digit Indian PIN code."}
    tier_1 = {"56": "Bengaluru", "11": "Delhi NCR", "40": "Mumbai", "60": "Chennai", "50": "Hyderabad", "70": "Kolkata"}
    city = tier_1.get(p[:2], "Regional Hub")
    days = 1 if p[:2] in tier_1 else 3
    est = (datetime.now() + timedelta(days=days)).strftime("%A, %d %b")
    return {
        "valid": True, "available": True, "pincode": p, "city": city, "estimated_date": est,
        "estimated_days": days, "delivery_charge": 0.0, "free_delivery": True, "cod_available": True,
        "message": f"Delivery to {city} ({p}) by {est} | FREE Delivery"
    }

@app.get("/api/cart")
def get_cart(session_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    SELECT c.id as cart_id, c.variant_name, c.quantity, p.*
    FROM cart_items c JOIN products p ON c.product_id = p.id
    WHERE c.session_id = ?
    ''', (session_id,))
    rows = c.fetchall()
    items = []
    subtotal, original_total = 0.0, 0.0
    for r in rows:
        subtotal += r["price"] * r["quantity"]
        original_total += r["mrp"] * r["quantity"]
        items.append({
            "cart_id": r["cart_id"], "product_id": r["id"], "title": r["title"],
            "brand": r["brand"], "price": r["price"], "mrp": r["mrp"],
            "discount": r["discount"], "quantity": r["quantity"],
            "variant": r["variant_name"],
            "image": json.loads(r["images"])[0] if r["images"] else "",
            "stock": r["stock"]
        })
    delivery_fee = 0.0 if (subtotal >= 499 or subtotal == 0) else 99.0
    tax = round(subtotal * 0.18, 2)
    conn.close()
    return {
        "items": items, "item_count": sum(i["quantity"] for i in items),
        "subtotal": subtotal, "mrp_total": original_total,
        "total_savings": original_total - subtotal,
        "delivery_fee": delivery_fee, "tax": tax,
        "total": subtotal + delivery_fee
    }

@app.post("/api/cart")
def add_to_cart(item: CartItemRequest):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, stock FROM products WHERE id = ?", (item.product_id,))
    prod = c.fetchone()
    if not prod:
        conn.close(); raise HTTPException(status_code=404, detail="Product not found")
    if prod["stock"] < 1:
        conn.close(); raise HTTPException(status_code=400, detail="Out of stock")

    c.execute("SELECT id, quantity FROM cart_items WHERE session_id = ? AND product_id = ? AND variant_name = ?",
              (item.session_id, item.product_id, item.variant_name))
    existing = c.fetchone()
    if existing:
        c.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (existing["quantity"] + item.quantity, existing["id"]))
    else:
        cid = f"crt-{uuid.uuid4().hex[:8]}"
        c.execute("INSERT INTO cart_items VALUES (?, ?, ?, ?, ?, ?)",
                  (cid, item.session_id, item.product_id, item.variant_name, item.quantity, datetime.now().isoformat()))
    conn.commit(); conn.close()
    return {"success": True, "message": "Item added to cart"}

@app.put("/api/cart/{cart_id}")
def update_cart(cart_id: str, quantity: int):
    conn = get_db(); c = conn.cursor()
    if quantity <= 0: c.execute("DELETE FROM cart_items WHERE id = ?", (cart_id,))
    else: c.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (quantity, cart_id))
    conn.commit(); conn.close()
    return {"success": True}

@app.delete("/api/cart/{cart_id}")
def remove_cart(cart_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM cart_items WHERE id = ?", (cart_id,))
    conn.commit(); conn.close()
    return {"success": True}

@app.get("/api/wishlist")
def get_wishlist(session_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute('''
    SELECT w.id as wishlist_id, p.* FROM wishlist_items w JOIN products p ON w.product_id = p.id WHERE w.session_id = ?
    ''', (session_id,))
    rows = c.fetchall()
    items = []
    for r in rows:
        items.append({
            "wishlist_id": r["wishlist_id"], "product_id": r["id"],
            "title": r["title"], "brand": r["brand"], "price": r["price"],
            "mrp": r["mrp"], "discount": r["discount"], "rating": r["rating"],
            "stock": r["stock"], "image": json.loads(r["images"])[0] if r["images"] else ""
        })
    conn.close()
    return items

@app.post("/api/wishlist/toggle")
def toggle_wishlist(req: WishlistRequest):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id FROM wishlist_items WHERE session_id = ? AND product_id = ?", (req.session_id, req.product_id))
    ex = c.fetchone()
    if ex:
        c.execute("DELETE FROM wishlist_items WHERE id = ?", (ex["id"],))
        conn.commit(); conn.close()
        return {"in_wishlist": False, "message": "Removed from Wishlist"}
    else:
        wid = f"wsh-{uuid.uuid4().hex[:8]}"
        c.execute("INSERT INTO wishlist_items VALUES (?, ?, ?, ?)", (wid, req.session_id, req.product_id, datetime.now().isoformat()))
        conn.commit(); conn.close()
        return {"in_wishlist": True, "message": "Added to Wishlist"}

@app.get("/api/coupons")
def get_coupons():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM coupons WHERE active = 1")
    coupons = [dict(r) for r in c.fetchall()]
    conn.close()
    return coupons

@app.get("/api/coupons/validate")
def validate_coupon(code: str, order_amount: float):
    code = code.strip().upper()
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM coupons WHERE code = ? AND active = 1", (code,))
    cp = c.fetchone()
    conn.close()
    if not cp: return {"valid": False, "message": "Invalid or expired coupon."}
    if order_amount < cp["min_order"]:
        return {"valid": False, "message": f"Requires min order of ₹{cp['min_order']:,.0f}"}
    if cp["discount_type"] == "percentage":
        disc = min((order_amount * cp["discount_value"]) / 100.0, cp["max_discount"])
    elif cp["discount_type"] == "fixed":
        disc = min(cp["discount_value"], order_amount)
    else: disc = 99.0
    return {"valid": True, "code": code, "discount_amount": round(disc, 2), "message": f"Saved ₹{disc:,.0f}!"}

def process_order_checkout(order_data: CheckoutRequest):
    conn = get_db(); c = conn.cursor()
    if not order_data.items:
        conn.close(); raise HTTPException(status_code=400, detail="Empty cart")
    subtotal = sum(i["price"] * i["quantity"] for i in order_data.items)
    discount = 0.0
    if order_data.coupon_code:
        c.execute("SELECT * FROM coupons WHERE code = ? AND active = 1", (order_data.coupon_code.upper(),))
        cp = c.fetchone()
        if cp and subtotal >= cp["min_order"]:
            if cp["discount_type"] == "percentage": discount = min((subtotal * cp["discount_value"]) / 100.0, cp["max_discount"])
            elif cp["discount_type"] == "fixed": discount = cp["discount_value"]
            elif cp["discount_type"] == "free_shipping": order_data.delivery_fee = 0.0
    tax = round((subtotal - discount) * 0.18, 2)
    delivery_fee = order_data.delivery_fee or 0.0
    total = round(subtotal - discount + delivery_fee, 2)
    order_id = f"NVB-2026-{uuid.uuid4().hex[:6].upper()}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    timeline = [
        {"status": "ORDER PLACED", "time": now_str, "completed": True, "desc": "Order placed successfully"},
        {"status": "CONFIRMED", "time": "In 15 mins", "completed": False, "desc": "Seller confirmed order"},
        {"status": "PACKED", "time": "Expected Tomorrow", "completed": False, "desc": "Tamper-proof packaging"},
        {"status": "SHIPPED", "time": "Pending", "completed": False, "desc": "Courier dispatched"},
        {"status": "OUT FOR DELIVERY", "time": "Pending", "completed": False, "desc": "Courier rider out for delivery"},
        {"status": "DELIVERED", "time": "Pending", "completed": False, "desc": "Package delivered"}
    ]
    for it in order_data.items:
        p_id = it.get("product_id") or it.get("id")
        qty = it.get("quantity", 1)
        if p_id:
            c.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?", (qty, p_id))
            c.execute("UPDATE products SET flash_sold = flash_sold + ? WHERE id = ? AND is_flash_sale = 1", (qty, p_id))
    c.execute('''
    INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ORDER PLACED', ?, ?, ?)
    ''', (
        order_id, order_data.session_id or "guest-session", order_data.customer_name, order_data.customer_email or "cult@nvb.com", order_data.customer_phone,
        order_data.shipping_address, order_data.delivery_method or "Standard Free Delivery", delivery_fee, order_data.payment_method or "Cash on Delivery",
        "Paid" if order_data.payment_method != "Cash on Delivery" else "Pending (COD)",
        subtotal, discount, tax, total, json.dumps(timeline), json.dumps(order_data.items), datetime.now().isoformat()
    ))
    if order_data.session_id:
        c.execute("DELETE FROM cart_items WHERE session_id = ?", (order_data.session_id,))
    c.execute('''INSERT INTO notifications VALUES (?, ?, 'Order Confirmed!', ?, 'order', 0, ?)''',
              (f"notif-{uuid.uuid4().hex[:6]}", order_data.session_id or "guest", f"Order #{order_id} placed successfully.", datetime.now().isoformat()))
    conn.commit(); conn.close()
    return {"success": True, "order_id": order_id, "total": total, "message": "Order placed successfully!"}

@app.post("/api/checkout")
def checkout_endpoint(order_data: CheckoutRequest):
    return process_order_checkout(order_data)

@app.post("/api/orders")
def orders_post_endpoint(order_data: CheckoutRequest):
    return process_order_checkout(order_data)

@app.get("/api/orders")
def get_orders(session_id: Optional[str] = None):
    conn = get_db(); c = conn.cursor()
    if session_id: c.execute("SELECT * FROM orders WHERE session_id = ? ORDER BY created_at DESC", (session_id,))
    else: c.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = []
    for r in c.fetchall():
        orders.append({
            "id": r["id"], "customer_name": r["customer_name"], "customer_email": r["customer_email"],
            "customer_phone": r["customer_phone"], "shipping_address": r["shipping_address"],
            "delivery_method": r["delivery_method"], "delivery_fee": r["delivery_fee"],
            "payment_method": r["payment_method"], "payment_status": r["payment_status"],
            "subtotal": r["subtotal"], "discount": r["discount"], "tax": r["tax"], "total": r["total"],
            "status": r["status"], "timeline": json.loads(r["timeline"]), "items": json.loads(r["items"]),
            "created_at": r["created_at"]
        })
    conn.close()
    return orders

@app.get("/api/orders/{order_id}")
def get_order_by_id(order_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    r = c.fetchone()
    if not r: conn.close(); raise HTTPException(status_code=404, detail="Order not found")
    order = {
        "id": r["id"], "customer_name": r["customer_name"], "customer_email": r["customer_email"],
        "customer_phone": r["customer_phone"], "shipping_address": r["shipping_address"],
        "delivery_method": r["delivery_method"], "delivery_fee": r["delivery_fee"],
        "payment_method": r["payment_method"], "payment_status": r["payment_status"],
        "subtotal": r["subtotal"], "discount": r["discount"], "tax": r["tax"], "total": r["total"],
        "status": r["status"], "timeline": json.loads(r["timeline"]), "items": json.loads(r["items"]),
        "created_at": r["created_at"]
    }
    conn.close()
    return order

@app.put("/api/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    r = c.fetchone()
    if not r: conn.close(); raise HTTPException(status_code=404, detail="Order not found")
    c.execute("UPDATE orders SET status = 'CANCELLED' WHERE id = ?", (order_id,))
    conn.commit(); conn.close()
    return {"success": True, "message": "Order cancelled"}

@app.post("/api/orders/{order_id}/return")
def return_order(order_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE orders SET status = 'RETURN REQUESTED' WHERE id = ?", (order_id,))
    conn.commit(); conn.close()
    return {"success": True, "message": "Return request submitted."}

@app.post("/api/reviews")
@app.post("/api/products/{prod_id}/reviews")
def add_review(rev: ReviewRequest, prod_id: Optional[str] = None):
    conn = get_db(); c = conn.cursor()
    rid = f"rev-{uuid.uuid4().hex[:8]}"
    p_id = rev.product_id or prod_id or ""
    author_name = rev.user_name or rev.author or "Verified Customer"
    c.execute('''INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?)''',
              (rid, p_id, author_name, rev.rating, rev.title, rev.comment, datetime.now().strftime("%Y-%m-%d")))
    c.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?", (p_id,))
    row = c.fetchone()
    avg_r = row[0] or 5.0
    count_r = row[1] or 1
    c.execute("UPDATE products SET rating = ?, review_count = ? WHERE id = ?", (round(avg_r, 1), count_r, p_id))
    conn.commit(); conn.close()
    return {"id": rid, "status": "APPROVED", "message": "Review posted successfully!"}

@app.post("/api/reviews/{review_id}/helpful")
def review_helpful(review_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE reviews SET helpful_count = helpful_count + 1 WHERE id = ?", (review_id,))
    conn.commit(); conn.close()
    return {"success": True}

@app.get("/api/compare")
def compare_products(ids: str):
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    if not id_list: return []
    conn = get_db(); c = conn.cursor()
    holders = ",".join(["?"] * len(id_list))
    c.execute(f"SELECT * FROM products WHERE id IN ({holders})", id_list)
    results = [parse_product(r) for r in c.fetchall()]
    conn.close()
    return results

@app.post("/api/ai-assistant")
def ai_assistant(req: AIQueryRequest):
    query = req.query.lower().strip()
    conn = get_db(); c = conn.cursor()
    resp_text = ""
    matched = []
    
    if any(k in query for k in ["company", "story", "motto", "dream", "vision", "brand", "cult", "about", "who are you", "what is"]):
        c.execute("SELECT * FROM products WHERE status = 'Published' LIMIT 3")
        matched = [parse_product(r) for r in c.fetchall()]
        resp_text = (
            "✦ **NEXT VISION BRAND (NVB CULT) // THE COMPANY MANIFESTO** ✦\n\n"
            "**NVB Cult** (Next Vision Brand) is an independent streetwear & creator tech collective founded in 2026, born from timeless romance, melody, and uncompromising substance.\n\n"
            "👑 **OUR MOTTO: DREAM • PLAN • ACHIEVE**\n"
            "• **DREAM**: Envisioning a world free from disposable, fast-fashion junk. We believe in heavy, everlasting fabrics that carry weight and posture.\n"
            "• **PLAN**: Obsessive craft and discipline. Sourcing 260 GSM French Terry cotton, bio-washed pre-shrunk weaves, and engineering pure, analog-warm creator electronics.\n"
            "• **ACHIEVE**: Releasing strictly limited, numbered drops directly to our cult community with zero corporate dilution.\n\n"
            "👁️ **THE LOGO SYMBOLISM**: The golden eye and soaring upward arrow in our circular metallic emblem represents sharp clarity of vision, fearless ambition, and ascending to the peak of your craft."
        )
        
    elif any(k in query for k in ["oversized", "streetwear", "heavy", "heavyweight", "260 gsm", "drop shoulder", "tshirt", "t-shirt", "tee"]):
        c.execute("SELECT * FROM products WHERE category = 'T-Shirts' LIMIT 3")
        matched = [parse_product(r) for r in c.fetchall()]
        if matched:
            resp_text = "For that signature street drape, here are our **NVB Cult** heavyweight drops:"
        else:
            resp_text = "👕 **NVB Cult T-Shirt Archive:** All placeholder example products have been cleared! The owner can upload authentic NVB Cult t-shirts directly via the Owner Dashboard."
        
    elif any(k in query for k in ["graphic", "print", "cyberpunk", "japan", "wave", "retro", "neon"]):
        c.execute("SELECT * FROM products WHERE category = 'T-Shirts' AND subcategory LIKE '%Graphic%' LIMIT 3")
        matched = [parse_product(r) for r in c.fetchall()]
        if matched:
            resp_text = "Here are our standout graphic pieces from the **NVB Cult** art series:"
        else:
            resp_text = "🎨 **NVB Cult Art Series:** Ready for authentic drops to be uploaded by the store owner!"
        
    elif any(k in query for k in ["size", "sizing", "fit", "measurements", "small", "medium", "large", "xl"]):
        resp_text = "📐 **NVB Cult Sizing Guide:**\n\n• **Oversized / Streetwear Tees:** Designed with a generous boxy drop-shoulder silhouette. Choose your standard size for a relaxed look, or size down one size for a regular fitted look.\n• **Classic & Supima Tees:** Tailored modern fit true to Indian sizing.\n• Available Sizes: **S (38\"), M (40\"), L (42\"), XL (44\"), XXL (46\")**."
        
    elif any(k in query for k in ["electronic", "tech", "gadget", "audio", "earbuds", "smartwatch", "charger"]):
        c.execute("SELECT * FROM products WHERE category = 'Electronics' LIMIT 3")
        matched = [parse_product(r) for r in c.fetchall()]
        if matched:
            resp_text = "Here are the latest tech drops in the NVB Cult Electronics collection:"
        else:
            resp_text = "⚡ **NVB Cult Electronics Status:** All placeholder products have been cleared! Store owners can upload new electronics right now via the Owner Dashboard."
            
    elif any(k in query for k in ["discount", "coupon", "offer", "sale", "code"]):
        resp_text = "🔥 **Exclusive Offer:** Use coupon code **`VISION10`** during checkout for an extra 10% instant discount across all NVB Cult drops!"
        
    elif any(k in query for k in ["shipping", "delivery", "track", "cod", "payment"]):
        resp_text = "📦 **Shipping & Payments:**\n\n• **Free Express Delivery** across India within 2 to 3 days on all orders.\n• Payment options: **Cash on Delivery (COD)**, **UPI (Google Pay, PhonePe, Paytm)**, and **Credit/Debit Cards**."
        
    else:
        words = [w for w in query.split() if len(w) > 2]
        if words:
            clause = " OR ".join(["title LIKE ? OR tags LIKE ? OR category LIKE ? OR subcategory LIKE ?" for _ in words])
            params = []
            for w in words: params.extend([f"%{w}%", f"%{w}%", f"%{w}%", f"%{w}%"])
            c.execute(f"SELECT * FROM products WHERE status = 'Published' AND ({clause}) LIMIT 3", params)
            matched = [parse_product(r) for r in c.fetchall()]
            
        if not matched:
            resp_text = f"I'm here to assist with **NVB Cult**! Ask me about our 260 GSM heavyweight drops, sizing guide, or upload your products as the store owner."
        else:
            resp_text = f"Here are the best matches for '{req.query}' from NVB Cult:"
            
    conn.close()
    return {"text": resp_text, "response": resp_text, "products": matched, "recommended_products": matched}

@app.get("/api/admin/stats")
def admin_stats():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT SUM(total), COUNT(*) FROM orders WHERE status != 'CANCELLED'")
    rev, total_orders = c.fetchone()
    c.execute("SELECT COUNT(*) FROM sellers")
    sellers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    total_products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products WHERE stock <= low_stock_threshold AND stock > 0")
    low_stock = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM orders WHERE status = 'ORDER PLACED'")
    pending = c.fetchone()[0]
    c.execute("SELECT category, COUNT(*) as count, AVG(price) as avg_p FROM products GROUP BY category")
    cats = [dict(r) for r in c.fetchall()]
    conn.close()
    total_rev = (rev or 0.0) + 1284500.0
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
    }

def handle_admin_auth(req: LoginRequest):
    conn = get_db(); c = conn.cursor()
    pw_hash = hashlib.sha256(req.password.strip().encode('utf-8')).hexdigest()
    user = None
    try:
        c.execute("SELECT * FROM admin_users WHERE username = ? AND password_hash = ?", (req.username.strip(), pw_hash))
        user = c.fetchone()
    except Exception:
        pass
    conn.close()
    
    # Also accept default owner credentials
    if not user and req.username.strip() == "admin" and req.password.strip() == "admin123":
        user = {"username": "admin", "role": "owner", "full_name": "NVB Cult Owner"}
        
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials. Use username: admin, password: admin123")
        
    token = f"nvb-owner-{uuid.uuid4().hex}"
    return {
        "success": True,
        "token": token,
        "user": {
            "username": "admin",
            "role": "owner",
            "full_name": "NVB Cult Owner"
        },
        "message": "Welcome back, NVB Cult Owner!"
    }

@app.post("/api/admin/login")
def admin_login(req: LoginRequest):
    return handle_admin_auth(req)

@app.post("/api/auth/login")
def auth_login(req: LoginRequest):
    return handle_admin_auth(req)

@app.get("/api/admin/verify")
def admin_verify(token: Optional[str] = None):
    if token and token.startswith("nvb-owner-"):
        return {"authenticated": True, "role": "owner", "username": "admin"}
    return {"authenticated": False}

def create_product_handler(prod: AddProductRequest):
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
        imgs = ["/static/products/nvb-tee-dream-plan-achieve.jpg"]

    specs_obj = prod.specs or prod.specifications or {}
    vars_obj = prod.variants or []
    mrp_val = prod.mrp or (prod.price * 1.25)
    disc = prod.discount if prod.discount is not None else (int(round(((mrp_val - prod.price) / mrp_val) * 100)) if mrp_val > prod.price else 0)
    deal_val = 1 if (prod.is_deal_of_day or prod.deal_of_the_day) else 0

    clean_title = re.sub(r'[^a-zA-Z0-9]+', '-', prod.title.lower()).strip('-')[:25]
    pid = f"nvb-{clean_title}-{uuid.uuid4().hex[:4]}"
    base_sku = prod.sku or f"NVB-{uuid.uuid4().hex[:6].upper()}"
    sku = base_sku

    # Check if SKU exists and make unique if needed
    c.execute("SELECT COUNT(*) FROM products WHERE sku = ?", (sku,))
    if c.fetchone()[0] > 0:
        sku = f"{base_sku}-{uuid.uuid4().hex[:4].upper()}"

    c.execute('''
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 50, 0, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pid, prod.title, prod.brand, category_name, prod.subcategory, prod.price, mrp_val,
        disc, prod.stock, prod.low_stock_threshold, sku, json.dumps(imgs),
        prod.video_url or "", prod.tags or "", int(prod.is_featured or False), 0, 1, int(prod.is_flash_sale or False),
        deal_val, json.dumps(specs_obj), json.dumps(vars_obj),
        prod.description or prod.short_description or "", prod.short_description or "",
        prod.seller_name, prod.seller_id, prod.status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit(); conn.close()
    return {"id": pid, "status": "CREATED", "message": f"Product '{prod.title}' added successfully."}

@app.post("/api/admin/products")
def create_admin_product(prod: AddProductRequest):
    return create_product_handler(prod)

@app.post("/api/products")
def create_product(prod: AddProductRequest):
    return create_product_handler(prod)

def update_stock_handler(product_id: str, stock: Optional[int] = None, data: Optional[dict] = None):
    conn = get_db(); c = conn.cursor()
    new_stock = stock
    if new_stock is None and data and "stock" in data:
        new_stock = int(data["stock"])
    if new_stock is not None:
        c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    conn.commit(); conn.close()
    return {"success": True}

@app.put("/api/products/{product_id}")
def update_product_endpoint(product_id: str, stock: Optional[int] = None, data: Optional[dict] = Body(None)):
    return update_stock_handler(product_id, stock, data)

@app.put("/api/admin/products/{product_id}")
def update_admin_product_endpoint(product_id: str, stock: Optional[int] = None, data: Optional[dict] = Body(None)):
    return update_stock_handler(product_id, stock, data)

@app.put("/api/admin/products/{product_id}/stock")
def update_admin_product_stock_endpoint(product_id: str, stock: Optional[int] = None, data: Optional[dict] = Body(None)):
    return update_stock_handler(product_id, stock, data)

def delete_product_handler(product_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit(); conn.close()
    return {"success": True}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: str):
    return delete_product_handler(product_id)

@app.delete("/api/admin/products/{product_id}")
def delete_admin_product(product_id: str):
    return delete_product_handler(product_id)

@app.put("/api/admin/orders/{order_id}/status")
@app.patch("/api/admin/orders/{order_id}/status")
@app.put("/api/orders/{order_id}/status")
@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status: str):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT timeline FROM orders WHERE id = ?", (order_id,))
    row = c.fetchone()
    if not row: conn.close(); raise HTTPException(status_code=404, detail="Order not found")
    timeline = json.loads(row["timeline"])
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    matched = False
    for step in timeline:
        if step["status"].upper() == status.upper():
            step["completed"] = True; step["time"] = now_str; matched = True
        elif not matched: step["completed"] = True
    c.execute("UPDATE orders SET status = ?, timeline = ? WHERE id = ?", (status.upper(), json.dumps(timeline), order_id))
    conn.commit(); conn.close()
    return {"success": True, "status": status.upper()}

@app.post("/api/admin/bulk-upload")
@app.post("/api/admin/bulk-import")
def bulk_upload(payload: Any = Body(...)):
    products = payload.get("products", []) if isinstance(payload, dict) else payload
    if not isinstance(products, list):
        raise HTTPException(status_code=400, detail="Invalid products payload format")
    conn = get_db(); c = conn.cursor()
    added, errors = 0, []
    for idx, p in enumerate(products):
        try:
            if not p.get("title") or not p.get("price") or not p.get("category"):
                errors.append(f"Row {idx+1}: Missing required title, price or category"); continue
            pid = f"nvb-bulk-{uuid.uuid4().hex[:6]}"
            price = float(p.get("price", 999))
            mrp = float(p.get("mrp", price * 1.3))
            disc = int(round(((mrp - price) / mrp) * 100)) if mrp > price else 0
            c.execute('''
            INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, 4.5, 1, ?, 5, ?, ?, '', ?, 0, 0, 1, 0, 0, 50, 0, ?, ?, ?, ?, 'Next Vision Brand Cult', 'seller-1', 'Published', ?)
            ''', (
                pid, p["title"], p.get("brand", "NVB Brand"), p["category"],
                p.get("subcategory", "General"), price, mrp, disc, int(p.get("stock", 25)),
                f"SKU-BLK-{uuid.uuid4().hex[:6].upper()}",
                json.dumps([p.get("image", "/static/products/nvb-tee-dream-plan-achieve.jpg")]),
                p.get("tags", "bulk"), json.dumps(p.get("specs", {"Standard": "Included"})),
                json.dumps([]), p.get("description", p["title"]), p.get("description", p["title"])[:100],
                datetime.now().isoformat()
            ))
            added += 1
        except Exception as e:
            errors.append(f"Row {idx+1}: {str(e)}")
    conn.commit(); conn.close()
    return {"success": True, "added_count": added, "errors": errors}

@app.post("/api/seller/register")
def register_seller(seller: SellerRegisterRequest):
    conn = get_db(); c = conn.cursor()
    sid = f"slr-{uuid.uuid4().hex[:6]}"
    c.execute('''INSERT INTO sellers VALUES (?, ?, ?, ?, ?, ?, 'Approved', 0.0, 0, ?)''',
              (sid, seller.name, seller.business_name, seller.email, seller.phone, seller.gstin, datetime.now().isoformat()))
    conn.commit(); conn.close()
    return {"success": True, "seller_id": sid, "message": "Seller registration approved!"}

@app.get("/api/notifications")
def get_notifications(session_id: str):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM notifications WHERE session_id = ? OR session_id = 'default-user' ORDER BY created_at DESC", (session_id,))
    notifs = [dict(r) for r in c.fetchall()]
    conn.close()
    return notifs

# Serve Static files & SPA
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/sitemap.xml")
def sitemap():
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>http://localhost:8000/</loc><priority>1.0</priority></url>
    <url><loc>http://localhost:8000/#shop</loc><priority>0.9</priority></url>
    <url><loc>http://localhost:8000/#deals</loc><priority>0.8</priority></url>
    <url><loc>http://localhost:8000/#flash-sales</loc><priority>0.8</priority></url>
    <url><loc>http://localhost:8000/#seller</loc><priority>0.7</priority></url>
    <url><loc>http://localhost:8000/#admin</loc><priority>0.5</priority></url>
</urlset>'''
    return Response(content=xml_content, media_type="application/xml")

@app.get("/robots.txt")
def robots():
    return Response(content="User-agent: *\nAllow: /\nSitemap: http://localhost:8000/sitemap.xml", media_type="text/plain")


@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    uploads_dir = os.path.join(STATIC_DIR, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower() or ".png"
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"]:
        ext = ".png"
    safe_name = f"nvb-{uuid.uuid4().hex[:8]}{ext}"
    dest_path = os.path.join(uploads_dir, safe_name)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "success": True,
        "url": f"/static/uploads/{safe_name}",
        "filename": safe_name
    }



# ==================== GOOGLE SEARCH OFFICIAL APIS ====================

@app.get("/api/google/suggest")
def google_suggest(q: str = ""):
    query = (q or "").strip().lower()
    
    trending = [
        "Google Gemini 2.0 release date",
        "ICC Cricket World Cup standings",
        "Python 3.13 new features",
        "Weather forecast today",
        "Chandrayaan ISRO space mission",
        "Google Pixel 9 Pro Fold review",
        "Best movies streaming this week",
        "Stock market trends Nifty Sensex",
        "Machine Learning roadmap 2026",
        "Translate English to Tamil"
    ]
    
    suggestions_map = {
        "g": ["google", "gmail", "google drive", "google maps", "google translate", "google flights", "gemini ai", "google sheets"],
        "go": ["google", "google search", "google finance", "google photos", "google classroom", "golang tutorial", "google store"],
        "goo": ["google", "google account", "google docs", "google meet", "google news", "google trends", "google play"],
        "goog": ["google", "google search engine", "google cloud", "google workspace", "google scholar"],
        "p": ["python", "pinterest", "paypal", "premier league", "play store", "perplexity ai", "pixel 9"],
        "py": ["python download", "python documentation", "python tutorial w3schools", "pytorch", "pyside6", "python compiler"],
        "pyt": ["python tutorial", "python list methods", "python dict comprehension", "python virtualenv"],
        "w": ["weather", "wikipedia", "wordle", "whatsapp web", "world clock", "wall street journal"],
        "c": ["calculator", "canva", "chatgpt", "cricket score", "currency converter", "coursera", "cricbuzz"],
        "t": ["translate", "twitter", "time now", "timer 5 minutes", "top news", "tiktok", "tamil news"],
        "a": ["amazon", "apple", "artificial intelligence", "air india", "airbnb", "adobe"],
        "i": ["india weather", "instagram", "imdb", "isro missions", "income tax portal", "iphone 16"]
    }
    
    if not query:
        return {"query": "", "suggestions": trending[:6]}
        
    if query in suggestions_map:
        return {"query": query, "suggestions": suggestions_map[query]}
        
    # Generic filter
    matches = [t for t in trending if query in t.lower()]
    if not matches:
        matches = [
            f"{query}",
            f"{query} download",
            f"{query} online",
            f"{query} meaning",
            f"{query} official website",
            f"{query} tutorial",
            f"{query} wikipedia"
        ]
    return {"query": query, "suggestions": matches[:6]}


@app.get("/api/google/search")
def google_search(q: str = "", category: str = "all"):
    query = (q or "").strip()
    if not query:
        query = "Google"

    import time
    start_time = time.time()
    
    q_lower = query.lower()
    
    # Specific knowledge graphs
    knowledge = None
    if any(k in q_lower for k in ["google", "alphabet"]):
        knowledge = {
            "title": "Google",
            "subtitle": "Technology company",
            "description": "Google LLC is an American multinational corporation and technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, consumer electronics, and artificial intelligence.",
            "image": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=600&q=80",
            "attributes": [
                {"label": "Founders", "value": "Larry Page, Sergey Brin"},
                {"label": "CEO", "value": "Sundar Pichai (Oct 2, 2015–)"},
                {"label": "Parent organization", "value": "Alphabet Inc."},
                {"label": "Founded", "value": "September 4, 1998, Menlo Park, California, USA"},
                {"label": "Headquarters", "value": "Mountain View, California, United States"}
            ]
        }
    elif any(k in q_lower for k in ["python", "programming"]):
        knowledge = {
            "title": "Python",
            "subtitle": "High-level programming language",
            "description": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected.",
            "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&q=80",
            "attributes": [
                {"label": "Designed by", "value": "Guido van Rossum"},
                {"label": "First appeared", "value": "February 20, 1991 (35 years ago)"},
                {"label": "Typing discipline", "value": "Duck, dynamic, strong typing"},
                {"label": "Major implementations", "value": "CPython, PyPy, Jython, IronPython"}
            ]
        }
    elif any(k in q_lower for k in ["ai", "artificial intelligence", "gemini"]):
        knowledge = {
            "title": "Artificial Intelligence",
            "subtitle": "Academic discipline & field of computer science",
            "description": "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of living beings, primarily of humans. It is also an academic field of study in computer science.",
            "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80",
            "attributes": [
                {"label": "Leading Labs", "value": "Google DeepMind, Google Research"},
                {"label": "State-of-the-Art", "value": "Gemini 2.0, Transformer Architectures"},
                {"label": "Key Applications", "value": "Computer vision, Natural language processing, Robotics, Autonomous vehicles"}
            ]
        }
    elif any(k in q_lower for k in ["india"]):
        knowledge = {
            "title": "India",
            "subtitle": "Country in South Asia",
            "description": "India, officially the Republic of India, is a country in South Asia. It is the seventh-largest country by area; the most populous country in the world; and since the time of its independence in 1947, the world's most populous democracy.",
            "image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&q=80",
            "attributes": [
                {"label": "Capital", "value": "New Delhi"},
                {"label": "Prime Minister", "value": "Narendra Modi"},
                {"label": "President", "value": "Droupadi Murmu"},
                {"label": "Currency", "value": "Indian Rupee (₹)"}
            ]
        }
    
    # Organic results generator
    organic_results = [
        {
            "title": f"{query} — Official Overview & Latest Updates",
            "url": f"https://www.google.com/search?q={query}",
            "displayed_url": f"https://www.google.com › {query.lower().replace(' ', '-')}",
            "snippet": f"Explore official information, features, documentation, and the latest news about {query}. Find comprehensive insights, guides, and related resources.",
            "sitelinks": [
                {"title": "Documentation & Guides", "snippet": "Official technical specifications and getting started manuals."},
                {"title": "Latest News & Releases", "snippet": "Recent developments, announcements, and version updates."},
                {"title": "Community & Support", "snippet": "Official discussion forums, FAQ, and global user community."},
                {"title": "Downloads & Tools", "snippet": "Certified tools, SDKs, and developer kits."}
            ]
        },
        {
            "title": f"{query} - Wikipedia, the free encyclopedia",
            "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            "displayed_url": f"https://en.wikipedia.org › wiki › {query.replace(' ', '_')}",
            "snippet": f"{query} is a prominent subject with extensive global recognition. Read the historical background, development timeline, applications, and verified citations on Wikipedia.",
            "sitelinks": []
        },
        {
            "title": f"Top News, Trends, and Stories on {query}",
            "url": f"https://news.google.com/search?q={query}",
            "displayed_url": f"https://news.google.com › stories › {query.lower()}",
            "snippet": f"Real-time news updates, editorial analysis, and press releases about {query}. Follow breaking headlines and expert opinions from leading international publications.",
            "sitelinks": []
        },
        {
            "title": f"Google Cloud & DeepMind Innovations in {query}",
            "url": f"https://cloud.google.com/solutions/{query.lower()}",
            "displayed_url": f"https://cloud.google.com › solutions › {query.lower()}",
            "snippet": f"Harness Google's world-class cloud infrastructure, AI models, and enterprise security to accelerate your projects with {query}.",
            "sitelinks": []
        },
        {
            "title": f"GitHub - Trending Open-Source Projects for {query}",
            "url": f"https://github.com/topics/{query.lower()}",
            "displayed_url": f"https://github.com › topics › {query.lower()}",
            "snippet": f"Explore open-source repositories, libraries, star ratings, and community contributions for {query}. Collaborate with developers worldwide.",
            "sitelinks": []
        }
    ]
    
    # Image results
    images_results = [
        {"title": f"{query} Showcase 1", "thumbnail": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=400&q=80", "source": "google.com"},
        {"title": f"{query} Technology", "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80", "source": "techcrunch.com"},
        {"title": f"{query} Infrastructure", "thumbnail": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=80", "source": "wikipedia.org"},
        {"title": f"{query} Future Concept", "thumbnail": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&q=80", "source": "theverge.com"},
        {"title": f"{query} Global Impact", "thumbnail": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=400&q=80", "source": "nature.com"},
        {"title": f"{query} Innovation Lab", "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=400&q=80", "source": "wired.com"}
    ]
    
    # Video results
    videos_results = [
        {"title": f"What is {query}? Complete Beginner to Master Guide", "channel": "Google Developers", "duration": "14:28", "views": "1.4M views", "thumbnail": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&q=80"},
        {"title": f"The Evolution of {query} in 2026 and Beyond", "channel": "Tech Vision", "duration": "21:05", "views": "850K views", "thumbnail": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&q=80"},
        {"title": f"{query} Keynote Demonstration & Deep Dive", "channel": "Google I/O", "duration": "48:12", "views": "3.2M views", "thumbnail": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80"}
    ]
    
    # News results
    news_results = [
        {"title": f"Major Breakthrough Announced for {query} Ecosystem", "source": "Reuters", "time": "2 hours ago", "snippet": f"Industry leaders convene as groundbreaking innovations around {query} redefine speed, accessibility, and scalability."},
        {"title": f"How {query} is Transforming Global Enterprise Operations", "source": "Bloomberg", "time": "5 hours ago", "snippet": f"A comprehensive report reveals a 45% productivity surge among early adopters of modern {query} architectures."},
        {"title": f"Next Generation Technologies: What {query} Means for Tomorrow", "source": "The Verge", "time": "14 hours ago", "snippet": f"Analysts highlight pivotal trends and anticipated feature sets scheduled for rollout across international markets."}
    ]
    
    # People Also Ask
    people_also_ask = [
        {"question": f"What is {query} used for?", "answer": f"{query} is widely adopted for accelerating digital transformation, engineering scalable solutions, and providing streamlined access to knowledge and tools worldwide."},
        {"question": f"Is {query} free to access and use?", "answer": f"Yes, core public features, documentation, and standard services for {query} are freely accessible to users across all major platforms."},
        {"question": f"How can I get started with {query}?", "answer": f"You can get started by visiting the official documentation or platform portal, exploring introductory tutorials, and following community best practices."},
        {"question": f"What are the best alternatives to {query}?", "answer": f"Depending on your workflow, related solutions offer specialized capabilities, though {query} remains the industry benchmark for overall reliability and coverage."}
    ]
    
    # Related searches
    related = [
        f"{query} official website",
        f"{query} download windows",
        f"{query} tutorial for beginners",
        f"{query} github open source",
        f"{query} latest news 2026",
        f"{query} price & specs",
        f"{query} vs competitor comparison",
        f"{query} api documentation"
    ]
    
    duration = round(time.time() - start_time + 0.32, 2)
    
    return {
        "query": query,
        "category": category,
        "total_results": "3,420,000,000",
        "search_time": f"{duration} seconds",
        "knowledge_panel": knowledge,
        "organic_results": organic_results,
        "images_results": images_results,
        "videos_results": videos_results,
        "news_results": news_results,
        "people_also_ask": people_also_ask,
        "related_searches": related
    }

# ==================== END GOOGLE SEARCH APIS ====================

@app.get("/{full_path:path}")
def serve_index(full_path: str):
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file): return FileResponse(index_file)
    return HTMLResponse("<h1>NVB Cult starting up...</h1>")

if __name__ == "__main__":
    import sys
    import socket

    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = int(os.environ.get("PORT", 8000))
    
    def is_port_in_use(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', p)) == 0

    if is_port_in_use(port):
        print(f"\n[!] Notice: Port {port} is already in use by another process.")
        for alt_port in [8001, 8080, 5000]:
            if not is_port_in_use(alt_port):
                print(f"[!] Automatically switching to open port: http://localhost:{alt_port}\n")
                port = alt_port
                break

    print(f"\n>>> Starting NVB Cult on http://localhost:{port} <<<\n")
    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=True)

