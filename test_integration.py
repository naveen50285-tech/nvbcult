import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("1. Testing GET /api/categories...")
res = client.get('/api/categories')
assert res.status_code == 200, f"Categories failed: {res.status_code}"
cats = res.json()
print(f"   Success: {len(cats)} categories returned")

print("2. Testing GET /api/products...")
res = client.get('/api/products')
assert res.status_code == 200, f"Products failed: {res.status_code}"
prods = res.json()
assert len(prods) > 0, "No products found"
p0 = prods[0]
print(f"   Success: {len(prods)} products. Sample: {p0['title']} (Rs. {p0['price']})")
assert 'image_url' in p0, "image_url field missing"
assert 'discount_percent' in p0, "discount_percent field missing"
assert 'category_name' in p0, "category_name field missing"

print("3. Testing GET /api/delivery-check?pincode=560038...")
res = client.get('/api/delivery-check?pincode=560038')
assert res.status_code == 200
print("   Success:", res.json())

print("4. Testing POST /api/cart and GET /api/cart...")
res = client.post('/api/cart', json={"product_id": p0['id'], "quantity": 1, "session_id": "test-session"})
assert res.status_code == 200
cart_item = res.json()
res = client.get('/api/cart?session_id=test-session')
assert res.status_code == 200
cart_list = res.json()
print(f"   Success: Cart has {len(cart_list)} items")

print("5. Testing GET /api/coupons/validate?code=VISION20&order_amount=5000...")
res = client.get('/api/coupons/validate?code=VISION20&order_amount=5000')
assert res.status_code == 200
print("   Success:", res.json())

print("6. Testing POST /api/ai-assistant...")
res = client.post('/api/ai-assistant', json={"query": "laptop for programming and coding"})
assert res.status_code == 200
ai_data = res.json()
print(f"   Success: AI responded with {len(ai_data.get('recommended_products', []))} products")
assert 'response' in ai_data or 'text' in ai_data

print("7. Testing GET /api/admin/stats...")
res = client.get('/api/admin/stats')
assert res.status_code == 200
stats = res.json()
print(f"   Success: Revenue: Rs. {stats['revenue']:,}, Orders: {stats['orders_count']}")
assert 'revenue_chart' in stats
assert 'category_distribution' in stats

print("8. Testing Section 37: 3-column product adder POST /api/admin/products...")
new_prod_payload = {
    "title": "NVB Quantum Ultra Wireless Earbuds",
    "category_id": 1,
    "subcategory": "Audio",
    "brand": "NVB Vision",
    "sku": "NVB-QEAR-01",
    "price": 2999.0,
    "mrp": 5999.0,
    "stock": 40,
    "short_description": "Active Noise Cancelling earbuds with 48h battery life.",
    "description": "Premium wireless earbuds with spatial audio and ultra-low latency.",
    "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800",
    "specifications": {"Driver": "11mm Dynamic", "ANC": "45dB", "Bluetooth": "5.3"},
    "is_featured": True,
    "is_flash_sale": True,
    "deal_of_the_day": False
}
res = client.post('/api/admin/products', json=new_prod_payload)
assert res.status_code == 200, f"Add product failed: {res.text}"
print("   Success:", res.json())

print("9. Testing Section 38: Bulk import POST /api/admin/bulk-import...")
bulk_payload = {
    "products": [
        {
            "title": "NVB Pro Mechanical Keyboard RGB",
            "category": "Electronics",
            "subcategory": "Accessories",
            "brand": "NVB",
            "sku": "NVB-KB-RGB",
            "price": 4499.0,
            "mrp": 7999.0,
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
            "short_description": "Hot-swappable tactile RGB mechanical gaming keyboard."
        }
    ]
}
res = client.post('/api/admin/bulk-import', json=bulk_payload)
assert res.status_code == 200, f"Bulk import failed: {res.text}"
print("   Success:", res.json())

print("10. Testing POST /api/products/{id}/reviews...")
res = client.post(f"/api/products/{p0['id']}/reviews", json={
    "rating": 5,
    "title": "Outstanding quality!",
    "comment": "Exceeded all expectations. NVB delivery was super fast too.",
    "author": "Priya Sharma",
    "verified_purchase": True
})
assert res.status_code == 200, f"Review failed: {res.text}"
print("   Success:", res.json())

print("11. Testing static / index.html...")
res = client.get('/')
assert res.status_code == 200
assert 'NEXT VISION BRAND' in res.text
print("   Success: index.html served on root /")

print("\nALL 11 BACKEND AND FRONTEND INTEGRATION TESTS PASSED PERFECTLY!")
