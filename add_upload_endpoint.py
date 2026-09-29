with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Check if UploadFile and File are imported
if 'UploadFile' not in code:
    code = code.replace(
        'from fastapi import FastAPI, HTTPException, Request, Response, Body',
        'from fastapi import FastAPI, HTTPException, Request, Response, Body, UploadFile, File'
    )
    print("Added UploadFile, File to imports")

# Add upload endpoint right before if __name__ == '__main__':
upload_endpoint = '''
@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    uploads_dir = os.path.join(STATIC_DIR, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower() or ".png"
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"]:
        ext = ".png"
    safe_name = f"nvb-{uuid.uuid4().hex[:8]}{ext}"
    dest_path = os.path.join(uploads_dir, safe_name)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "success": True,
        "url": f"/static/uploads/{safe_name}",
        "filename": safe_name
    }
'''

if '@app.post("/api/upload-image")' not in code:
    idx = code.rfind('@app.get("/{full_path:path}")')
    code = code[:idx] + upload_endpoint + '\n\n' + code[idx:]
    print("Added /api/upload-image endpoint")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("server.py updated with image upload capability!")
