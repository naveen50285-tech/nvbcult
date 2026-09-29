import sqlite3
import json
import hashlib
from datetime import datetime

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def reset_db():
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    print("Clearing old products, cart, wishlist...")
    c.execute("DELETE FROM products")
    c.execute("DELETE FROM cart_items")
    c.execute("DELETE FROM wishlist_items")
    c.execute("DELETE FROM categories")
    
    # Create or update admin_users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # Insert default admin user if not exists
    admin_pw_hash = hash_pw("admin123")
    c.execute("INSERT OR REPLACE INTO admin_users VALUES (?, ?, ?, ?, ?, ?)", (
        "admin-1", "admin", admin_pw_hash, "owner", "Next Vision Owner", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    # 2 Sole Categories: Electronics & T-Shirts
    categories = [
        (
            "electronics",
            "Electronics",
            "lucide:laptop",
            "Cutting-edge wireless audio, smart wearables, fast chargers and premium tech gadgets engineered by Next Vision Brand.",
            json.dumps(["Smart Audio", "Smartwatches", "Power & Charging", "Gaming Gear", "Smart Gadgets"])
        ),
        (
            "t-shirts",
            "T-Shirts",
            "lucide:shirt",
            "Signature heavyweight cotton, oversized streetwear, cyberpunk graphics, and luxury plain everyday tees.",
            json.dumps(["Oversized Tees", "Graphic Tees", "Plain Luxury Tees", "Polo T-Shirts", "Gym & Active Tees"])
        )
    ]
    c.executemany("INSERT INTO categories VALUES (?, ?, ?, ?, ?)", categories)
    print(f"Inserted {len(categories)} categories.")
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    products = [
        # ==================== ELECTRONICS ====================
        (
            "nvb-elec-earbuds-pro",
            "NVB Sonic Pro ANC Wireless Earbuds with Spatial Audio",
            "Next Vision Brand",
            "Electronics",
            "Smart Audio",
            2999.0,
            5999.0,
            50,
            4.9,
            384,
            65,
            10,
            "NVB-AUD-001",
            json.dumps([
                "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1572536147248-ac59a8abfa4b?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "wireless earbuds, anc, bluetooth 5.4, spatial audio, next vision",
            1, 1, 1, 1, 1, 50, 18,
            json.dumps({
                "Noise Cancellation": "Active Hybrid ANC up to 42dB",
                "Battery Life": "40 Hours with USB-C Charging Case",
                "Connectivity": "Bluetooth 5.4 Low Latency (38ms)",
                "Water Resistance": "IPX5 Sweat & Splash Proof",
                "Drivers": "11mm Titanium-Coated Dynamic Drivers"
            }),
            json.dumps([
                {"name": "Color", "options": ["Matte Black", "Arctic White", "Cyber Blue"]}
            ]),
            "Experience studio-grade acoustic clarity with the NVB Sonic Pro. Featuring hybrid 42dB active noise cancellation, quad-mic ENC for crystal calls, and an ergonomic ultra-lightweight design tailored for all-day comfort.",
            "42dB Hybrid ANC, 40H battery life, Bluetooth 5.4 & spatial surround sound.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-smartwatch-ultra",
            "NVB Pulse Ultra 1.96\" AMOLED Smartwatch with BT Calling",
            "Next Vision Brand",
            "Electronics",
            "Smartwatches",
            3499.0,
            6999.0,
            50,
            4.8,
            248,
            42,
            8,
            "NVB-WCH-002",
            json.dumps([
                "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "smartwatch, amoled, bluetooth calling, fitness tracker, next vision",
            1, 1, 1, 0, 1, 50, 12,
            json.dumps({
                "Display": "1.96-inch HD AMOLED 410x502 (800 Nits)",
                "Calling": "High-Fidelity Bluetooth Calling & Dial Pad",
                "Battery": "Up to 10 Days typical use, 30 days standby",
                "Health Monitoring": "24/7 SpO2, Heart Rate, Stress, Sleep Tracking",
                "Sports Modes": "120+ Sports Modes with GPS route tracking via App"
            }),
            json.dumps([
                {"name": "Strap", "options": ["Obsidian Black", "Titanium Gray", "Ocean Green"]}
            ]),
            "Engineered with a stunning aerospace-grade zinc alloy chassis and a curved 1.96-inch AMOLED display with Always-On capability. Make calls directly from your wrist and monitor vital wellness metrics in real time.",
            "1.96\" AMOLED Always-On Display, Bluetooth calling, 10-day battery & IP68 waterproof.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-powerbank-titan",
            "NVB Titan 20000mAh 65W GaN Fast Charge Power Bank",
            "Next Vision Brand",
            "Electronics",
            "Power & Charging",
            2499.0,
            4499.0,
            44,
            4.9,
            195,
            80,
            15,
            "NVB-PWR-003",
            json.dumps([
                "https://images.unsplash.com/photo-1609081219090-a6d8173087ec?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "power bank, 65w, gan fast charging, 20000mah, laptop charging",
            1, 0, 1, 1, 0, 50, 22,
            json.dumps({
                "Capacity": "20,000mAh (74Wh Airline Approved)",
                "Max Output": "65W PD 3.0 / PPS (Charges MacBooks & Laptops)",
                "Ports": "2x USB-C (In/Out 65W) + 1x USB-A (22.5W QC)",
                "Display": "Real-time Smart LED Battery & Wattage Display",
                "Safety": "10-Layer Smart Multi-Protection Circuit"
            }),
            json.dumps([
                {"name": "Color", "options": ["Matte Black", "Space Gray"]}
            ]),
            "Charge your laptop, tablet, and smartphone simultaneously with 65W Power Delivery. Built with advanced Gallium Nitride (GaN) components to keep footprint compact and temperatures low.",
            "65W High-Power PD Output, 20000mAh, smart digital screen, charges laptops & phones.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-headphones-studio",
            "NVB Studio Pro ANC Wireless Over-Ear Headphones",
            "Next Vision Brand",
            "Electronics",
            "Smart Audio",
            4999.0,
            8999.0,
            44,
            4.9,
            160,
            35,
            5,
            "NVB-HDP-004",
            json.dumps([
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "headphones, anc, over ear, hi-res audio, next vision",
            1, 1, 0, 0, 0, 50, 9,
            json.dumps({
                "Driver Size": "40mm Bio-Cellulose Custom Dynamic Drivers",
                "Noise Cancellation": "Deep 45dB Active Noise Cancellation",
                "Playtime": "60 Hours with ANC Off, 45 Hours with ANC On",
                "Audio Codecs": "LDAC, AAC, SBC (Hi-Res Audio Certified)",
                "Comfort": "Memory Foam Protein Leather Ear Cushions"
            }),
            json.dumps([
                {"name": "Color", "options": ["Midnight Black", "Silver Frost", "Champagne Gold"]}
            ]),
            "Immerse yourself in rich, unadulterated sound with the NVB Studio Pro Over-Ear Headphones. Features 45dB active noise isolation, Hi-Res wireless audio with LDAC, and up to 60 hours of continuous playtime.",
            "Hi-Res Wireless Audio, 45dB hybrid ANC, 60h battery & memory foam ear cups.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-keyboard-mech",
            "NVB MechStrike Wireless RGB Mechanical Gaming Keyboard",
            "Next Vision Brand",
            "Electronics",
            "Gaming Gear",
            3899.0,
            6499.0,
            40,
            4.8,
            112,
            50,
            10,
            "NVB-KBD-005",
            json.dumps([
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "mechanical keyboard, rgb, wireless, hot swappable, gaming, next vision",
            0, 0, 1, 0, 0, 50, 14,
            json.dumps({
                "Switch Type": "Pre-Lubed Hot-Swappable Red Linear Switches",
                "Connectivity": "Tri-Mode (2.4GHz Wireless, Bluetooth 5.2, USB-C)",
                "Keycaps": "Double-Shot PBT Cherry Profile Keycaps",
                "Battery": "4000mAh Rechargeable Lithium Battery (200h without RGB)",
                "Lighting": "16.8M Color Per-Key RGB with 20 Backlight Modes"
            }),
            json.dumps([
                {"name": "Switches", "options": ["Red Linear", "Brown Tactile"]}
            ]),
            "Engineered for gamers and pro typists alike. Tri-mode wireless connectivity, hot-swappable switch sockets, premium sound dampening foam layers, and durable double-shot PBT keycaps.",
            "Tri-Mode wireless, hot-swappable mechanical switches, per-key RGB & 4000mAh battery.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-charger-gan65w",
            "NVB Volt 65W GaN Multi-Port Ultra Fast Wall Charger",
            "Next Vision Brand",
            "Electronics",
            "Power & Charging",
            1499.0,
            2999.0,
            50,
            4.8,
            210,
            120,
            20,
            "NVB-CHG-006",
            json.dumps([
                "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "charger, gan, 65w fast charger, type c, next vision",
            0, 1, 0, 0, 0, 50, 26,
            json.dumps({
                "Power Output": "65W Max Power Delivery 3.0 / PPS",
                "Ports": "2x USB Type-C + 1x USB Type-A",
                "Technology": "GaN III (Gallium Nitride) Semiconductor",
                "Compatibility": "Laptops, iPhones, Galaxy, Pixel, iPads, Nintendo Switch",
                "Plug Type": "India 2-Pin Plug with foldable travel design"
            }),
            json.dumps([
                {"name": "Color", "options": ["Midnight Black", "Pure White"]}
            ]),
            "Power up to three devices at once with cutting-edge GaN III architecture that is 50% smaller and cooler than standard chargers. Delivers blazing fast 65W PD power for laptops and phones.",
            "GaN III 65W triple-port charger, compact pocket size, powers laptops & smartphones.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-soundbar-wave",
            "NVB SoundWave 60W Bluetooth Soundbar with Subwoofer",
            "Next Vision Brand",
            "Electronics",
            "Smart Audio",
            4299.0,
            7999.0,
            46,
            4.7,
            88,
            30,
            5,
            "NVB-SND-007",
            json.dumps([
                "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "soundbar, bluetooth speaker, home theater, 3d surround, next vision",
            0, 0, 1, 0, 0, 50, 8,
            json.dumps({
                "Audio Output": "60W RMS Peak Power with DSP EQ Modes",
                "Drivers": "4x Neodymium Full-Range Drivers + Dual Bass Reflex Tubes",
                "Connectivity": "Bluetooth 5.3, Optical, HDMI (ARC), AUX, USB",
                "Design": "Slim Metallic Mesh Wall-Mountable Aesthetic"
            }),
            json.dumps([
                {"name": "Finish", "options": ["Brushed Black", "Space Slate"]}
            ]),
            "Upgrade your home entertainment with punchy bass and crystal dialogues. Features specialized Movie, Music, and News equalizer presets with multiple connection options including HDMI ARC.",
            "60W cinematic soundbar, HDMI ARC, Optical, Bluetooth 5.3 & punchy bass.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-elec-camera-action4k",
            "NVB Horizon 4K Ultra HD Dual-Screen Waterproof Action Cam",
            "Next Vision Brand",
            "Electronics",
            "Smart Gadgets",
            6499.0,
            11999.0,
            46,
            4.8,
            76,
            24,
            4,
            "NVB-CAM-008",
            json.dumps([
                "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "action camera, 4k 60fps, waterproof, vlogging, next vision",
            0, 0, 1, 0, 0, 50, 6,
            json.dumps({
                "Video Resolution": "4K at 60FPS / 1080P at 120FPS Slow-Mo",
                "Stabilization": "6-Axis Smart EIS Gyro Anti-Shake",
                "Waterproof": "Up to 30 Meters with included rugged casing",
                "Screens": "Dual Screen (2.0\" Touch Rear + 1.4\" Selfie Front Screen)",
                "Battery": "2x 1350mAh Batteries included (Up to 180 min recording)"
            }),
            json.dumps([
                {"name": "Bundle", "options": ["Standard Kit", "Vlogger Accessory Kit (+₹999)"]}
            ]),
            "Capture thrilling travel adventures, bike rides, and underwater footage in buttery smooth 4K 60FPS. Dual color screens make vlogging and framing effortless anywhere in the world.",
            "4K 60FPS dual-screen action camera with 6-axis gyro stabilization & 30m waterproof casing.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),

        # ==================== T-SHIRTS ====================
        (
            "nvb-tee-oversized-heavy",
            "NVB Heavyweight 260 GSM Oversized Streetwear T-Shirt",
            "Next Vision Brand",
            "T-Shirts",
            "Oversized Tees",
            1199.0,
            1999.0,
            40,
            4.9,
            312,
            90,
            15,
            "NVB-TEE-101",
            json.dumps([
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "tshirt, oversized, streetwear, 260 gsm, heavy cotton, next vision",
            1, 1, 1, 1, 1, 50, 24,
            json.dumps({
                "Fabric": "100% Super-Combed French Terry Cotton (260 GSM)",
                "Fit": "Signature Boxy Oversized Fit with Drop Shoulders",
                "Neckline": "Thick 1.25\" Ribbed Lycra Crew Neck (Anti-Sag)",
                "Wash Care": "Bio-Washed & Pre-Shrunk for Zero Color Fade"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Washed Charcoal", "Off-White Cream", "Olive Sage", "Pitch Black"]}
            ]),
            "The pinnacle of contemporary streetwear silhouette. Constructed from ultra-heavyweight 260 GSM French Terry cotton that drapes effortlessly. Designed with an intentional boxy drop-shoulder cut.",
            "260 GSM heavyweight combed cotton, drop shoulder boxy streetwear fit.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-graphic-cyberpunk",
            "NVB Cyber Vision High-Density Graphic Printed T-Shirt",
            "Next Vision Brand",
            "T-Shirts",
            "Graphic Tees",
            999.0,
            1699.0,
            41,
            4.8,
            260,
            75,
            12,
            "NVB-TEE-102",
            json.dumps([
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "graphic tee, cyberpunk, screen print, next vision brand, casual t-shirt",
            1, 1, 1, 0, 1, 50, 19,
            json.dumps({
                "Fabric": "100% Bio-Washed Ring-Spun Cotton (210 GSM)",
                "Print Technique": "High-Density Plastisol Screen Print (No Cracking)",
                "Fit": "Relaxed Regular Fit with Clean Hemming",
                "Feel": "Silky Smooth Hand-Feel, Breathable all-season comfort"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Jet Black", "Electric Slate"]}
            ]),
            "Bold futurist typography and cybernetic artwork make this tee an instant wardrobe centerpiece. Crafted with high-density screen printing on soft, breathable 210 GSM combed cotton.",
            "Futuristic cyberpunk high-density graphic print, 210 GSM soft bio-washed cotton.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-luxury-supima",
            "NVB Signature Supima Luxury Plain Minimalist Tee",
            "Next Vision Brand",
            "T-Shirts",
            "Plain Luxury Tees",
            899.0,
            1499.0,
            40,
            4.9,
            184,
            100,
            20,
            "NVB-TEE-103",
            json.dumps([
                "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "plain t-shirt, supima cotton, luxury tee, everyday basics, next vision",
            1, 0, 1, 1, 0, 50, 14,
            json.dumps({
                "Material": "100% Extra-Long Staple American Supima Cotton (190 GSM)",
                "Texture": "Lustrous Silk-Like Handfeel with High Tear Resistance",
                "Fit": "Tailored Modern Classic Fit",
                "Details": "Discreet Embroidered NVB Monogram at Left Chest"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Chalk White", "Midnight Navy", "Carbon Black", "Forest Pine"]}
            ]),
            "The quintessential daily luxury tee. Woven from 100% extra-long staple Supima cotton, delivering extraordinary softness, natural luster, and color retention through dozens of wash cycles.",
            "100% Extra-Long Staple Supima Cotton, tailored silhouette with NVB chest embroidery.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-japan-art",
            "NVB Ukiyo-e Wave Vintage Minimalist Japanese T-Shirt",
            "Next Vision Brand",
            "T-Shirts",
            "Graphic Tees",
            1099.0,
            1799.0,
            39,
            4.8,
            140,
            60,
            10,
            "NVB-TEE-104",
            json.dumps([
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "japanese wave, vintage art tee, streetwear graphic, next vision",
            0, 1, 1, 0, 0, 50, 16,
            json.dumps({
                "Fabric": "100% Pre-Shrunk Ringspun Cotton (220 GSM)",
                "Artwork": "Authentic Japanese Woodblock Inspired Tidal Wave & Kanji",
                "Fit": "Slightly Relaxed Streetwear Cut",
                "Stitching": "Twin-Needle Sleeve and Bottom Hem"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Sage Moss", "Oatmeal Heather", "Deep Indigo"]}
            ]),
            "Inspired by classical Japanese ukiyo-e woodblock art blended with futuristic street fashion. Printed using eco-friendly soft-feel inks that soften with every wear.",
            "Japanese wave vintage artwork, 220 GSM pre-shrunk cotton & relaxed cut.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-polo-mercerized",
            "NVB Classic Mercerized Pique Cotton Polo T-Shirt",
            "Next Vision Brand",
            "T-Shirts",
            "Polo T-Shirts",
            1399.0,
            2299.0,
            39,
            4.8,
            96,
            55,
            8,
            "NVB-TEE-105",
            json.dumps([
                "https://images.unsplash.com/photo-1625910513413-568393e155c8?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "polo t-shirt, pique cotton, mercerized, smart casual, next vision",
            0, 0, 1, 0, 0, 50, 11,
            json.dumps({
                "Fabric": "100% Double-Mercerized Combed Pique Cotton (230 GSM)",
                "Collar": "Anti-Curl Structured Ribbed Collar",
                "Buttons": "Genuine Mother-of-Pearl Engraved Buttons",
                "Fit": "Contemporary Slim Fit with Side Vents"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Royal Burgundy", "Classic Navy", "Emerald Green", "Jet Black"]}
            ]),
            "Elevate smart-casual style. Double-mercerized pique cotton provides a smooth, subtle sheen, exceptional drape, and anti-wrinkle resilience from business meetings to weekend dinners.",
            "Double-mercerized pique cotton polo, anti-curl collar & mother-of-pearl buttons.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-gym-dryfit",
            "NVB Motion Pro Dry-Fit 4-Way Stretch Athletic Gym Tee",
            "Next Vision Brand",
            "T-Shirts",
            "Gym & Active Tees",
            799.0,
            1299.0,
            38,
            4.9,
            224,
            85,
            15,
            "NVB-TEE-106",
            json.dumps([
                "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "gym tee, dry fit, activewear, moisture wicking, workout t-shirt, next vision",
            0, 1, 0, 0, 0, 50, 30,
            json.dumps({
                "Fabric Blend": "88% Polyester Microfiber + 12% Spandex (160 GSM)",
                "Tech": "Quick-Dry Moisture Management & Silver Anti-Bacterial Ion Tech",
                "Ventilation": "Laser-Cut Breathable Underarm Ventilation Zones",
                "Visibility": "Reflective NVB Logos for Night Running Safety"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Athletic Slate", "Stealth Black", "Neon Lime", "Crimson Red"]}
            ]),
            "Designed for high-intensity training, marathon runs, and gym sessions. Engineered with 4-way stretch microfiber that pulls perspiration away from the skin and evaporates instantly.",
            "4-Way stretch microfiber with quick-dry moisture wicking & anti-odor tech.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-retro-neon",
            "NVB Retro Neon Synthwave Boxy Graphic Tee",
            "Next Vision Brand",
            "T-Shirts",
            "Graphic Tees",
            1049.0,
            1799.0,
            42,
            4.7,
            135,
            48,
            8,
            "NVB-TEE-107",
            json.dumps([
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "synthwave, retro neon, vintage wash, graphic t-shirt, next vision",
            0, 0, 1, 0, 0, 50, 15,
            json.dumps({
                "Fabric": "100% Combed Cotton Vintage Acid-Washed (230 GSM)",
                "Design": "80s Neon Sunset Grid & Palm Silhouette Graphic",
                "Fit": "Relaxed Boxy Fit with Drop Shoulder",
                "Neck": "Ribbed Spandex Neckband"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Midnight Purple", "Washed Charcoal"]}
            ]),
            "Channelling vibrant 80s arcade aesthetics with modern streetwear cuts. Mineral acid-washed for a naturally worn-in texture with vibrant neon screen printing that pops.",
            "Vintage acid-wash 230 GSM cotton with 80s synthwave neon artwork.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        ),
        (
            "nvb-tee-puff-vision",
            "NVB Minimalist Typography \"Next Vision 2026\" Heavy Tee",
            "Next Vision Brand",
            "T-Shirts",
            "Oversized Tees",
            1149.0,
            1899.0,
            39,
            4.9,
            178,
            64,
            10,
            "NVB-TEE-108",
            json.dumps([
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
            ]),
            "",
            "puff print, minimalist typography, oversized t-shirt, next vision brand",
            1, 0, 1, 0, 0, 50, 21,
            json.dumps({
                "Fabric": "100% Luxury Combed Cotton (250 GSM)",
                "Printing": "3D Tactile Puff Print Typography on Chest & Back",
                "Fit": "Loose Oversized Silhouette with Wide Sleeves",
                "Colorway": "Sand Beige & Off-White Monochromatic Palette"
            }),
            json.dumps([
                {"name": "Size", "options": ["S", "M", "L", "XL", "XXL"]},
                {"name": "Color", "options": ["Sand Beige", "Chalk White", "Deep Coal"]}
            ]),
            "Subtle yet commanding. Premium 3D tactile puff printing with clean typography detailing the Next Vision Brand manifesto across the back shoulders. Cut in a generous relaxed drape.",
            "3D tactile puff print typography, 250 GSM luxury combed cotton & oversized silhouette.",
            "Next Vision Brand Official Store",
            "seller-1",
            "Published",
            now_str
        )
    ]
    
    insert_sql = '''
    INSERT INTO products (
        id, title, brand, category, subcategory, price, mrp, discount,
        rating, review_count, stock, low_stock_threshold, sku, images,
        video_url, tags, is_featured, is_bestseller, is_new, is_flash_sale,
        is_deal_of_day, flash_stock_limit, flash_sold, specs, variants,
        description, short_description, seller_name, seller_id, status, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    c.executemany(insert_sql, products)
    conn.commit()
    
    c.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
    counts = c.fetchall()
    print("New product counts by category:", counts)
    
    conn.close()
    print("Database successfully reset with ONLY Electronics & T-Shirts!")

if __name__ == "__main__":
    reset_db()
