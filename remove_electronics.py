import sqlite3

def remove_electronics():
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE category = 'Electronics'")
    count = c.rowcount
    conn.commit()
    print(f"Successfully deleted {count} electronic example products.")
    
    # Check remaining
    c.execute("SELECT category, COUNT(id) FROM products GROUP BY category")
    remaining = c.fetchall()
    print("Remaining products by category:", remaining)
    
    c.execute("SELECT id, name FROM categories")
    print("Categories available:", c.fetchall())
    conn.close()

if __name__ == "__main__":
    remove_electronics()
