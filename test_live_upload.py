import urllib.request
import json
import io

print("1. Testing Image Upload to /api/upload-image...")
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = io.BytesIO()
body.write(f'--{boundary}\r\n'.encode('utf-8'))
body.write(b'Content-Disposition: form-data; name="file"; filename="sample_headset.png"\r\n')
body.write(b'Content-Type: image/png\r\n\r\n')
body.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
body.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

req = urllib.request.Request(
    'http://localhost:8000/api/upload-image',
    data=body.getvalue(),
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)
resp = urllib.request.urlopen(req)
upload_res = json.loads(resp.read().decode('utf-8'))
print("   Image Uploaded:", upload_res)
assert upload_res['success'] is True
image_url = upload_res['url']

print("\n2. Testing Product Creation to /api/admin/products...")
prod_data = {
    "title": "NVB Wireless Studio Pro Headphones",
    "category": "Electronics",
    "subcategory": "Audio",
    "brand": "Next Vision Brand",
    "price": 3499.0,
    "mrp": 6999.0,
    "stock": 30,
    "short_description": "High-fidelity spatial audio with active noise cancellation.",
    "description": "Engineered by Next Vision Brand. 50 hours battery life, USB-C fast charging.",
    "image_url": image_url,
    "specifications": {
        "Connectivity": "Bluetooth 5.3",
        "Battery": "50 Hours",
        "Warranty": "1 Year Replacement"
    },
    "is_featured": True,
    "is_flash_sale": True
}

req_p = urllib.request.Request(
    'http://localhost:8000/api/admin/products',
    data=json.dumps(prod_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
resp_p = urllib.request.urlopen(req_p)
prod_res = json.loads(resp_p.read().decode('utf-8'))
print("   Product Created:", prod_res)
assert prod_res['status'] == 'CREATED'
new_id = prod_res['id']

print("\n3. Testing Product Appearance in Storefront Catalog...")
resp_cat = urllib.request.urlopen('http://localhost:8000/api/products')
prods = json.loads(resp_cat.read().decode('utf-8'))
found = [p for p in prods if p['id'] == new_id]
assert len(found) > 0, "New product not found in catalog!"
print(f"   Success! Product '{found[0]['title']}' is live in catalog with price Rs. {found[0]['price']} and image {found[0]['image_url']}")

print("\nPRODUCT UPLOAD PIPELINE VERIFIED 100% WORKING LIVE!")
