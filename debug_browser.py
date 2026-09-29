import subprocess
import time
import requests
import json
import asyncio
import websockets

async def check_browser():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    proc = subprocess.Popen([
        edge_path,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "about:blank"
    ])
    
    time.sleep(1.5)
    
    try:
        tabs = requests.get("http://127.0.0.1:9222/json").json()
        ws_url = tabs[0]["webSocketDebuggerUrl"]
        print("Connected to:", ws_url)
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Log.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Page.enable"}))
            
            # Navigate to 8000
            await ws.send(json.dumps({"id": 4, "method": "Page.navigate", "params": {"url": "http://127.0.0.1:8000/"}}))
            
            start = time.time()
            while time.time() - start < 5:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    method = data.get("method")
                    if method == "Runtime.exceptionThrown":
                        details = data["params"]["exceptionDetails"]
                        print("\n>>> JS EXCEPTION:", details.get("text"), details.get("exception", {}).get("description"))
                    elif method == "Runtime.consoleAPICalled":
                        print(">>> CONSOLE:", data["params"]["type"], [a.get("value") for a in data["params"]["args"]])
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check_browser())
