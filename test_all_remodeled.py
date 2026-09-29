import requests

base = 'http://127.0.0.1:8000'

def test_endpoint(name, method, path, data=None):
    url = f"{base}{path}"
    try:
        if method == 'GET':
            res = requests.get(url, timeout=3)
        else:
            res = requests.post(url, json=data, timeout=3)
        success = res.status_code == 200
        print(f"[{'PASS' if success else 'FAIL'}] {name} ({method} {path}): status={res.status_code}")
        if not success:
            print("   Response:", res.text[:200])
        return res
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        return None

print("=== TESTING ALL REMODELED BACKEND ENDPOINTS ===")
test_endpoint("Health Check", "GET", "/api/health")
test_endpoint("Categories", "GET", "/api/categories")
test_endpoint("Products Catalog (8 Drops)", "GET", "/api/products")
test_endpoint("Admin Login (/api/admin/login)", "POST", "/api/admin/login", {"username": "admin", "password": "admin123"})
test_endpoint("Admin Login (/api/auth/login)", "POST", "/api/auth/login", {"username": "admin", "password": "admin123"})
test_endpoint("Checkout Endpoint (/api/checkout)", "POST", "/api/checkout", {
    "customer_name": "Karthik",
    "customer_phone": "9876543210",
    "shipping_address": "Chennai, Tamil Nadu",
    "items": [{"product_id": "nvb-cult-dpa-tee-001", "title": "NVB Cult Tee", "price": 1499, "quantity": 1}]
})
test_endpoint("Orders POST Endpoint (/api/orders)", "POST", "/api/orders", {
    "customer_name": "Karthik",
    "customer_phone": "9876543210",
    "shipping_address": "Chennai, Tamil Nadu",
    "items": [{"product_id": "nvb-cyberdeck-earbuds-001", "title": "CyberDeck Buds", "price": 3499, "quantity": 1}]
})
test_endpoint("Orders Retrieval (/api/orders)", "GET", "/api/orders")
test_endpoint("AI Assistant (/api/ai-assistant)", "POST", "/api/ai-assistant", {"query": "Tell me about NVB Cult drops"})
print("===============================================")
