import subprocess
import time
import requests
import json
import asyncio
import websockets

async def find_syntax_error():
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
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            
            # Navigate to 8000
            await ws.send(json.dumps({"id": 3, "method": "Page.navigate", "params": {"url": "http://127.0.0.1:8000/"}}))
            
            start = time.time()
            while time.time() - start < 5:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get("method") == "Runtime.exceptionThrown":
                        details = data["params"]["exceptionDetails"]
                        print("\n===============================")
                        print("CRITICAL JAVASCRIPT ERROR:")
                        print("Message:", details.get("text"))
                        print("Line number:", details.get("lineNumber"))
                        print("Column number:", details.get("columnNumber"))
                        print("Exception:", details.get("exception"))
                        print("===============================\n")
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(find_syntax_error())
