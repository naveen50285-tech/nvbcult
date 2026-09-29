import os
import sqlite3
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'marketplace.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        brand TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        price REAL NOT NULL,
        mrp REAL NOT NULL,
        discount INTEGER NOT NULL,
        rating REAL NOT NULL,
        review_count INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        low_stock_threshold INTEGER DEFAULT 10,
        sku TEXT UNIQUE,
        images TEXT NOT NULL,
        video_url TEXT,
        tags TEXT,
        is_featured INTEGER DEFAULT 0,
        is_bestseller INTEGER DEFAULT 0,
        is_new INTEGER DEFAULT 0,
        is_flash_sale INTEGER DEFAULT 0,
        is_deal_of_day INTEGER DEFAULT 0,
        flash_stock_limit INTEGER DEFAULT 50,
        flash_sold INTEGER DEFAULT 0,
        specs TEXT NOT NULL,
        variants TEXT NOT NULL,
        description TEXT NOT NULL,
        short_description TEXT NOT NULL,
        seller_name TEXT NOT NULL,
        seller_id TEXT NOT NULL,
        status TEXT DEFAULT 'Published',
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        icon TEXT NOT NULL,
        description TEXT,
        subcategories TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS cart_items (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        variant_name TEXT,
        quantity INTEGER NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS wishlist_items (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        shipping_address TEXT NOT NULL,
        delivery_method TEXT NOT NULL,
        delivery_fee REAL NOT NULL,
        payment_method TEXT NOT NULL,
        payment_status TEXT NOT NULL,
        subtotal REAL NOT NULL,
        discount REAL NOT NULL,
        tax REAL NOT NULL,
        total REAL NOT NULL,
        status TEXT NOT NULL,
        timeline TEXT NOT NULL,
        items TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,
        product_id TEXT NOT NULL,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        title TEXT NOT NULL,
        comment TEXT NOT NULL,
        verified INTEGER DEFAULT 1,
        helpful_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS coupons (
        code TEXT PRIMARY KEY,
        discount_type TEXT NOT NULL,
        discount_value REAL NOT NULL,
        min_order REAL NOT NULL,
        max_discount REAL NOT NULL,
        active INTEGER DEFAULT 1,
        description TEXT
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS sellers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        business_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        gstin TEXT NOT NULL,
        status TEXT DEFAULT 'Approved',
        revenue REAL DEFAULT 0,
        orders_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('DB schema ready')
