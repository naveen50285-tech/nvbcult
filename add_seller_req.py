with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

def_str = '''class SellerRegisterRequest(BaseModel):
    name: str
    business_name: str
    email: str
    phone: str
    gstin: Optional[str] = ""

'''

idx = code.find('class AddProductRequest')
if idx != -1:
    code = code[:idx] + def_str + code[idx:]
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully inserted SellerRegisterRequest")
else:
    print("Could not find class AddProductRequest")
