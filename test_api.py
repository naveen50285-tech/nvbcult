import json
from server import app
from fastapi.testclient import TestClient

client = TestClient(app)

res = client.get('/api/products')
print('GET /api/products status:', res.status_code)
data = res.json()
print('Total products:', data.get('total') if isinstance(data, dict) else len(data))
if isinstance(data, dict) and 'products' in data and len(data['products']) > 0:
    p = data['products'][0]
    print('Sample product keys:', list(p.keys()))
    print('Sample product id:', p.get('id'), 'title:', p.get('title'), 'price:', p.get('price'))
elif isinstance(data, list) and len(data) > 0:
    p = data[0]
    print('Sample product keys:', list(p.keys()))
    print('Sample product id:', p.get('id'), 'title:', p.get('title'), 'price:', p.get('price'))

res2 = client.get('/api/categories')
print('GET /api/categories status:', res2.status_code)
cats = res2.json()
print('Categories count:', len(cats))

res3 = client.get('/api/admin/stats')
print('GET /api/admin/stats status:', res3.status_code)
print('Admin stats keys:', list(res3.json().keys()))
