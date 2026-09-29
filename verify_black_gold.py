import requests
import json
import sqlite3

def test_store():
    base_url = "http://localhost:8000"
    print("--- 1. Testing Homepage HTTP & Content ---")
    res = requests.get(f"{base_url}/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    html = res.text
    
    # Palette checks
    assert "#09090c" in html, "Canvas black (#09090c) not found"
    assert "#d4af37" in html, "Emblem gold (#d4af37) not found"
    assert "#fbbf24" in html, "Bright gold (#fbbf24) not found"
    assert "NVB Cult" in html, "Brand title NVB Cult not found"
    assert "DREAM • PLAN • ACHIEVE" in html, "Motto not found"
    assert "Started in 2026" in html, "'Started in 2026' not found"
    assert "Est. 2026" in html, "'Est. 2026' not found"
    
    # 90s checks
    assert "90s" not in html.lower(), "Found '90s' in HTML!"
    assert "1990" not in html, "Found '1990' in HTML!"
    print("[OK] HTML & Black with Gold Palette Verified!")

    print("\n--- 2. Checking Database & Products Endpoint ---")
    p_res = requests.get(f"{base_url}/api/products")
    assert p_res.status_code == 200
    products = p_res.json()
    print(f"Current product count: {len(products)}")
    assert len(products) == 0, f"Expected 0 dummy products, found {len(products)}"
    print("[OK] Products catalog is clean (0 example products)!")

    print("\n--- 3. Testing Owner Product Upload & Delete Cycle ---")
    test_drop = {
        "title": "NVB Imperial Heavyweight Oversized Tee 260 GSM",
        "category": "T-Shirts",
        "subcategory": "Oversized Streetwear",
        "price": 1899,
        "mrp": 3499,
        "discount": 45,
        "stock": 50,
        "sku": "NVB-TEST-GOLD-01",
        "image_url": "/static/nvb-logo.png",
        "images": ["/static/nvb-logo.png"],
        "short_description": "260 GSM French Terry cotton with gold foil typography",
        "description": "Authentic luxury specimen built with bio-washed heavyweight cotton.",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "variants": ["S", "M", "L", "XL", "XXL"],
        "tags": "nvb cult, black gold, streetwear",
        "rating": 5.0,
        "review_count": 1
    }
    
    upload_res = requests.post(f"{base_url}/api/products", json=test_drop)
    assert upload_res.status_code in [200, 201], f"Upload failed: {upload_res.status_code} {upload_res.text}"
    created_id = upload_res.json().get("id") or upload_res.json().get("product_id")
    print(f"[OK] Upload successful! Created ID: {created_id}")

    # Verify product appears in catalog
    p_check = requests.get(f"{base_url}/api/products").json()
    assert len(p_check) == 1, "Expected 1 product after test upload"
    assert p_check[0]["title"] == "NVB Imperial Heavyweight Oversized Tee 260 GSM"
    print("[OK] Product retrieved successfully in catalog!")

    # Clean up test product
    del_res = requests.delete(f"{base_url}/api/products/{created_id}")
    assert del_res.status_code in [200, 204]
    p_check2 = requests.get(f"{base_url}/api/products").json()
    assert len(p_check2) == 0, "Catalog not reset to 0 after test cleanup"
    print("[OK] Test product deleted cleanly. Catalog reset to 0!")

    print("\n--- 4. Testing Cult AI Assistant Comm-Link ---")
    ai_res = requests.post(f"{base_url}/api/ai-assistant", json={"query": "Tell me about the NVB Cult company story and motto"})
    assert ai_res.status_code == 200
    ai_data = ai_res.json()
    ai_text = ai_data.get("response", "") or ai_data.get("text", "")
    clean_ai = ai_text[:140].encode('ascii', 'replace').decode('ascii')
    print(f"AI response excerpt: {clean_ai}...")
    assert "NVB" in ai_text or "Next Vision" in ai_text
    assert "90s" not in ai_text.lower(), "Found '90s' in AI response!"
    print("[OK] Cult AI Assistant answered correctly with 2026 brand lore!")

    print("\n================ ALL VERIFICATION TESTS PASSED! ================")

if __name__ == "__main__":
    test_store()
