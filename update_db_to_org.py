import sqlite3
import json

db_path = "marketplace.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

product_images = {
    "nvb-tee-dream-plan-achieve": ["/static/products/nvb-tee-dream-plan-achieve.jpg"],
    "nvb-tee-golden-eye-horus": ["/static/products/nvb-tee-golden-eye-horus.jpg"],
    "nvb-tee-supima-obsidian-luxury": ["/static/products/nvb-tee-supima-obsidian-luxury.jpg"],
    "nvb-tee-cyberpunk-analog-drop": ["/static/products/nvb-tee-cyberpunk-analog-drop.jpg"],
    "nvb-elec-cyberdeck-anc-earbuds": ["/static/products/nvb-elec-cyberdeck-anc-earbuds.jpg"],
    "nvb-elec-magfast-65w-gan": ["/static/products/nvb-elec-magfast-65w-gan.jpg"],
    "nvb-elec-creator-soundtrack-mic": ["/static/products/nvb-elec-creator-soundtrack-mic.jpg"],
    "nvb-elec-chronosync-amoled-watch": ["/static/products/nvb-elec-chronosync-amoled-watch.jpg"]
}

for pid, imgs in product_images.items():
    c.execute("UPDATE products SET images = ? WHERE id = ?", (json.dumps(imgs), pid))
    print(f"Updated {pid} -> {imgs}")

conn.commit()

# Verify
c.execute("SELECT id, title, images FROM products")
rows = c.fetchall()
print(f"\nTotal products in database: {len(rows)}")
for r in rows:
    print(f"  {r[0]}: {json.loads(r[2])}")

conn.close()
