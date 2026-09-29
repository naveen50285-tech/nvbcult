import json
from database import get_db

conn = get_db()
c = conn.cursor()
c.execute('DELETE FROM products')
c.execute('DELETE FROM reviews')
c.execute('DELETE FROM orders')
c.execute('DELETE FROM notifications')

def add_p(pid, title, brand, cat, subcat, price, mrp, rating, rev_count, stock, sku, img, tags, specs, feat=0, best=0, new=0, flash=0, deal=0, f_lim=50, f_sold=0, variants=None):
    disc = int(round(((mrp - price) / mrp) * 100)) if mrp > price else 0
    vars_json = json.dumps(variants or [{'name': 'Color', 'options': ['Space Black', 'Titanium Gray']}])
    c.execute('''
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 10, ?, ?, '', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NVB Direct Official', 'seller-1', 'Published', '2026-09-10T10:00:00')
    ''', (
        pid, title, brand, cat, subcat, price, mrp, disc, rating, rev_count, stock, sku,
        json.dumps([img, img]), tags, feat, best, new, flash, deal, f_lim, f_sold,
        json.dumps(specs), vars_json,
        f'Experience peak engineering with the {title}. Designed for discerning customers with uncompromising performance and luxury finish.',
        f'Next Vision flagship {brand} - Premium craftsmanship, verified warranty and authentic experience.',
    ))

# 1. Electronics
add_p('nvb-vision-phone-pro', 'NVB Vision Phone Pro 5G (Titanium Gray, 256GB)', 'Next Vision', 'Electronics', 'Smartphones', 64999.0, 79999.0, 4.9, 1420, 42, 'NVB-PHN-PRO-256', 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800&q=80', '5g, flagship, titanium, oled, 120hz, ai camera, phone, smartphone, mobile', {'Processor': 'Snapdragon 8 Gen 3 AI', 'RAM': '12GB LPDDR5X', 'Storage': '256GB UFS 4.0', 'Display': '6.8 QHD+ 144Hz LTPO', 'Camera': '200MP OIS Quad + 50MP Zoom', 'Battery': '5400 mAh 100W HyperCharge'}, feat=1, best=1, new=1, flash=1, deal=1, f_lim=50, f_sold=38, variants=[{'name': 'Color', 'options': ['Titanium Gray', 'Cyber Blue', 'Obsidian Black']}, {'name': 'Storage', 'options': ['256GB', '512GB', '1TB']}])

add_p('nvb-cyberbook-ai-16', 'NVB CyberBook AI Ultra 16-inch Laptop (Intel Ultra 9, 32GB RAM, 1TB SSD)', 'Next Vision', 'Electronics', 'Laptops', 124999.0, 149999.0, 4.8, 860, 18, 'NVB-LPT-CYBER-16', 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80', 'laptop, programming, coding, ultrabook, rtx 4070, intel ultra 9, oled, developer', {'Processor': 'Intel Core Ultra 9 185H', 'RAM': '32GB LPDDR5X', 'Storage': '1TB NVMe Gen4 SSD', 'GPU': 'NVIDIA RTX 4070 8GB', 'Display': '16 3.2K OLED 120Hz', 'Weight': '1.68 kg'}, feat=1, best=1, new=1, flash=0, deal=0, f_lim=30, f_sold=12, variants=[{'name': 'Color', 'options': ['Space Slate', 'Starlight Silver']}, {'name': 'RAM', 'options': ['32GB', '64GB']}])

add_p('sony-wh1000xm5-headphones', 'Sony WH-1000XM5 Wireless Noise Cancelling Over-Ear Headphones', 'Sony', 'Electronics', 'Headphones', 26990.0, 34990.0, 4.9, 3120, 65, 'SNY-WH-1000XM5', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80', 'headphones, noise cancelling, anc, sony, bluetooth, audio, hi-res, wireless', {'Driver': '30mm Carbon Fiber', 'Noise Cancellation': 'Dual HD V1/QN1 Processors', 'Battery': '30 Hours', 'Codec': 'LDAC, Hi-Res Wireless'}, feat=1, best=1, new=0, flash=1, deal=1, f_lim=80, f_sold=54, variants=[{'name': 'Color', 'options': ['Black', 'Silver', 'Midnight Blue']}])

add_p('playstation-5-slim-console', 'Sony PlayStation 5 Slim Gaming Console (1TB SSD Edition)', 'Sony', 'Electronics', 'Gaming Consoles', 49990.0, 54990.0, 4.9, 4120, 35, 'SNY-PS5-SLIM-1TB', 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&q=80', 'ps5, gaming, console, 4k 120fps, playstation, sony', {'Storage': '1TB High Speed NVMe', 'Resolution': 'Up to 4K 120Hz & 8K', 'Haptics': 'DualSense Wireless Controller'}, feat=1, best=1, new=1, flash=1, deal=1, f_lim=60, f_sold=45)

add_p('nvb-pulse-watch-ultra', 'NVB Pulse Ultra Smart Watch with AMOLED Display & ECG Monitor', 'Next Vision', 'Electronics', 'Smart Watches', 4999.0, 9999.0, 4.7, 940, 80, 'NVB-WTC-PULSE-01', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80', 'smart watch, amoled, bluetooth calling, fitness, ecg, heart rate, wearable, under 20000', {'Display': '1.96 Curved AMOLED Always-On', 'Sensors': 'ECG, SpO2, Heart Rate', 'Waterproof': 'IP68 & 5ATM', 'Battery': 'Up to 12 Days'}, feat=0, best=1, new=1, flash=1, deal=0, f_lim=100, f_sold=82, variants=[{'name': 'Color', 'options': ['Space Black', 'Alpine Silver', 'Ocean Blue']}])

# 2. Fashion
add_p('nvb-signature-linen-shirt', 'NVB Signature 100% Pure French Linen Casual Shirt for Men', 'Next Vision Fashion', 'Fashion', 'Shirts', 1899.0, 3499.0, 4.6, 680, 110, 'NVB-FSH-LIN-01', 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&q=80', 'fashion, shirt, linen, breathable, formal, casual, summer, men', {'Material': '100% Certified French Flax Linen', 'Fit': 'Tailored Relaxed Fit', 'Care': 'Machine Wash Cold'}, feat=1, best=1, new=1, flash=0, deal=1, f_lim=150, f_sold=90, variants=[{'name': 'Color', 'options': ['Powder Blue', 'Crisp White', 'Sage Green', 'Charcoal']}, {'name': 'Size', 'options': ['S', 'M', 'L', 'XL', 'XXL']}])

add_p('nvb-aero-knit-running-shoes', 'NVB AeroKnit Pro Cushion High-Performance Sneakers', 'Next Vision Active', 'Fashion', 'Shoes', 2499.0, 4999.0, 4.8, 1250, 95, 'NVB-SH-AERO-01', 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80', 'shoes, sneakers, running, college, black shoes, gym, lightweight, footwear', {'Sole': 'Nitrogen Rebound Foam', 'Upper': 'AeroKnit Seamless Mesh', 'Insole': 'Memory Cushion Arch'}, feat=1, best=1, new=0, flash=1, deal=1, f_lim=120, f_sold=88, variants=[{'name': 'Color', 'options': ['Stealth Black', 'Cyber Red', 'Ghost White']}, {'name': 'Size', 'options': ['UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11']}])

add_p('nvb-kanchipuram-silk-saree', 'NVB Royal Kanchipuram Handwoven Pure Silk Saree with Zari', 'Heritage Vision', 'Fashion', 'Sarees', 8999.0, 15999.0, 4.9, 430, 30, 'HRT-SAR-KNC-01', 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&q=80', 'saree, ethnic, silk, wedding, festival, zari, festive, women', {'Fabric': 'Pure Mulberry Silk (Silk Mark)', 'Zari': 'Tested Gold & Silver Weave', 'Length': '6.3 Meters with Blouse'}, feat=0, best=1, new=1, flash=0, deal=0, f_lim=50, f_sold=22, variants=[{'name': 'Color', 'options': ['Royal Crimson', 'Peacock Green', 'Deep Magenta']}])

# 3. Home & Kitchen
add_p('nvb-ergopro-mesh-chair', 'NVB ErgoPro Ergonomic High-Back Mesh Office & Gaming Chair', 'Next Vision Home', 'Home & Kitchen', 'Furniture', 8999.0, 18999.0, 4.8, 1150, 40, 'NVB-HOM-CHAIR-01', 'https://images.unsplash.com/photo-1580481077195-c3a821a50609?w=800&q=80', 'office chair, ergonomics, lumbar support, desk, wfh, work from home, furniture', {'Lumbar': '3D Dynamic Tracking', 'Armrests': '4D Adjustable', 'Gas Lift': 'Class 4 BIFMA Certified', 'Max Weight': '150 kg'}, feat=1, best=1, new=0, flash=1, deal=1, f_lim=60, f_sold=41, variants=[{'name': 'Color', 'options': ['Carbon Black', 'Graphite Gray', 'Sky Blue']}])

add_p('philips-smart-airfryer-xxl', 'Philips Smart Digital Air Fryer XXL 7.2L Rapid Air', 'Philips', 'Home & Kitchen', 'Kitchen Appliances', 10999.0, 15995.0, 4.8, 2180, 35, 'PHL-AF-XXL-72', 'https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=800&q=80', 'air fryer, kitchen, healthy, philips, oil free, cooking, appliances', {'Capacity': '7.2 Liters XXL', 'Power': '2000W Rapid Air Vortex', 'Fat Reduction': 'Up to 90% Less Fat'}, feat=1, best=1, new=0, flash=0, deal=1, f_lim=50, f_sold=29, variants=[{'name': 'Color', 'options': ['Midnight Black', 'Pearl White']}])

# 4. Beauty & Personal Care
add_p('nvb-bioluminescent-vitamin-c-serum', 'NVB GlowScience 15% Vitamin C + Hyaluronic Facial Serum 30ml', 'GlowScience', 'Beauty & Personal Care', 'Skincare', 899.0, 1499.0, 4.8, 1540, 130, 'GLW-SRM-VITC-30', 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80', 'serum, vitamin c, skincare, glowing skin, hyaluronic, anti aging, beauty', {'Actives': '15% L-Ascorbic Acid + Hyaluronic', 'Skin Type': 'All Skin Types', 'Volume': '30ml'}, feat=1, best=1, new=1, flash=1, deal=1, f_lim=150, f_sold=115, variants=[{'name': 'Volume', 'options': ['30ml', '50ml']}])

# 5. Grocery
add_p('royal-basmati-rice-5kg', 'Royal Heritage Premium Aged Extra Long Grain Basmati Rice (5kg)', 'Royal Heritage', 'Grocery', 'Rice', 749.0, 999.0, 4.8, 2100, 140, 'GRC-RCE-BSM-05', 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800&q=80', 'grocery, rice, basmati, biryani, staples, food', {'Aging': 'Aged 2 Years Naturally', 'Grain': 'Extra Long Grain 24mm', 'Weight': '5kg'}, feat=0, best=1, new=0, flash=0, deal=1, f_lim=200, f_sold=130, variants=[{'name': 'Pack Size', 'options': ['5kg', '10kg']}])

# 6. Sports & Fitness
add_p('nvb-powergrip-adjustable-dumbbell', 'NVB PowerGrip Quick-Select Adjustable Dumbbell Set (2.5kg to 24kg)', 'Next Vision Fitness', 'Sports & Fitness', 'Gym Equipment', 7999.0, 14999.0, 4.9, 920, 30, 'NVB-SPT-DMB-24', 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&q=80', 'gym, dumbbell, fitness, home gym, workout, weight lifting, sports', {'Weight': '15 Settings: 2.5kg to 24kg', 'Mechanism': 'Precision Turn Dial', 'Plates': 'Silicone Coated Cast Iron'}, feat=1, best=1, new=1, flash=1, deal=1, f_lim=40, f_sold=29, variants=[{'name': 'Set', 'options': ['Single 24kg', 'Pair 2x24kg']}])

# 7. Books & Education
add_p('architecture-of-tomorrow-book', 'The Architecture of Tomorrow: Artificial Intelligence & Quantum Systems', 'Visionary Press', 'Books & Education', 'Books', 899.0, 1499.0, 4.9, 640, 85, 'BOK-ARCH-FUT-01', 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&q=80', 'book, ai, quantum, technology, computer science, hardcover, education', {'Pages': '480 Pages', 'Binding': 'Hardcover Deluxe', 'Language': 'English'}, feat=0, best=1, new=1, flash=0, deal=0, f_lim=100, f_sold=44, variants=[{'name': 'Format', 'options': ['Hardcover', 'Paperback']}])

# 8. Automotive
add_p('nvb-vision-4k-dashcam', 'NVB Vision 4K Ultra HD Dual Front & Rear Dash Cam with GPS', 'Next Vision Auto', 'Automotive', 'Car Accessories', 6499.0, 12999.0, 4.8, 810, 45, 'NVB-AUT-DSH-4K', 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=800&q=80', 'dash cam, car, 4k camera, gps, car accessories, safety, automotive', {'Resolution': '4K Front + 1080P Rear', 'Sensor': 'Sony STARVIS 2 Night Vision', 'Features': 'WiFi 5GHz & GPS'}, feat=1, best=1, new=1, flash=1, deal=1, f_lim=50, f_sold=36, variants=[{'name': 'Card Included', 'options': ['64GB', '128GB']}])

# 9. Health & Wellness
add_p('nvb-pro-deep-tissue-massage-gun', 'NVB ProPulse Cordless Deep Tissue Muscle Massage Gun with 6 Heads', 'Next Vision Health', 'Health & Wellness', 'Healthcare Accessories', 3499.0, 7999.0, 4.8, 1100, 60, 'NVB-HLT-MSG-01', 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&q=80', 'massage gun, health, pain relief, gym recovery, percussion, wellness, under 20000', {'Motor': 'QuietBrushless 3200 RPM', 'Speeds': '30 Speed Settings', 'Heads': '6 Specialized Attachments'}, feat=1, best=1, new=0, flash=1, deal=1, f_lim=70, f_sold=52, variants=[{'name': 'Color', 'options': ['Matte Black', 'Emerald Teal']}])

# 10. Appliances
add_p('bosch-front-load-washing-machine', 'Bosch Serie 6 8kg 5-Star Fully Automatic Front Loading Washing Machine', 'Bosch', 'Appliances', 'Washing Machines', 36990.0, 47990.0, 4.9, 1420, 16, 'BSH-WM-8KG-SR6', 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800&q=80', 'washing machine, front load, bosch, inverter, 8kg, appliances', {'Capacity': '8kg Front Load', 'Spin': '1400 RPM High Speed', 'Motor': 'EcoSilence Drive Frictionless'}, feat=1, best=1, new=1, flash=1, deal=0, f_lim=25, f_sold=17, variants=[{'name': 'Color', 'options': ['Silver Inox', 'White']}])

# Seed Sample Reviews
reviews = [
    ('rev-1', 'nvb-vision-phone-pro', 'Vikramaditya S.', 5, 'Unbelievable Camera and Build Quality!', 'Switching from my older phone to the NVB Vision Phone Pro is the best decision. The 200MP camera produces DSLR-level portraits, and battery easily lasts 1.5 days.', 1, 48, '2026-09-15'),
    ('rev-2', 'nvb-vision-phone-pro', 'Ananya Verma', 5, 'Titanium chassis feels ultra-premium', 'The display colors pop and 144Hz is buttery smooth. The 100W charger went from 10% to 100% in 22 minutes!', 1, 32, '2026-09-18'),
    ('rev-3', 'nvb-cyberbook-ai-16', 'Rahul Krishnan', 5, 'Best developer laptop in India for 2026', 'Compiling massive Rust and Python AI pipelines is blazing fast. The OLED display is sharp and keyboard has perfect tactile bounce.', 1, 65, '2026-09-19'),
    ('rev-4', 'sony-wh1000xm5-headphones', 'Deepak Sharma', 5, 'Pure silence in flights and metro', 'The noise cancellation is witchcraft. You put these on and the entire world mutes. Soundstage is punchy and detailed.', 1, 112, '2026-09-12'),
    ('rev-5', 'nvb-ergopro-mesh-chair', 'Meera Sen', 5, 'Saved my lower back!', 'I sit for 10 hours coding every day. The dynamic lumbar support follows every movement. Very solid build.', 1, 74, '2026-09-20')
]
for r in reviews:
    c.execute('INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', r)

# Sample Order with tracking
timeline = [
    {'status': 'ORDER PLACED', 'time': '2026-09-22 14:30', 'completed': True, 'desc': 'Order placed successfully'},
    {'status': 'CONFIRMED', 'time': '2026-09-22 14:45', 'completed': True, 'desc': 'Seller confirmed order inventory'},
    {'status': 'PACKED', 'time': '2026-09-23 09:15', 'completed': True, 'desc': 'Item packed in tamper-proof NVB packaging'},
    {'status': 'SHIPPED', 'time': '2026-09-23 18:00', 'completed': True, 'desc': 'Dispatched via BlueDart Express (AWB: BD8891024)'},
    {'status': 'OUT FOR DELIVERY', 'time': 'Expected Tomorrow', 'completed': False, 'desc': 'Courier agent will arrive between 10 AM - 1 PM'},
    {'status': 'DELIVERED', 'time': 'Pending', 'completed': False, 'desc': 'Package delivered safely'}
]
items = [
    {
        'product_id': 'nvb-vision-phone-pro',
        'title': 'NVB Vision Phone Pro 5G (Titanium Gray, 256GB)',
        'price': 64999.0,
        'variant': 'Titanium Gray / 256GB',
        'quantity': 1,
        'image': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800&q=80'
    }
]
c.execute('''
INSERT INTO orders VALUES (
    'NVB-2026-89412', 'default-user', 'Arjun Sundaram', 'arjun.s@gmail.com', '+91 98450 12345',
    '402, Highrise Silicon Residency, 100ft Road, Indiranagar, Bengaluru, Karnataka, 560038',
    'NVB Prime Express', 0.0, 'UPI (GPay)', 'Paid',
    64999.0, 2500.0, 11249.82, 62499.0, 'SHIPPED', ?, ?, '2026-09-22T14:30:00'
)''', (json.dumps(timeline), json.dumps(items)))

c.execute('''
INSERT INTO notifications VALUES (
    'notif-1', 'default-user', 'Flash Sale Live!',
    'The Grand NVB Flash Sale has started with up to 56% off on Electronics and Health Tech.',
    'sale', 0, '2026-09-24T10:00:00'
)''')

conn.commit()
conn.close()
print('All catalog products seeded successfully!')
