with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_ret = '''    return {
        "valid": True, "pincode": p, "city": city, "estimated_date": est,
        "delivery_charge": 0.0, "free_delivery": True, "cod_available": True,
        "message": f"Delivery to {city} ({p}) by {est} | FREE Delivery"
    }'''

new_ret = '''    return {
        "valid": True, "available": True, "pincode": p, "city": city, "estimated_date": est,
        "estimated_days": days, "delivery_charge": 0.0, "free_delivery": True, "cod_available": True,
        "message": f"Delivery to {city} ({p}) by {est} | FREE Delivery"
    }'''

if old_ret in text:
    text = text.replace(old_ret, new_ret)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated check_delivery successfully")
else:
    print("Warning: old_ret pattern not matched")
