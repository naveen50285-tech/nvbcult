import urllib.request
import json

test_payload = {
    'title': 'Test Owner Electronics Device',
    'brand': 'Next Vision Brand',
    'category': 'Electronics',
    'subcategory': 'Smart Audio',
    'price': 1999.0,
    'mrp': 3999.0,
    'stock': 20,
    'images': ['https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800'],
    'short_description': 'Test device for owner upload verification',
    'seller_name': 'Next Vision Brand Official Store',
    'seller_id': 'seller-1',
    'status': 'Published'
}

req = urllib.request.Request('http://localhost:8000/api/admin/products',
                             data=json.dumps(test_payload).encode('utf-8'),
                             headers={'Content-Type': 'application/json'}, method='POST')
res = urllib.request.urlopen(req)
created = json.loads(res.read().decode('utf-8'))
print('Product Created:', created)

prods = json.loads(urllib.request.urlopen('http://localhost:8000/api/products').read().decode('utf-8'))
print('Total products after upload:', len(prods))

req_del = urllib.request.Request(f"http://localhost:8000/api/admin/products/{created['id']}", method='DELETE')
urllib.request.urlopen(req_del)
print('Test product deleted. Total products back to:', len(json.loads(urllib.request.urlopen('http://localhost:8000/api/products').read().decode('utf-8'))))
