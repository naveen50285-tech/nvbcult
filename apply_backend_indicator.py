import os
import re

def update_store():
    store_file = r"C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\build_nvb_store.py"
    with open(store_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS for backend-status-pill if not already present
    status_css = """
        .backend-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 5px 12px;
            border-radius: var(--radius-classic);
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border: 1px solid rgba(34, 197, 94, 0.45);
            background: rgba(34, 197, 94, 0.12);
            color: #22c55e;
            box-shadow: 2px 2px 0px #000000;
            cursor: pointer;
            transition: all 0.2s;
        }
        .backend-status-pill:hover {
            transform: translate(-1px, -1px);
            box-shadow: 3px 3px 0px rgba(34, 197, 94, 0.5);
        }
        .backend-status-pill.disconnected {
            border-color: rgba(239, 68, 68, 0.45);
            background: rgba(239, 68, 68, 0.12);
            color: #ef4444;
        }
        .status-pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 8px #22c55e;
            animation: pulseGlow 1.4s infinite;
        }
        .backend-status-pill.disconnected .status-pulse-dot {
            background: #ef4444;
            box-shadow: 0 0 8px #ef4444;
        }
    """
    
    if ".backend-status-pill" not in content:
        content = content.replace("/* Header Right Actions */", status_css + "\n        /* Header Right Actions */")

    # 2. Add status pill in header-actions
    pill_html = """
                <!-- Live Backend Connection Status Indicator -->
                <div class="backend-status-pill" id="backend-status-pill" onclick="checkBackendHealth(true)" title="Click to verify FastAPI Backend & SQLite connection">
                    <span class="status-pulse-dot"></span>
                    <span id="backend-status-text">CONNECTING...</span>
                </div>
    """
    if 'id="backend-status-pill"' not in content:
        content = content.replace('<div class="header-actions">', '<div class="header-actions">' + pill_html)

    # 3. Add API_BASE and checkBackendHealth in JS
    js_api_base = """
        // Smart Backend Origin Resolver (Supports http://localhost:8000, file:///, Live Server, etc.)
        const API_BASE = (window.location.protocol === 'file:' || !window.location.host) 
            ? 'http://localhost:8000' 
            : '';
    """
    if "const API_BASE" not in content:
        content = content.replace("let allProducts = [];", js_api_base + "\n        let allProducts = [];")

    # Replace relative API paths with API_BASE
    content = content.replace('fetch("/api/products")', 'fetch(`${API_BASE}/api/products`)')
    content = content.replace('fetch(`/api/products/${prodId}`', 'fetch(`${API_BASE}/api/products/${prodId}`')
    content = content.replace('fetch("/api/orders")', 'fetch(`${API_BASE}/api/orders`)')
    content = content.replace('fetch("/api/orders",', 'fetch(`${API_BASE}/api/orders`,')
    content = content.replace('fetch(`/api/orders/${orderId}`', 'fetch(`${API_BASE}/api/orders/${orderId}`')
    content = content.replace('fetch("/api/admin/stats")', 'fetch(`${API_BASE}/api/admin/stats`)')
    content = content.replace('fetch("/api/auth/login",', 'fetch(`${API_BASE}/api/auth/login`,')
    content = content.replace('fetch("/api/ai-assistant",', 'fetch(`${API_BASE}/api/ai-assistant`,')
    content = content.replace('fetch("/api/upload-image",', 'fetch(`${API_BASE}/api/upload-image`,')
    content = content.replace('fetch("/api/admin/products",', 'fetch(`${API_BASE}/api/admin/products`,')

    # Add checkBackendHealth function and call it on load
    health_fn = """
        // ==================== LIVE BACKEND HEALTH MONITOR ====================
        async function checkBackendHealth(showToastMsg = false) {
            const pill = document.getElementById("backend-status-pill");
            const text = document.getElementById("backend-status-text");
            try {
                const res = await fetch(`${API_BASE}/api/health`);
                if (res.ok) {
                    const data = await res.json();
                    if (pill && text) {
                        pill.className = "backend-status-pill";
                        text.textContent = `BACKEND: LIVE (${data.products_count} DROPS)`;
                    }
                    if (showToastMsg) showToast(`✓ BACKEND LIVE: ${data.server} (${data.database})`);
                    return true;
                } else {
                    throw new Error("HTTP " + res.status);
                }
            } catch (err) {
                if (pill && text) {
                    pill.className = "backend-status-pill disconnected";
                    text.textContent = "BACKEND: OFFLINE";
                }
                if (showToastMsg) showToast("⚠ BACKEND OFFLINE! Run: python server.py");
                return false;
            }
        }
    """

    if "checkBackendHealth" not in content:
        content = content.replace("fetchAdminStats();", "fetchAdminStats();\n            checkBackendHealth();\n            setInterval(checkBackendHealth, 8000);")
        content = content.replace("// ==================== FETCH PRODUCTS ====================", health_fn + "\n        // ==================== FETCH PRODUCTS ====================")

    # 4. In empty archive box, display clear backend status banner
    connected_banner = """
                        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(34,197,94,0.12); border:1.5px solid rgba(34,197,94,0.35); padding:6px 14px; border-radius:4px; font-family:'Space Mono', monospace; font-size:11px; color:#22c55e; margin-bottom:18px;">
                            <span style="width:7px; height:7px; background:#22c55e; border-radius:50%; box-shadow:0 0 6px #22c55e;"></span>
                            <span>BACKEND & SQLITE DATABASE: CONNECTED (0 DROPS STORED)</span>
                        </div><br>
    """
    if "BACKEND & SQLITE DATABASE: CONNECTED" not in content:
        content = content.replace('<h3 style="font-family:\'Cinzel\', serif; font-size: 20px; font-weight: 800; text-transform: uppercase; color:#ffffff;">NVB Cult Archive Clear</h3>', connected_banner + '<h3 style="font-family:\'Cinzel\', serif; font-size: 20px; font-weight: 800; text-transform: uppercase; color:#ffffff;">NVB Cult Archive Clear</h3>')

    with open(store_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("build_nvb_store.py updated with live backend indicator and smart API_BASE.")

if __name__ == "__main__":
    update_store()
