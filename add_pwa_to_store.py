import os

def update_pwa():
    store_file = r"C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\build_nvb_store.py"
    with open(store_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add PWA tags in <head>
    pwa_head = """    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#d4af37">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="NVB Cult">
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
"""
    if '<link rel="manifest"' not in content:
        content = content.replace('<link rel="icon" type="image/png" href="/static/favicon.png">', '<link rel="icon" type="image/png" href="/static/favicon.png">\n' + pwa_head)

    # 2. Add PWA Install Button style
    pwa_btn_css = """
        .pwa-install-btn {
            background: linear-gradient(135deg, var(--gold) 0%, var(--gold-bright) 100%) !important;
            color: #000000 !important;
            font-weight: 800 !important;
            border: 1.5px solid var(--gold-bright) !important;
            box-shadow: 2px 2px 0px #000000 !important;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
        }
        .pwa-install-btn:hover {
            transform: translate(-1px, -1px);
            box-shadow: 3px 3px 0px var(--gold-bright) !important;
            background: var(--gold-bright) !important;
        }
    """
    if ".pwa-install-btn" not in content:
        content = content.replace("/* Header Right Actions */", pwa_btn_css + "\n        /* Header Right Actions */")

    # 3. Add PWA Install Button in header-actions
    install_btn_html = """
                <button class="header-icon-btn pwa-install-btn" id="pwa-install-btn" onclick="triggerPwaInstall()" title="Install NVB Cult as Desktop/Mobile App">
                    <span>📲 INSTALL APP</span>
                </button>
    """
    if 'id="pwa-install-btn"' not in content:
        content = content.replace('<button class="header-icon-btn" onclick="filterByWishlist()"', install_btn_html + '\n                <button class="header-icon-btn" onclick="filterByWishlist()"')

    # 4. Add Service Worker registration and PWA prompt logic in <script>
    pwa_js = """
        // ==================== PWA INSTALL & SERVICE WORKER ====================
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js')
                    .then(reg => console.log('NVB Cult SW registered:', reg.scope))
                    .catch(err => console.log('NVB Cult SW register failed:', err));
            });
        }

        let deferredPrompt = null;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            const btn = document.getElementById('pwa-install-btn');
            if (btn) btn.style.display = 'inline-flex';
        });

        async function triggerPwaInstall() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    showToast('INSTALLING NVB CULT APP...');
                }
                deferredPrompt = null;
            } else {
                alert("✦ TO INSTALL NVB CULT AS AN APP:\\n\\n1. Look for the 'Install App' icon (⊕) on the right side of your browser address bar.\\n2. Click 'Install' to add NVB Cult to your Windows Start Menu, Taskbar & Desktop!\\n\\nOr use the desktop shortcut created on your desktop: 'NVB Cult App'");
            }
        }
    """
    if "PWA INSTALL & SERVICE WORKER" not in content:
        content = content.replace("// Initialize Store on load", pwa_js + "\n        // Initialize Store on load")

    with open(store_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("build_nvb_store.py updated with PWA install support.")

if __name__ == "__main__":
    update_pwa()
