import sqlite3

def update_brand():
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    c.execute("UPDATE products SET brand = 'Next Vision Brand Cult', seller_name = 'Next Vision Brand Cult Official Store'")
    print(f"Updated {c.rowcount} products to brand 'Next Vision Brand Cult'.")
    
    # Also update sellers table
    c.execute("UPDATE sellers SET name = 'Next Vision Brand Cult Official', business_name = 'Next Vision Brand Cult Retail Ltd.' WHERE id = 'seller-1'")
    
    c.execute("SELECT id, title, brand, seller_name FROM products LIMIT 3")
    for r in c.fetchall():
        print("Product:", r)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_brand()
