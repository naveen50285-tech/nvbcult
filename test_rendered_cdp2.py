import subprocess
import time
import requests
import json
import asyncio
import websockets

async def check_rendered_products():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    proc = subprocess.Popen([
        edge_path,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "http://127.0.0.1:8000/"
    ])
    
    time.sleep(2)
    
    try:
        tabs = requests.get("http://127.0.0.1:9222/json").json()
        target = [t for t in tabs if "8000" in t.get("url", "")][0]
        ws_url = target["webSocketDebuggerUrl"]
        
        async with websockets.connect(ws_url) as ws:
            await asyncio.sleep(2)
            
            expr = """
            (() => {
                return JSON.stringify({
                    hasAllProducts: typeof allProducts !== 'undefined',
                    allProductsCount: typeof allProducts !== 'undefined' ? allProducts.length : -1,
                    gridInner: document.getElementById('products-grid') ? document.getElementById('products-grid').innerHTML.substring(0, 300) : 'NO_GRID',
                    location: window.location.href,
                    apiBase: typeof API_BASE !== 'undefined' ? API_BASE : 'UNDEFINED'
                });
            })()
            """
            req = {
                "id": 11,
                "method": "Runtime.evaluate",
                "params": {"expression": expr}
            }
            await ws.send(json.dumps(req))
            resp = await ws.recv()
            data = json.loads(resp)
            print("State:", data["result"]["result"]["value"])
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check_rendered_products())
