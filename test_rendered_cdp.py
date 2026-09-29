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
        print("Connected to:", ws_url)
        
        async with websockets.connect(ws_url) as ws:
            # Wait 2 seconds for fetch to complete
            await asyncio.sleep(2)
            
            # Evaluate document.getElementById('products-grid').innerHTML
            req = {
                "id": 10,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "JSON.stringify({cardCount: document.querySelectorAll('.product-card').length, titles: Array.from(document.querySelectorAll('.card-title')).map(e => e.textContent), errors: window._caughtErrors || []})"
                }
            }
            await ws.send(json.dumps(req))
            resp = await ws.recv()
            data = json.loads(resp)
            print("Evaluation result:", data["result"]["result"]["value"])
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check_rendered_products())
