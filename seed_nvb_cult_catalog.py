import sqlite3
import json
import uuid
from datetime import datetime

def seed_nvb_cult():
    conn = sqlite3.connect("marketplace.db")
    c = conn.cursor()

    # Clear any old or partial products
    c.execute("DELETE FROM products")
    print("Cleared old products.")

    products = [
        # --- T-SHIRTS (SIDE A) ---
        {
            "id": "nvb-tee-dream-plan-achieve",
            "title": "NVB Cult 'Dream • Plan • Achieve' Heavyweight Tee 260 GSM",
            "brand": "NVB Cult",
            "category": "T-Shirts",
            "subcategory": "Oversized Streetwear",
            "price": 1499.0,
            "mrp": 2999.0,
            "discount": 50,
            "stock": 45,
            "low_stock_threshold": 10,
            "sku": "NVB-TEE-DPA-260",
            "images": [
                "/static/products/nvb-tee-dream-plan-achieve.jpg"
            ],
            "video_url": "",
            "tags": "nvb cult, 260 gsm, heavyweight, dream plan achieve, streetwear, oversized",
            "is_featured": 1,
            "is_bestseller": 1,
            "is_new": 1,
            "is_flash_sale": 0,
            "is_deal_of_day": 1,
            "specs": {
                "Fabric": "100% French Terry Cotton",
                "Weight": "260 GSM Heavyweight Dense Knit",
                "Fit": "Signature Boxy Drop-Shoulder Oversized",
                "Treatment": "Pre-shrunk & Bio-washed for zero shrinkage",
                "Print": "Metallic Gold High-Density Screen Print",
                "Origin": "Crafted by NVB Cult — Est. 2026"
            },
            "variants": [
                {"name": "S", "stock": 10},
                {"name": "M", "stock": 15},
                {"name": "L", "stock": 12},
                {"name": "XL", "stock": 5},
                {"name": "XXL", "stock": 3}
            ],
            "short_description": "Signature 260 GSM French Terry cotton with gold foil typography and drop shoulder posture.",
            "description": "The definitive statement piece from NVB Cult. Crafted from custom-milled 260 GSM French Terry cotton, featuring dense looping on the interior for unmatched drape and thermal breathability. Emblazoned with the 'DREAM • PLAN • ACHIEVE' manifesto in radiant antique gold. Double-stitched ribbed collar that will never bacon or deform.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 5.0,
            "review_count": 38
        },
        {
            "id": "nvb-tee-golden-eye-horus",
            "title": "NVB Golden Eye of Horus Cyber-Graphic Acid Wash Tee",
            "brand": "NVB Cult",
            "category": "T-Shirts",
            "subcategory": "Graphic & Art",
            "price": 1699.0,
            "mrp": 3299.0,
            "discount": 48,
            "stock": 35,
            "low_stock_threshold": 8,
            "sku": "NVB-TEE-EYE-002",
            "images": [
                "/static/products/nvb-tee-golden-eye-horus.jpg"
            ],
            "video_url": "",
            "tags": "horus eye, acid wash, cyber graphic, metallic gold, cult drop",
            "is_featured": 1,
            "is_bestseller": 1,
            "is_new": 1,
            "is_flash_sale": 1,
            "is_deal_of_day": 0,
            "specs": {
                "Fabric": "240 GSM Combed Ring-Spun Cotton",
                "Wash": "Mineral Acid Wash Vintage Obsidian",
                "Graphic": "Golden Eye of Horus & Upward Arrow Emblem",
                "Fit": "Relaxed Streetwear Silhouette",
                "Care": "Cold wash inside-out, hang dry"
            },
            "variants": [
                {"name": "M", "stock": 10},
                {"name": "L", "stock": 15},
                {"name": "XL", "stock": 10}
            ],
            "short_description": "Mineral acid-washed obsidian canvas with the sacred Golden Eye of Horus emblem.",
            "description": "Embodying vision and foresight, this acid-washed tee carries the official NVB Cult emblem. Each piece undergoes an artisanal mineral wash process, giving each garment a unique dark marble patina. Premium soft-hand discharge print with metallic gold fleck detailing.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 4.9,
            "review_count": 24
        },
        {
            "id": "nvb-tee-supima-obsidian-luxury",
            "title": "NVB Obsidian Luxury Supima Plain Minimalist Tee",
            "brand": "NVB Cult",
            "category": "T-Shirts",
            "subcategory": "Supima Plain",
            "price": 1299.0,
            "mrp": 2499.0,
            "discount": 48,
            "stock": 60,
            "low_stock_threshold": 12,
            "sku": "NVB-TEE-SUP-003",
            "images": [
                "/static/products/nvb-tee-supima-obsidian-luxury.jpg"
            ],
            "video_url": "",
            "tags": "supima cotton, minimalist, plain luxury, black gold, classic",
            "is_featured": 0,
            "is_bestseller": 1,
            "is_new": 0,
            "is_flash_sale": 0,
            "is_deal_of_day": 0,
            "specs": {
                "Fabric": "100% American Long-Staple Supima Cotton",
                "Weight": "220 GSM Ultra-Soft Silken Finish",
                "Collar": "Seamless 1x1 Lycra Ribbed Neckband",
                "Branding": "Subtle Gold Embroidered NVB Tab on Hem"
            },
            "variants": [
                {"name": "S", "stock": 10},
                {"name": "M", "stock": 20},
                {"name": "L", "stock": 20},
                {"name": "XL", "stock": 10}
            ],
            "short_description": "Pure American Supima long-staple cotton with silken drape and minimalist gold hem tab.",
            "description": "For those who appreciate unadorned perfection. Woven from extra-long staple Supima cotton fibers twice the strength of regular cotton, offering a silk-like hand feel that grows softer with every wash. Finished with a discrete antique gold embroidered emblem tab.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 4.9,
            "review_count": 42
        },
        {
            "id": "nvb-tee-cyberpunk-analog-drop",
            "title": "NVB Melodic Cyberpunk Drop-Shoulder Heavy Tee",
            "brand": "NVB Cult",
            "category": "T-Shirts",
            "subcategory": "Oversized Streetwear",
            "price": 1599.0,
            "mrp": 3199.0,
            "discount": 50,
            "stock": 30,
            "low_stock_threshold": 6,
            "sku": "NVB-TEE-CYB-004",
            "images": [
                "/static/products/nvb-tee-cyberpunk-analog-drop.jpg"
            ],
            "video_url": "",
            "tags": "cyberpunk, melodic, 260 gsm, oversized, side a track",
            "is_featured": 1,
            "is_bestseller": 0,
            "is_new": 1,
            "is_flash_sale": 0,
            "is_deal_of_day": 0,
            "specs": {
                "Fabric": "260 GSM French Terry Cotton",
                "Fit": "Wide Armhole Extended Drop Shoulder",
                "Back Graphic": "Analog Synth & Soundwave Matrix in Radiant Gold",
                "Origin": "Started in 2026 // NVB Cult"
            },
            "variants": [
                {"name": "M", "stock": 10},
                {"name": "L", "stock": 15},
                {"name": "XL", "stock": 5}
            ],
            "short_description": "260 GSM French Terry with oversized armhole cut and gold soundwave matrix back print.",
            "description": "Melding analog audio soul with futuristic streetwear silhouettes. Designed with drop-tail hems, extended shoulders, and high-impact gold graphic artwork representing the harmony between rhythm and visual aesthetics.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 5.0,
            "review_count": 19
        },

        # --- ELECTRONICS (SIDE B) ---
        {
            "id": "nvb-elec-cyberdeck-anc-earbuds",
            "title": "NVB CyberDeck ANC Studio Earbuds (Black & Gold Edition)",
            "brand": "NVB Cult",
            "category": "Electronics",
            "subcategory": "Earbuds & Audio",
            "price": 2999.0,
            "mrp": 5999.0,
            "discount": 50,
            "stock": 40,
            "low_stock_threshold": 10,
            "sku": "NVB-AUD-ANC-01",
            "images": [
                "/static/products/nvb-elec-cyberdeck-anc-earbuds.jpg"
            ],
            "video_url": "",
            "tags": "anc, earbuds, bluetooth 5.3, studio audio, gold edition, analog warmth",
            "is_featured": 1,
            "is_bestseller": 1,
            "is_new": 1,
            "is_flash_sale": 1,
            "is_deal_of_day": 1,
            "specs": {
                "Drivers": "12mm Graphene Dynamic Drivers with Analog Acoustic Chamber",
                "Active Noise Cancellation": "Hybrid 42dB ANC + Ambient Transparency Mode",
                "Battery Life": "48 Hours Total Playback (8h buds + 40h charging case)",
                "Connectivity": "Bluetooth 5.3 Ultra-Low 35ms Gaming Latency",
                "Finish": "Obsidian Matte with Electroplated 24K Gold Trim",
                "Water Resistance": "IPX5 Splash & Sweat Resistance"
            },
            "variants": [
                {"name": "Standard Black & Gold", "stock": 40}
            ],
            "short_description": "Hybrid 42dB ANC, 12mm graphene drivers tuned for analog sound warmth, and 48hr playback.",
            "description": "Engineered for music producers, creators, and audiophiles. Features customized 12mm graphene diaphragms that deliver deep melodic sub-bass, velvety mids, and crisp high frequencies. Housed in an aerospace-grade matte obsidian case with metallic gold hinges.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 4.9,
            "review_count": 56
        },
        {
            "id": "nvb-elec-magfast-65w-gan",
            "title": "NVB MagFast 65W GaN Turbo Multi-Port Fast Charger",
            "brand": "NVB Cult",
            "category": "Electronics",
            "subcategory": "Fast Chargers",
            "price": 1799.0,
            "mrp": 3499.0,
            "discount": 49,
            "stock": 50,
            "low_stock_threshold": 12,
            "sku": "NVB-PWR-GAN-65",
            "images": [
                "/static/products/nvb-elec-magfast-65w-gan.jpg"
            ],
            "video_url": "",
            "tags": "gan charger, 65w, type-c, fast charging, macbook, iphone",
            "is_featured": 1,
            "is_bestseller": 1,
            "is_new": 0,
            "is_flash_sale": 0,
            "is_deal_of_day": 0,
            "specs": {
                "Technology": "Gallium Nitride (GaN III) High-Efficiency Architecture",
                "Output Power": "65W Max Fast Charge (charges MacBook Pro to 50% in 30 mins)",
                "Ports": "2x USB-C Power Delivery 3.0 + 1x USB-A Quick Charge 4.0",
                "Safety": "Active Temperature Monitoring with Over-Voltage Shield",
                "Size": "40% smaller than standard 65W laptop bricks"
            },
            "variants": [
                {"name": "65W GaN Block", "stock": 50}
            ],
            "short_description": "GaN III 65W ultra-compact brick: power your laptop, phone & creator gear simultaneously.",
            "description": "Next-generation GaN III charging power condensed into a pocketable chassis. Delivers blazing-fast 65W Power Delivery to charge your laptop, creator cameras, tablets, and phones simultaneously with dynamic power distribution.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 5.0,
            "review_count": 31
        },
        {
            "id": "nvb-elec-creator-soundtrack-mic",
            "title": "NVB Creator SoundTrack XLR/USB Studio Podcast Mic",
            "brand": "NVB Cult",
            "category": "Electronics",
            "subcategory": "Creator Mics",
            "price": 3499.0,
            "mrp": 6999.0,
            "discount": 50,
            "stock": 25,
            "low_stock_threshold": 5,
            "sku": "NVB-MIC-ST-01",
            "images": [
                "/static/products/nvb-elec-creator-soundtrack-mic.jpg"
            ],
            "video_url": "",
            "tags": "studio mic, podcasting, xlr, usb-c, creator gear, analog warmth",
            "is_featured": 0,
            "is_bestseller": 0,
            "is_new": 1,
            "is_flash_sale": 0,
            "is_deal_of_day": 0,
            "specs": {
                "Capsule": "Cardioid Dynamic Broadcast Capsule",
                "Audio Quality": "24-bit / 96kHz Studio-Grade A/D Converter",
                "Outputs": "Dual USB-C (Plug-and-Play) & Balanced XLR",
                "Monitoring": "Zero-Latency 3.5mm Headphone Jack with Volume Dial",
                "Body": "Heavy All-Metal Zinc-Alloy Chassis with Built-in Pop Filter"
            },
            "variants": [
                {"name": "Studio Edition", "stock": 25}
            ],
            "short_description": "Dual USB-C & XLR dynamic broadcast mic: broadcast studio clarity with rich analog warmth.",
            "description": "Engineered for streamers, vocalists, and creators. The custom cardioid dynamic capsule rejects background room noise while capturing the deep resonance of your voice. Features integrated gain control and touch-sensitive tap-to-mute.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 4.9,
            "review_count": 18
        },
        {
            "id": "nvb-elec-chronosync-amoled-watch",
            "title": "NVB ChronoSync AMOLED Cyberpunk Smartwatch",
            "brand": "NVB Cult",
            "category": "Electronics",
            "subcategory": "Smartwatches",
            "price": 3999.0,
            "mrp": 7999.0,
            "discount": 50,
            "stock": 30,
            "low_stock_threshold": 6,
            "sku": "NVB-WCH-CHRONO-01",
            "images": [
                "/static/products/nvb-elec-chronosync-amoled-watch.jpg"
            ],
            "video_url": "",
            "tags": "smartwatch, amoled, bluetooth calling, fitness, black gold, titanium",
            "is_featured": 1,
            "is_bestseller": 1,
            "is_new": 1,
            "is_flash_sale": 0,
            "is_deal_of_day": 0,
            "specs": {
                "Display": "1.43\" Ultra-Retina HD AMOLED (1000 nits peak brightness)",
                "Frame": "Titanium Alloy Unibody with Ceramic Back",
                "Health Sensors": "Continuous SpO2, Heart Rate, Stress & Sleep Tracking",
                "Calling": "Crystal-Clear Bluetooth 5.3 Calling with Noise-Filter Mic",
                "Battery": "14 Days Typical Use, Fast Magnetic Charging"
            },
            "variants": [
                {"name": "Obsidian Gold Titanium", "stock": 30}
            ],
            "short_description": "1.43\" Ultra-Retina AMOLED, titanium alloy frame, Bluetooth calling, and 14-day battery life.",
            "description": "Tactile luxury on your wrist. Featuring custom NVB Cult watch faces with analog chronometer dials and digital telemetry. The titanium alloy bezel and sapphire-coated glass withstand rigorous daily wear while looking impeccable.",
            "seller_name": "NVB Cult Official",
            "seller_id": "seller-nvb",
            "status": "Published",
            "rating": 5.0,
            "review_count": 27
        }
    ]

    for p in products:
        c.execute('''
        INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 50, 0, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p["id"], p["title"], p["brand"], p["category"], p["subcategory"],
            p["price"], p["mrp"], p["discount"], p["rating"], p["review_count"],
            p["stock"], p["low_stock_threshold"], p["sku"], json.dumps(p["images"]),
            p["video_url"], p["tags"], p["is_featured"], p["is_bestseller"], p["is_new"],
            p["is_flash_sale"], p["is_deal_of_day"],
            json.dumps(p["specs"]), json.dumps(p["variants"]),
            p["description"], p["short_description"],
            p["seller_name"], p["seller_id"], p["status"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        print(f"Added product: {p['title']}")

    conn.commit()
    conn.close()
    print("Catalog seeded successfully with 8 authentic NVB Cult products!")

if __name__ == "__main__":
    seed_nvb_cult()
