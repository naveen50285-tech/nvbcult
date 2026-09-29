import os
import json
import uuid
import sqlite3
from datetime import datetime
import streamlit as st
from PIL import Image

# ==================== STREAMLIT PAGE CONFIG ====================
st.set_page_config(
    page_title="NVB Cult // Official Store (Est. 2026)",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "marketplace.db")
STATIC_DIR = os.path.join(BASE_DIR, "static")
PRODUCTS_DIR = os.path.join(STATIC_DIR, "products")
LOGO_PATH = os.path.join(STATIC_DIR, "nvb-logo.png")

# ==================== CUSTOM LUXURY BLACK & GOLD CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800;900&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-main: #09090d;
        --bg-card: #121218;
        --bg-card-hover: #181822;
        --gold: #d4af37;
        --gold-bright: #fbbf24;
        --gold-glow: rgba(212, 175, 55, 0.25);
        --border-gold: rgba(212, 175, 55, 0.35);
        --text-white: #ffffff;
        --text-dim: #cbd5e1;
        --text-muted: #94a3b8;
    }

    /* Base Streamlit App Overrides */
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-white) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Global Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        color: var(--text-white) !important;
        letter-spacing: 0.04em !important;
    }

    /* Streamlit top header hide decoration */
    header[data-testid="stHeader"] {
        background-color: rgba(9, 9, 13, 0.95) !important;
        backdrop-filter: blur(8px) !important;
    }

    /* Top Marquee Banner */
    .cult-ticker {
        background: #0d0d12;
        border-top: 1px solid var(--border-gold);
        border-bottom: 1px solid var(--border-gold);
        padding: 8px 16px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        color: var(--gold-bright);
        letter-spacing: 0.1em;
        margin-bottom: 24px;
        border-radius: 4px;
    }
    .ticker-highlight {
        background: var(--gold);
        color: #000000;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 2px;
    }

    /* Product Card Luxury Styling */
    .product-box {
        background: var(--bg-card);
        border: 1px solid var(--border-gold);
        border-radius: 6px;
        padding: 16px;
        transition: all 0.25s ease;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .product-box:hover {
        border-color: var(--gold-bright);
        box-shadow: 0 6px 25px var(--gold-glow);
        transform: translateY(-2px);
    }
    .product-sku {
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: var(--gold);
        letter-spacing: 0.08em;
    }
    .product-badge {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: 9px;
        font-weight: 700;
        background: rgba(212, 175, 55, 0.15);
        color: var(--gold-bright);
        border: 1px solid var(--border-gold);
        padding: 2px 8px;
        border-radius: 3px;
        margin-top: 4px;
    }
    .product-title {
        font-family: 'Cinzel', serif;
        font-size: 16px;
        font-weight: 700;
        color: var(--text-white);
        margin: 8px 0;
        line-height: 1.3;
        min-height: 42px;
    }
    .price-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin: 10px 0 14px 0;
        font-family: 'Space Mono', monospace;
    }
    .price-val {
        font-size: 20px;
        font-weight: 800;
        color: var(--gold-bright);
    }
    .mrp-val {
        font-size: 13px;
        color: var(--text-muted);
        text-decoration: line-through;
    }
    .discount-val {
        font-size: 11px;
        color: #22c55e;
        font-weight: 700;
    }

    /* Luxury Gold Buttons */
    .stButton>button {
        background: var(--gold) !important;
        color: #000000 !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        border: 1.5px solid var(--gold-bright) !important;
        border-radius: 4px !important;
        box-shadow: 2px 2px 0px #000000 !important;
        transition: all 0.2s ease !important;
        padding: 8px 16px !important;
    }
    .stButton>button:hover {
        background: var(--gold-bright) !important;
        color: #000000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 0 14px var(--gold-glow) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }

    /* Secondary / Outline Button */
    .outline-btn>button {
        background: transparent !important;
        color: var(--gold-bright) !important;
        border: 1px solid var(--border-gold) !important;
    }

    /* Form Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #121218 !important;
        color: #ffffff !important;
        border: 1px solid var(--border-gold) !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--gold-bright) !important;
        box-shadow: 0 0 8px var(--gold-glow) !important;
    }

    /* Streamlit Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0d0d12 !important;
        border-bottom: 1.5px solid var(--border-gold) !important;
        gap: 8px;
        padding: 6px 12px !important;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Mono', monospace !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: var(--text-dim) !important;
        border: none !important;
        padding: 8px 18px !important;
        border-radius: 4px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--gold) !important;
        color: #000000 !important;
    }

    /* Metrics & Stat Cards */
    div[data-testid="stMetricValue"] {
        font-family: 'Space Mono', monospace !important;
        color: var(--gold-bright) !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Cinzel', serif !important;
        color: var(--text-dim) !important;
    }

    /* Empty Vault Banner */
    .empty-vault-card {
        background: #121218;
        border: 1.5px dashed var(--border-gold);
        border-radius: 8px;
        padding: 40px 24px;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE HELPERS ====================
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        title TEXT,
        brand TEXT,
        category TEXT,
        subcategory TEXT,
        price REAL,
        mrp REAL,
        discount INTEGER,
        rating REAL,
        review_count INTEGER,
        stock INTEGER,
        low_stock_threshold INTEGER,
        sku TEXT,
        images TEXT,
        video_url TEXT,
        tags TEXT,
        is_featured INTEGER,
        is_bestseller INTEGER,
        is_new INTEGER,
        is_flash_sale INTEGER,
        is_deal_of_day INTEGER,
        flash_stock_limit INTEGER,
        flash_sold INTEGER,
        specs TEXT,
        variants TEXT,
        description TEXT,
        short_description TEXT,
        seller_name TEXT,
        seller_id TEXT,
        status TEXT,
        created_at TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        session_id TEXT,
        customer_name TEXT,
        customer_email TEXT,
        customer_phone TEXT,
        shipping_address TEXT,
        delivery_method TEXT,
        delivery_fee REAL,
        payment_method TEXT,
        payment_status TEXT,
        subtotal REAL,
        discount REAL,
        tax REAL,
        total REAL,
        status TEXT,
        timeline TEXT,
        items TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

def load_products_from_db(category="all", search=""):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM products WHERE status = 'Published'"
    params = []
    
    if category != "all":
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)
        
    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(category) LIKE ? OR LOWER(tags) LIKE ?)"
        s = f"%{search.lower()}%"
        params.extend([s, s, s])
        
    query += " ORDER BY is_featured DESC, created_at DESC"
    c.execute(query, params)
    rows = c.fetchall()
    
    products = []
    for r in rows:
        imgs = json.loads(r["images"]) if r["images"] else []
        img_url = imgs[0] if imgs else "/static/products/nvb-tee-dream-plan-achieve.jpg"
        # Convert relative to absolute for PIL if local
        if img_url.startswith("/"):
            local_p = os.path.join(BASE_DIR, img_url.lstrip("/"))
        else:
            local_p = img_url
            
        products.append({
            "id": r["id"],
            "title": r["title"],
            "brand": r["brand"] or "NVB Cult",
            "category": r["category"],
            "subcategory": r["subcategory"] or "",
            "price": float(r["price"]),
            "mrp": float(r["mrp"]) if r["mrp"] else float(r["price"]) * 1.5,
            "discount": int(r["discount"]) if r["discount"] else 0,
            "rating": float(r["rating"]) if r["rating"] else 5.0,
            "review_count": int(r["review_count"]) if r["review_count"] else 12,
            "stock": int(r["stock"]),
            "sku": r["sku"] or "NVB-CULT",
            "image_path": local_p,
            "image_url": img_url,
            "short_description": r["short_description"] or "",
            "description": r["description"] or "",
            "specs": json.loads(r["specs"]) if r["specs"] else {},
            "variants": json.loads(r["variants"]) if r["variants"] else []
        })
    conn.close()
    return products

def get_orders_from_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY created_at DESC")
    rows = c.fetchall()
    orders = []
    for r in rows:
        orders.append({
            "id": r["id"],
            "customer_name": r["customer_name"],
            "customer_phone": r["customer_phone"],
            "shipping_address": r["shipping_address"],
            "payment_method": r["payment_method"],
            "total": float(r["total"]),
            "status": r["status"],
            "items": json.loads(r["items"]) if r["items"] else [],
            "created_at": r["created_at"]
        })
    conn.close()
    return orders

# ==================== STATE MANAGEMENT ====================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = [
        {"role": "assistant", "content": "✦ **Cult AI Comm-Link Active.** Welcome to **NVB Cult (Next Vision Brand)** — Founded in 2026 under the vision **DREAM • PLAN • ACHIEVE**. Ask me about our 260 GSM French Terry drops, sizing guide (S to XXL), or creator electronics!"}
    ]

# ==================== HEADER SECTION ====================
col_logo, col_title, col_actions = st.columns([1.2, 5, 2])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=95)
    else:
        st.markdown("<h2 style='color:#d4af37;'>👑 NVB</h2>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
        <div style="padding-top: 4px;">
            <h1 style="margin: 0; font-size: 28px; line-height: 1.1;">
                NEXT VISION <span style="color:#d4af37;">BRAND CULT</span>
            </h1>
            <div style="font-family:'Space Mono', monospace; font-size: 11px; color:#fbbf24; margin-top: 4px; letter-spacing:0.08em;">
                DREAM • PLAN • ACHIEVE &nbsp;|&nbsp; EST. 2026 &nbsp;|&nbsp; OFFICIAL STORE
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_actions:
    cart_total_qty = sum(item["quantity"] for item in st.session_state.cart)
    st.markdown(f"""
        <div style="text-align: right; padding-top: 10px;">
            <span style="font-family:'Space Mono', monospace; font-size: 12px; background:rgba(212,175,55,0.15); border:1px solid #d4af37; padding:6px 12px; border-radius:4px; color:#fbbf24;">
                🛍️ BAG: <b>{cart_total_qty} DROPS</b>
            </span>
        </div>
    """, unsafe_allow_html=True)

# Ticker tape
st.markdown("""
    <div class="cult-ticker">
        <span><span class="ticker-highlight">MOTTO</span> DREAM • PLAN • ACHIEVE</span>
        <span>✦ 100% HEAVYWEIGHT 260 GSM FRENCH TERRY</span>
        <span>✦ NEXT VISION BRAND CULT // EST. 2026</span>
        <span>✦ CODE <span class="ticker-highlight">VISION10</span> FOR 10% OFF</span>
    </div>
""", unsafe_allow_html=True)

# ==================== MAIN TABS ====================
tab_store, tab_bag, tab_owner, tab_ai, tab_manifesto = st.tabs([
    "🛍️ STORE ARCHIVE",
    f"🎒 BAG ARCHIVE ({cart_total_qty})",
    "👑 OWNER CONSOLE",
    "💬 CULT AI COMM-LINK",
    "📜 COMPANY MANIFESTO"
])

# ==============================================================================
# TAB 1: STORE ARCHIVE (STOREFRONT)
# ==============================================================================
with tab_store:
    # Filter & Search Row
    col_search, col_cat, col_sort = st.columns([3, 2, 2])
    
    with col_search:
        search_query = st.text_input("🔍 Scan Specimen Archive", placeholder="Search 260 GSM tees, GaN charger, audio...").strip()
    
    with col_cat:
        cat_filter = st.selectbox(
            "Category Filter",
            options=["All Archive", "T-Shirts", "Electronics"],
            index=0
        )
    
    with col_sort:
        sort_choice = st.selectbox(
            "Sort Specimens",
            options=["Featured Drops", "Price: Low to High", "Price: High to Low", "Highest Rating"],
            index=0
        )
        
    db_cat = "all" if cat_filter == "All Archive" else cat_filter
    products = load_products_from_db(category=db_cat, search=search_query)
    
    # Sorting logic
    if sort_choice == "Price: Low to High":
        products.sort(key=lambda p: p["price"])
    elif sort_choice == "Price: High to Low":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif sort_choice == "Highest Rating":
        products.sort(key=lambda p: p["rating"], reverse=True)
        
    st.write("") # spacing
    
    # Live catalog display or empty archive box
    if len(products) == 0:
        st.markdown(f"""
            <div class="empty-vault-card">
                <div style="font-size: 48px; margin-bottom: 12px;">👑</div>
                <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(34,197,94,0.12); border:1.5px solid rgba(34,197,94,0.4); padding:6px 14px; border-radius:4px; font-family:'Space Mono', monospace; font-size:11px; color:#22c55e; margin-bottom:16px;">
                    <span style="width:7px; height:7px; background:#22c55e; border-radius:50%; box-shadow:0 0 6px #22c55e;"></span>
                    <span>SQLITE DATABASE CONNECTED: 0 PRODUCTS STORED</span>
                </div>
                <h3 style="font-size: 22px; color:#ffffff; margin: 8px 0;">NVB Cult Archive Clear</h3>
                <p style="color: #cbd5e1; font-size: 14px; max-width: 520px; margin: 0 auto 20px auto;">
                    All placeholder and demo products have been removed. The vault is clean and primed for authentic drops. As the store owner, you can upload original specimens or restore the official 8-piece release below.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col_restore_1, col_restore_2 = st.columns([1, 1])
        with col_restore_1:
            if st.button("✦ RESTORE OFFICIAL 8 NVB CULT SPECIMENS", use_container_width=True):
                try:
                    import seed_nvb_cult_catalog
                    seed_nvb_cult_catalog.seed_nvb_cult()
                    st.success("✓ 8 Authentic NVB Cult specimens restored to database!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error restoring catalog: {e}")
        with col_restore_2:
            st.info("💡 Or switch to the **👑 OWNER CONSOLE** tab above to upload your own custom product with photo & price!")

    else:
        st.markdown(f"<div style='font-family:\"Space Mono\", monospace; font-size:12px; color:#fbbf24; margin-bottom:14px;'>DISPLAYING {len(products)} VERIFIED SPECIMENS</div>", unsafe_allow_html=True)
        
        # Grid layout: 3 columns per row
        cols = st.columns(3)
        for i, prod in enumerate(products):
            col = cols[i % 3]
            with col:
                st.markdown("""<div class="product-box">""", unsafe_allow_html=True)
                
                # Product Image
                img_p = prod["image_path"]
                if os.path.exists(img_p):
                    st.image(img_p, use_container_width=True)
                else:
                    # Fallback to DPA tee or logo
                    fallback = os.path.join(PRODUCTS_DIR, "nvb-tee-dream-plan-achieve.jpg")
                    if os.path.exists(fallback):
                        st.image(fallback, use_container_width=True)
                    else:
                        st.image(LOGO_PATH, use_container_width=True)
                        
                st.markdown(f"""
                    <div class="product-sku">{prod['sku']}</div>
                    <span class="product-badge">{prod['category']} • {prod['subcategory']}</span>
                    <div class="product-title">{prod['title']}</div>
                    <div style="font-size: 12px; color: #94a3b8; min-height: 36px;">
                        {prod['short_description'][:85]}...
                    </div>
                    <div class="price-row">
                        <span class="price-val">₹{prod['price']:,.0f}</span>
                        <span class="mrp-val">₹{prod['mrp']:,.0f}</span>
                        <span class="discount-val">{prod['discount']}% OFF</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Select size variant if tee
                variant_names = [v.get("name", "Standard") for v in prod["variants"]] if prod["variants"] else ["Standard"]
                chosen_var = st.selectbox(
                    f"Size/Variant",
                    options=variant_names,
                    key=f"var_{prod['id']}",
                    label_visibility="collapsed"
                )
                
                btn_add, btn_details = st.columns([2, 1])
                with btn_add:
                    if st.button(f"+ ADD TO BAG", key=f"add_{prod['id']}", use_container_width=True):
                        # Add item to session cart
                        existing = next((item for item in st.session_state.cart if item["product"]["id"] == prod["id"] and item["variant"] == chosen_var), None)
                        if existing:
                            existing["quantity"] += 1
                        else:
                            st.session_state.cart.append({
                                "product": prod,
                                "variant": chosen_var,
                                "quantity": 1
                            })
                        st.toast(f"✓ Added '{prod['title'][:25]}' ({chosen_var}) to Bag!", icon="🛍️")
                        st.rerun()
                        
                with btn_details:
                    with st.popover("👁️ SPECS"):
                        st.markdown(f"### {prod['title']}")
                        st.markdown(f"**SKU:** `{prod['sku']}` | **Price:** ₹{prod['price']:,.0f}")
                        st.write(prod['description'])
                        st.markdown("#### Technical Breakdown:")
                        for k, v in prod['specs'].items():
                            st.markdown(f"- **{k}:** {v}")
                            
                st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: BAG ARCHIVE & CHECKOUT
# ==============================================================================
with tab_bag:
    st.markdown("## 🎒 BAG ARCHIVE & DISPATCH")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>Review selected luxury specimens and confirm courier dispatch.</p>", unsafe_allow_html=True)
    
    if len(st.session_state.cart) == 0:
        st.markdown("""
            <div class="empty-vault-card">
                <div style="font-size: 40px; margin-bottom: 8px;">🛍️</div>
                <h3 style="font-size: 18px; color:#ffffff;">Your Bag Archive is Empty</h3>
                <p style="color: #cbd5e1; font-size: 13px;">Add 260 GSM French Terry drops or creator tech from the Store Archive.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col_cart_items, col_checkout = st.columns([3, 2])
        
        with col_cart_items:
            subtotal = 0.0
            for idx, item in enumerate(st.session_state.cart):
                p = item["product"]
                qty = item["quantity"]
                var = item["variant"]
                item_total = p["price"] * qty
                subtotal += item_total
                
                with st.container():
                    c_img, c_info, c_qty, c_del = st.columns([1, 2.5, 1.2, 0.8])
                    with c_img:
                        if os.path.exists(p["image_path"]):
                            st.image(p["image_path"], width=70)
                        else:
                            st.image(LOGO_PATH, width=70)
                    with c_info:
                        st.markdown(f"**{p['title']}**")
                        st.markdown(f"<span style='font-family:\"Space Mono\", monospace; font-size:11px; color:#fbbf24;'>{var} • ₹{p['price']:,.0f} each</span>", unsafe_allow_html=True)
                    with c_qty:
                        st.write(f"Qty: **{qty}**")
                        st.markdown(f"<b style='color:#fbbf24; font-family:\"Space Mono\";'>₹{item_total:,.0f}</b>", unsafe_allow_html=True)
                    with c_del:
                        if st.button("✕", key=f"del_{idx}"):
                            st.session_state.cart.pop(idx)
                            st.rerun()
                    st.divider()
                    
            if st.button("Clear Bag Archive"):
                st.session_state.cart = []
                st.rerun()

        with col_checkout:
            st.markdown("""
                <div style="background:#121218; border:1px solid rgba(212,175,55,0.35); padding:20px; border-radius:6px;">
                    <h3 style="margin-top:0; font-size:18px; color:#ffffff;">Order Summary</h3>
            """, unsafe_allow_html=True)
            
            # Coupon code
            coupon = st.text_input("Promo Code", placeholder="e.g. VISION10").strip().upper()
            discount = 0.0
            if coupon == "VISION10":
                discount = round(subtotal * 0.10, 2)
                st.success("✓ Promo Code VISION10 Applied: 10% Off!")
                
            delivery_fee = 0.0
            tax = round((subtotal - discount) * 0.18, 2)
            total_payable = round(subtotal - discount + delivery_fee, 2)
            
            st.markdown(f"""
                <div style="font-family:'Space Mono', monospace; font-size:13px; line-height:2;">
                    <div style="display:flex; justify-content:space-between;"><span>Subtotal:</span> <span>₹{subtotal:,.2f}</span></div>
                    <div style="display:flex; justify-content:space-between; color:#22c55e;"><span>Discount:</span> <span>-₹{discount:,.2f}</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>GST (18% Included):</span> <span>₹{tax:,.2f}</span></div>
                    <div style="display:flex; justify-content:space-between; color:#fbbf24;"><span>Express Courier:</span> <span>FREE</span></div>
                    <hr style="border-color:rgba(212,175,55,0.3); margin:8px 0;">
                    <div style="display:flex; justify-content:space-between; font-size:18px; font-weight:800; color:#fbbf24;">
                        <span>TOTAL:</span> <span>₹{total_payable:,.2f}</span>
                    </div>
                </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.markdown("#### Dispatch Details:")
            c_name = st.text_input("Full Name", placeholder="e.g. Karthik").strip()
            c_phone = st.text_input("Phone Number", placeholder="10-digit mobile number").strip()
            c_addr = st.text_area("Delivery Address", placeholder="Door No, Street, City, Pincode").strip()
            c_pay = st.selectbox("Payment Mode", ["Cash on Delivery (COD)", "UPI / Instant Pay", "Net Banking"])
            
            if st.button("CONFIRM DISPATCH & PLACE ORDER", use_container_width=True):
                if not c_name or not c_phone or not c_addr:
                    st.error("Please fill in your Name, Phone Number, and Address!")
                else:
                    order_id = f"NVB-2026-{uuid.uuid4().hex[:6].upper()}"
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    timeline = [
                        {"status": "ORDER PLACED", "time": now_str, "desc": "Order placed successfully"},
                        {"status": "CONFIRMED", "time": "In 15 mins", "desc": "Vault confirmed order"},
                        {"status": "DISPATCH READY", "time": "Tomorrow", "desc": "Tamper-proof NVB packaging"}
                    ]
                    
                    order_items = [{
                        "product_id": it["product"]["id"],
                        "title": it["product"]["title"],
                        "price": it["product"]["price"],
                        "quantity": it["quantity"],
                        "variant": it["variant"]
                    } for it in st.session_state.cart]
                    
                    conn = get_db()
                    c = conn.cursor()
                    c.execute('''
                    INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ORDER PLACED', ?, ?, ?)
                    ''', (
                        order_id, "streamlit-session", c_name, "cult@nvb.com", c_phone,
                        c_addr, "Standard Free Delivery", 0.0, c_pay,
                        "Pending (COD)" if "COD" in c_pay else "Paid",
                        subtotal, discount, tax, total_payable, json.dumps(timeline),
                        json.dumps(order_items), datetime.now().isoformat()
                    ))
                    # Deduct stock
                    for it in order_items:
                        c.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?", (it["quantity"], it["product_id"]))
                    conn.commit()
                    conn.close()
                    
                    # Clear cart
                    st.session_state.cart = []
                    st.balloons()
                    st.success(f"""
                        🎉 **DISPATCH ORDER CONFIRMED!**
                        
                        **Order ID:** `#{order_id}`  
                        **Customer:** {c_name} ({c_phone})  
                        **Total Amount:** ₹{total_payable:,.2f}  
                        **Payment:** {c_pay}  
                        
                        *Your package is being prepared with tamper-proof packaging at the NVB Cult Vault.*
                    """)

# ==============================================================================
# TAB 3: OWNER COMMAND CONSOLE
# ==============================================================================
with tab_owner:
    st.markdown("## 👑 OWNER COMMAND CONSOLE")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>Secure access for Next Vision Brand Cult vault administration.</p>", unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown("""
                <div style="background:#121218; border:1px solid #d4af37; padding:24px; border-radius:6px; text-align:center;">
                    <div style="font-size:36px; margin-bottom:8px;">🔒</div>
                    <h3 style="margin-top:0;">Owner Authentication Gate</h3>
                    <p style="font-size:12px; color:#cbd5e1;">Enter your administrative credentials to manage vault inventory and orders.</p>
                </div>
            """, unsafe_allow_html=True)
            u_user = st.text_input("Username", value="admin")
            u_pass = st.text_input("Password", type="password")
            if st.button("AUTHENTICATE AS OWNER", use_container_width=True):
                if u_user.strip() == "admin" and u_pass.strip() == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("✓ Owner Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Default: admin / admin123")
    else:
        # Logged in owner toolbar
        col_own_info, col_own_logout = st.columns([4, 1])
        with col_own_info:
            st.markdown("👑 **STATUS: OWNER SESSION ACTIVE** (`admin`)")
        with col_own_logout:
            if st.button("SIGN OUT"):
                st.session_state.admin_logged_in = False
                st.rerun()
                
        sub_upload, sub_inv, sub_orders, sub_reset = st.tabs([
            "+ UPLOAD SPECIMEN",
            "📊 VAULT INVENTORY",
            "📦 FREIGHT ORDERS",
            "⚙️ VAULT CONTROLS"
        ])
        
        # Sub-tab: Upload Specimen
        with sub_upload:
            st.markdown("### Upload Authentic Product Drop")
            with st.form("add_product_form", clear_on_submit=True):
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    p_title = st.text_input("Drop Title *", placeholder="e.g. NVB Heavy French Terry Oversized Tee")
                    p_cat = st.selectbox("Category *", ["T-Shirts", "Electronics"])
                    p_sub = st.text_input("Subcategory", placeholder="e.g. Oversized Streetwear / Studio Audio")
                    p_sku = st.text_input("SKU Code", placeholder="e.g. NVB-TEE-2026")
                with col_u2:
                    p_price = st.number_input("Selling Price (₹) *", min_value=1.0, value=1499.0, step=50.0)
                    p_mrp = st.number_input("MRP (₹) *", min_value=1.0, value=2999.0, step=50.0)
                    p_stock = st.number_input("Stock Units *", min_value=1, value=50, step=5)
                    p_variants = st.text_input("Variants (Comma separated)", value="S, M, L, XL, XXL" if p_cat == "T-Shirts" else "Standard")
                    
                p_short = st.text_input("One-Line Hook", placeholder="Signature 260 GSM French Terry with metallic gold typography.")
                p_desc = st.text_area("Full Specimen Description", placeholder="Detailed fabric composition, GSM, craftsmanship, warranty...")
                
                # Image Upload
                p_file = st.file_uploader("Upload Original Product Photo (JPG / PNG / WEBP)", type=["jpg", "png", "jpeg", "webp"])
                
                submitted = st.form_submit_button("PUBLISH TO CULT VAULT", use_container_width=True)
                if submitted:
                    if not p_title or p_price <= 0:
                        st.error("Please fill in the product title and a valid price!")
                    else:
                        img_rel_path = "/static/products/nvb-tee-dream-plan-achieve.jpg"
                        if p_file:
                            file_ext = os.path.splitext(p_file.name)[1] or ".jpg"
                            fname = f"nvb-upload-{uuid.uuid4().hex[:8]}{file_ext}"
                            fpath = os.path.join(PRODUCTS_DIR, fname)
                            with open(fpath, "wb") as f_out:
                                f_out.write(p_file.getbuffer())
                            img_rel_path = f"/static/products/{fname}"
                            
                        clean_id = f"nvb-{p_title.lower().replace(' ', '-')[:25]}-{uuid.uuid4().hex[:4]}"
                        sku_val = p_sku if p_sku else f"NVB-{uuid.uuid4().hex[:6].upper()}"
                        disc_calc = int(round(((p_mrp - p_price) / p_mrp) * 100)) if p_mrp > p_price else 0
                        vars_list = [{"name": v.strip(), "stock": int(p_stock // max(1, len(p_variants.split(','))))} for v in p_variants.split(',')]
                        
                        conn = get_db()
                        c = conn.cursor()
                        c.execute('''
                        INSERT INTO products VALUES (?, ?, 'NVB Cult', ?, ?, ?, ?, ?, 5.0, 0, ?, 5, ?, ?, '', ?, 1, 0, 1, 0, 0, 50, 0, ?, ?, ?, ?, 'NVB Cult Official', 'seller-nvb', 'Published', ?)
                        ''', (
                            clean_id, p_title, p_cat, p_sub, p_price, p_mrp, disc_calc,
                            p_stock, sku_val, json.dumps([img_rel_path]), f"{p_cat}, {p_sub}, nvb cult",
                            json.dumps({"Fabric/Material": "Premium NVB Specimen", "Era": "Est. 2026"}),
                            json.dumps(vars_list), p_desc, p_short, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ))
                        conn.commit()
                        conn.close()
                        st.success(f"✓ Product '{p_title}' published to NVB Cult Store successfully!")
                        st.rerun()

        # Sub-tab: Inventory Management
        with sub_inv:
            st.markdown("### Active Vault Inventory")
            all_db_prods = load_products_from_db("all")
            if not all_db_prods:
                st.info("Vault is currently empty.")
            else:
                for p in all_db_prods:
                    with st.container():
                        col_i1, col_i2, col_i3, col_i4 = st.columns([1, 3, 2, 1])
                        with col_i1:
                            if os.path.exists(p["image_path"]):
                                st.image(p["image_path"], width=60)
                            else:
                                st.image(LOGO_PATH, width=60)
                        with col_i2:
                            st.markdown(f"**{p['title']}**")
                            st.markdown(f"`{p['sku']}` | ₹{p['price']:,.0f} | Stock: **{p['stock']} units**")
                        with col_i3:
                            new_stk = st.number_input("Adjust Stock", min_value=0, value=p["stock"], key=f"stk_{p['id']}")
                            if new_stk != p["stock"]:
                                conn = get_db(); c = conn.cursor()
                                c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stk, p["id"]))
                                conn.commit(); conn.close()
                                st.toast(f"Updated stock for {p['title']}")
                                st.rerun()
                        with col_i4:
                            if st.button("🗑️ Delete", key=f"del_prod_{p['id']}"):
                                conn = get_db(); c = conn.cursor()
                                c.execute("DELETE FROM products WHERE id = ?", (p["id"],))
                                conn.commit(); conn.close()
                                st.warning(f"Deleted {p['title']}")
                                st.rerun()
                        st.divider()

        # Sub-tab: Freight Orders
        with sub_orders:
            st.markdown("### Customer Freight Orders")
            orders = get_orders_from_db()
            if not orders:
                st.info("No orders placed yet.")
            else:
                for o in orders:
                    with st.expander(f"📦 #{o['id']} — {o['customer_name']} (₹{o['total']:,.2f}) — Status: {o['status']}"):
                        st.markdown(f"**Customer:** {o['customer_name']} | **Phone:** {o['customer_phone']}")
                        st.markdown(f"**Shipping Address:** {o['shipping_address']}")
                        st.markdown(f"**Payment:** {o['payment_method']} | **Date:** {o['created_at']}")
                        st.markdown("**Ordered Items:**")
                        for it in o["items"]:
                            st.markdown(f"- {it.get('title')} ({it.get('variant')}) x {it.get('quantity')} @ ₹{it.get('price'):,.0f}")
                        
                        col_s1, col_s2 = st.columns([2, 1])
                        with col_s1:
                            new_status = st.selectbox(
                                "Update Order Status",
                                ["ORDER PLACED", "CONFIRMED", "PACKED", "SHIPPED", "DELIVERED", "CANCELLED"],
                                index=["ORDER PLACED", "CONFIRMED", "PACKED", "SHIPPED", "DELIVERED", "CANCELLED"].index(o['status']) if o['status'] in ["ORDER PLACED", "CONFIRMED", "PACKED", "SHIPPED", "DELIVERED", "CANCELLED"] else 0,
                                key=f"status_sel_{o['id']}"
                            )
                        with col_s2:
                            if st.button("Update Status", key=f"btn_st_{o['id']}"):
                                conn = get_db(); c = conn.cursor()
                                c.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, o["id"]))
                                conn.commit(); conn.close()
                                st.success("Status updated!")
                                st.rerun()

        # Sub-tab: Vault Controls
        with sub_reset:
            st.markdown("### Vault Catalog Controls")
            st.markdown("Use these controls to seed or wipe the catalog with 1-click:")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("✦ Seed 8 Authentic NVB Cult Specimens", use_container_width=True):
                    import seed_nvb_cult_catalog
                    seed_nvb_cult_catalog.seed_nvb_cult()
                    st.success("✓ 8 Authentic NVB Cult Specimens Loaded!")
                    st.rerun()
            with col_b2:
                if st.button("⚠️ Clear All Products (Empty Store)", use_container_width=True):
                    conn = get_db(); c = conn.cursor()
                    c.execute("DELETE FROM products")
                    conn.commit(); conn.close()
                    st.warning("All products cleared from catalog.")
                    st.rerun()

# ==============================================================================
# TAB 4: CULT AI COMM-LINK
# ==============================================================================
with tab_ai:
    st.markdown("## 💬 CULT AI COMM-LINK")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>Direct transmission to the Next Vision Brand intelligence terminal.</p>", unsafe_allow_html=True)
    
    # Display message history
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"], avatar="👑" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
            
    # Chat input
    if prompt := st.chat_input("Ask about 260 GSM heavyweight drops, sizing guide, or creator electronics..."):
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        # Generate answer based on NVB Cult knowledge
        p_low = prompt.lower()
        if "size" in p_low or "fit" in p_low or "chart" in p_low:
            resp = """✦ **NVB CULT // SIZING SPECIFICATIONS (260 GSM FRENCH TERRY)**:
- **Small (S):** Chest 42" | Length 28" — True-to-size clean drape.
- **Medium (M):** Chest 44" | Length 29" — Balanced streetwear boxy fit.
- **Large (L):** Chest 46" | Length 30" — Extended drop-shoulder presence.
- **Extra Large (XL):** Chest 48" | Length 31" — Relaxed oversized drape.
- **Double XL (XXL):** Chest 50" | Length 32" — Maximum streetwear silhouette.

*Pre-shrunk and bio-washed for absolute dimensional stability.*"""
        elif "gsm" in p_low or "fabric" in p_low or "cotton" in p_low:
            resp = """✦ **THE 260 GSM FRENCH TERRY ADVANTAGE**:
Unlike standard fast-fashion t-shirts (160–180 GSM), **NVB Cult** uses dense, custom-milled **260 GSM 100% French Terry Cotton**.
- Thick micro-loop interior for sweat absorption and structure.
- Dense knit exterior that holds shape through years of wears.
- 1x1 Lycra ribbed collar that never bacon-curls."""
        elif "electronic" in p_low or "charger" in p_low or "earbud" in p_low or "mic" in p_low or "watch" in p_low:
            resp = """✦ **SIDE B: CREATOR ELECTRONICS VAULT**:
- **CyberDeck ANC Earbuds:** 45dB Hybrid ANC, 12mm Graphene drivers, 48hr battery, 24K gold accents.
- **MagFast 65W GaN Charger:** 3-port GaN III architecture, charges laptops & phones simultaneously.
- **Creator SoundTrack Studio Mic:** Dual XLR & USB-C broadcast dynamic mic with gold mesh grille.
- **ChronoSync Smartwatch:** Titanium & Gold AMOLED dial, health sensors & cyberpunk UI."""
        elif "company" in p_low or "story" in p_low or "founder" in p_low or "manifesto" in p_low or "motto" in p_low or "2026" in p_low:
            resp = """✦ **NEXT VISION BRAND (NVB CULT) // THE MANIFESTO**:
- **Motto:** DREAM • PLAN • ACHIEVE
- **Origin:** Started in 2026
- **Vision:** Bridging heavyweight 260 GSM street apparel with studio creator technology.
- **Philosophy:** No fast fashion. No fragile junk. Timeless black and gold craftsmanship."""
        else:
            resp = f"✦ **Transmission Received:** Regarding '{prompt}'. You can explore all our authentic drops in the **Store Archive** or place a courier order directly from your **Bag Archive**."

        st.session_state.ai_messages.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant", avatar="👑"):
            st.markdown(resp)

# ==============================================================================
# TAB 5: COMPANY MANIFESTO
# ==============================================================================
with tab_manifesto:
    st.markdown("""
        <div style="background:#121218; border:1px solid #d4af37; padding:36px; border-radius:8px; margin-top:16px;">
            <div style="text-align:center;">
                <h1 style="font-size:32px; color:#ffffff; margin-bottom:8px;">NEXT VISION BRAND CULT</h1>
                <div style="font-family:'Space Mono', monospace; font-size:13px; color:#fbbf24; letter-spacing:0.12em;">
                    DREAM • PLAN • ACHIEVE // STARTED IN 2026
                </div>
            </div>
            
            <hr style="border-color:rgba(212,175,55,0.3); margin:24px 0;">
            
            <h3 style="color:#ffffff;">The Cult Doctrine</h3>
            <p style="color:#cbd5e1; line-height:1.8; font-size:15px;">
                <b>NVB Cult</b> was founded in 2026 on a singular conviction: streetwear should not be disposable, and creator technology should not feel fragile. 
                We combine the heavyweight drape of custom-milled <b>260 GSM French Terry cotton</b> with the precision engineering of <b>studio-grade creator electronics</b>.
            </p>
            
            <h3 style="color:#ffffff; margin-top:24px;">The Three Tenets</h3>
            <ul style="color:#cbd5e1; line-height:2; font-size:14px;">
                <li><b style="color:#fbbf24;">DREAM:</b> Bold vision unconstrained by fleeting trends. Every specimen begins as an architectural silhouette.</li>
                <li><b style="color:#fbbf24;">PLAN:</b> Analog precision meets modern materials — 260 GSM dense loop knits, GaN III semiconductors, and graphene acoustic drivers.</li>
                <li><b style="color:#fbbf24;">ACHIEVE:</b> Wear pieces and tools that last for years, aging gracefully with character and intent.</li>
            </ul>
            
            <div style="margin-top:28px; padding:16px; background:#09090d; border-left:3px solid #d4af37; font-family:'Space Mono', monospace; font-size:12px; color:#94a3b8;">
                HEADQUARTERS: NEXT VISION BRAND CULT VAULT<br>
                ESTABLISHED: 2026 &nbsp;|&nbsp; OBSIDIAN BLACK & RADIANT GOLD
            </div>
        </div>
    """, unsafe_allow_html=True)
