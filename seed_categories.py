import json
from database import get_db

def seed_meta():
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM categories')
    c.execute('DELETE FROM coupons')
    c.execute('DELETE FROM sellers')
    
    categories = [
        {
            'id': 'electronics', 'name': 'Electronics', 'icon': 'cpu',
            'description': 'Smartphones, Laptops, Audio, Gaming & Smart Devices',
            'subcategories': ['Smartphones', 'Mobile Accessories', 'Laptops', 'Tablets', 'Computers', 'Monitors', 'Keyboards', 'Mouse', 'Headphones', 'Earbuds', 'Speakers', 'Cameras', 'Smart Watches', 'Gaming', 'Gaming Consoles', 'Computer Components', 'Printers', 'Storage Devices', 'Networking', 'Chargers', 'Power Banks', 'Smart Home']
        },
        {
            'id': 'fashion', 'name': 'Fashion', 'icon': 'shopping-bag',
            'description': 'Men, Women & Kids Apparel, Footwear & Accessories',
            'subcategories': ['Mens Clothing', 'Womens Clothing', 'Kids Clothing', 'T-Shirts', 'Shirts', 'Jeans', 'Dresses', 'Sarees', 'Kurtas', 'Shoes', 'Sandals', 'Bags', 'Watches', 'Sunglasses', 'Fashion Accessories']
        },
        {
            'id': 'home-kitchen', 'name': 'Home & Kitchen', 'icon': 'home',
            'description': 'Furniture, Cookware, Lighting, Decor & Essentials',
            'subcategories': ['Furniture', 'Kitchen Appliances', 'Cookware', 'Home Decor', 'Lighting', 'Storage', 'Cleaning Products', 'Bedsheets', 'Curtains', 'Bathroom Accessories', 'Gardening', 'Home Improvement']
        },
        {
            'id': 'beauty', 'name': 'Beauty & Personal Care', 'icon': 'sparkles',
            'description': 'Skincare, Haircare, Fragrance & Grooming Luxuries',
            'subcategories': ['Skincare', 'Hair Care', 'Makeup', 'Fragrances', 'Grooming', 'Personal Care', 'Bath & Body']
        },
        {
            'id': 'grocery', 'name': 'Grocery', 'icon': 'coffee',
            'description': 'Staples, Snacks, Beverages, Spices & Gourmet Foods',
            'subcategories': ['Rice', 'Pulses', 'Flour', 'Snacks', 'Beverages', 'Spices', 'Cooking Essentials', 'Packaged Foods', 'Household Essentials']
        },
        {
            'id': 'sports-fitness', 'name': 'Sports & Fitness', 'icon': 'activity',
            'description': 'Gym Equipment, Outdoor Gear, Yoga & Activewear',
            'subcategories': ['Sports Equipment', 'Gym Equipment', 'Fitness Accessories', 'Outdoor Sports', 'Cycling', 'Running', 'Yoga']
        },
        {
            'id': 'books-education', 'name': 'Books & Education', 'icon': 'book-open',
            'description': 'Bestsellers, Textbooks, School Supplies & STEM',
            'subcategories': ['Books', 'School Supplies', 'College Supplies', 'Stationery', 'Educational Products']
        },
        {
            'id': 'automotive', 'name': 'Automotive', 'icon': 'navigation',
            'description': 'Car & Bike Accessories, Electronics & Care',
            'subcategories': ['Car Accessories', 'Bike Accessories', 'Car Care', 'Bike Care', 'Tools', 'Electronics']
        },
        {
            'id': 'toys-baby', 'name': 'Toys & Baby', 'icon': 'smile',
            'description': 'Baby Essentials, Learning Toys & Action Figures',
            'subcategories': ['Toys', 'Baby Clothing', 'Baby Care', 'Educational Toys', 'Games']
        },
        {
            'id': 'health-wellness', 'name': 'Health & Wellness', 'icon': 'heart',
            'description': 'Vitamins, Healthcare Monitoring & Wellness Gear',
            'subcategories': ['Wellness Products', 'Fitness Products', 'Personal Care', 'Healthcare Accessories']
        },
        {
            'id': 'pet-supplies', 'name': 'Pet Supplies', 'icon': 'shield',
            'description': 'Premium Dog & Cat Nutrition, Beds & Toys',
            'subcategories': ['Dog Products', 'Cat Products', 'Pet Food', 'Pet Toys', 'Pet Accessories']
        },
        {
            'id': 'appliances', 'name': 'Appliances', 'icon': 'wind',
            'description': 'Refrigerators, Washing Machines, ACs & Microwaves',
            'subcategories': ['Refrigerators', 'Washing Machines', 'Air Conditioners', 'Fans', 'Air Coolers', 'Microwaves', 'Vacuum Cleaners', 'Kitchen Appliances']
        }
    ]

    for cat in categories:
        c.execute('INSERT INTO categories VALUES (?, ?, ?, ?, ?)',
                  (cat['id'], cat['name'], cat['icon'], cat['description'], json.dumps(cat['subcategories'])))

    coupons = [
        ('NVB10', 'percentage', 10.0, 999.0, 1500.0, 1, '10% Instant Discount on orders over ₹999'),
        ('VISION20', 'percentage', 20.0, 1999.0, 2500.0, 1, '20% Super Saver on orders over ₹1,999'),
        ('FIRST500', 'fixed', 500.0, 2499.0, 500.0, 1, 'Flat ₹500 Off for your first order over ₹2,499'),
        ('FREESHIP', 'free_shipping', 100.0, 499.0, 150.0, 1, 'Free Standard Shipping on all orders over ₹499'),
        ('FLASH50', 'percentage', 15.0, 1499.0, 3000.0, 1, 'Flash Sale exclusive 15% bonus discount')
    ]
    for cp in coupons:
        c.execute('INSERT INTO coupons VALUES (?, ?, ?, ?, ?, ?, ?)', cp)

    sellers = [
        ('seller-1', 'NVB Direct Official', 'Next Vision Brand Retail Ltd.', 'direct@nextvisionbrand.com', '+91 800-456-7890', '29AAAAA0000A1Z5', 'Approved', 4850000.0, 3420, '2026-01-10'),
        ('seller-2', 'AuraTech Global', 'Aura Technologies Private Limited', 'contact@auratech.in', '+91 98111 22334', '07BBBBB1111B2Z6', 'Approved', 2150000.0, 1280, '2026-02-15'),
        ('seller-3', 'Luxe Couture India', 'Luxe Lifestyle Apparels', 'orders@luxecouture.in', '+91 97222 33445', '27CCCCC2222C3Z7', 'Approved', 1340000.0, 890, '2026-03-01'),
        ('seller-4', 'Zenith Home & Kitchen', 'Zenith Living Appliances LLP', 'support@zenithhome.com', '+91 99333 44556', '33DDDDD3333D4Z8', 'Approved', 980000.0, 610, '2026-03-20')
    ]
    for s in sellers:
        c.execute('INSERT INTO sellers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', s)

    conn.commit()
    conn.close()
    print('Seeded 12 categories, coupons, and sellers')

if __name__ == '__main__':
    seed_meta()
