import requests
import json

base = "http://127.0.0.1:8000"

def test_routes():
    print("Testing /api/health...")
    r = requests.get(f"{base}/api/health")
    print("Health:", r.status_code, r.text)

    print("\nTesting /api/categories...")
    r = requests.get(f"{base}/api/categories")
    print("Categories:", r.status_code, len(r.json()))

    print("\nTesting /api/products...")
    r = requests.get(f"{base}/api/products")
    print("Products:", r.status_code, len(r.json()))

    print("\nTesting /api/auth/login...")
    r = requests.post(f"{base}/api/auth/login", json={"username": "admin", "password": "admin123"})
    print("Login:", r.status_code, r.text)

    print("\nTesting /api/orders (GET)...")
    r = requests.get(f"{base}/api/orders")
    print("Orders GET:", r.status_code, len(r.json()))

    print("\nTesting /api/ai-assistant...")
    r = requests.post(f"{base}/api/ai-assistant", json={"query": "Hello"})
    print("AI Assistant:", r.status_code, r.text[:100])

if __name__ == "__main__":
    test_routes()
