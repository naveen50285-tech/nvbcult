import subprocess
import time
import requests
import json
import asyncio
import websockets
import shutil
import os

user_data = os.path.join(os.environ.get("TEMP", "C:\\temp"), "edge_debug_user_dir2")
if os.path.exists(user_data):
    try:
        shutil.rmtree(user_data)
    except:
        pass

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    f"--user-data-dir={user_data}",
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "http://127.0.0.1:8000/"
])

time.sleep(2.5)

async def run():
    try:
        res = requests.get("http://127.0.0.1:9222/json")
        tabs = res.json()
        print(f"Found {len(tabs)} targets:")
        target_tab = None
        for t in tabs:
            print(f" - [{t.get('type')}] {t.get('url')} (id: {t.get('id')})")
            if t.get('type') == 'page' and '8000' in t.get('url', ''):
                target_tab = t
        
        if not target_tab:
            # fallback to first page
            pages = [t for t in tabs if t.get('type') == 'page']
            if pages:
                target_tab = pages[0]

        if not target_tab:
            print("No page tab found!")
            return

        ws_url = target_tab["webSocketDebuggerUrl"]
        print("Connecting to target page ws:", ws_url)
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Log.enable"}))
            
            # Wait 2 seconds
            start = time.time()
            while time.time() - start < 2:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    m = data.get("method")
                    if m == "Runtime.exceptionThrown":
                        ex = data["params"]["exceptionDetails"]
                        print("[EXCEPTION]", ex.get("text"), ex.get("exception", {}).get("description"))
                    elif m == "Runtime.consoleAPICalled":
                        args = [a.get("value") for a in data["params"]["args"]]
                        print("[CONSOLE]", data["params"]["type"], args)
                except asyncio.TimeoutError:
                    pass
            
            # Evaluate document state
            eval_req = {
                "id": 10,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": """
                    JSON.stringify({
                        title: document.title,
                        productCards: document.querySelectorAll('.product-card').length,
                        allProductsCount: typeof allProducts !== 'undefined' ? allProducts.length : 'NOT_DEFINED',
                        filteredProductsCount: typeof filteredProducts !== 'undefined' ? filteredProducts.length : 'NOT_DEFINED',
                        cartItemsCount: typeof cartItems !== 'undefined' ? cartItems.length : 'NOT_DEFINED',
                        firstCardTitle: document.querySelector('.card-title') ? document.querySelector('.card-title').textContent : null,
                        backendStatusPill: document.getElementById('backend-status-pill') ? document.getElementById('backend-status-pill').textContent.trim() : null
                    })
                    """
                }
            }
            await ws.send(json.dumps(eval_req))
            resp = await ws.recv()
            val = json.loads(resp)["result"]["result"]["value"]
            print("\n=== DOM EVALUATION RESULT ===")
            print(val)
            print("=============================\n")
            
    finally:
        proc.terminate()

asyncio.run(run())
