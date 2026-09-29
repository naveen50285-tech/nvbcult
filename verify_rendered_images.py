import asyncio, websockets, requests, json

async def check():
    tabs = requests.get('http://127.0.0.1:9222/json').json()
    page = [t for t in tabs if t.get('type') == 'page' and '8000' in t.get('url', '')][0]
    async with websockets.connect(page['webSocketDebuggerUrl']) as ws:
        req = {
            'id': 100,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': 'Array.from(document.querySelectorAll(".card-img")).map(i => i.src)',
                'returnByValue': True
            }
        }
        await ws.send(json.dumps(req))
        resp = await ws.recv()
        data = json.loads(resp)
        print("Rendered Card Image Sources in Browser:")
        for s in data['result']['result']['value']:
            print("  ->", s)

asyncio.run(check())
