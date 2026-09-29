import os
import sys
import time
import socket
import subprocess
import urllib.request
import webbrowser

PORT = 8000
URL = f"http://127.0.0.1:{PORT}"
HEALTH_URL = f"{URL}/api/health"

def is_server_running():
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=1.5) as res:
            return res.status == 200
    except Exception:
        return False

def find_app_browser():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def start_server_background():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(base_dir, "server.py")
    
    print("Starting NVB Cult backend server...")
    proc = subprocess.Popen(
        [sys.executable, server_script],
        cwd=base_dir,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    return proc

def main():
    print("====================================================")
    print("    NVB CULT (Next Vision Brand) - DESKTOP APP      ")
    print("         \"DREAM • PLAN • ACHIEVE\" // Est. 2026       ")
    print("====================================================")

    server_process = None
    if not is_server_running():
        server_process = start_server_background()
        # Wait up to 10 seconds for server to be ready
        for _ in range(20):
            time.sleep(0.5)
            if is_server_running():
                break
        else:
            print("[!] Warning: Server did not respond to health check in time.")

    print(f"Backend active at {URL}")
    browser_exe = find_app_browser()

    if browser_exe:
        print(f"Launching NVB Cult Desktop Window via: {os.path.basename(browser_exe)} App Mode...")
        app_args = [
            browser_exe,
            f"--app={URL}",
            "--window-size=1340,860",
            "--window-position=120,60"
        ]
        try:
            app_proc = subprocess.Popen(app_args)
            app_proc.wait()
        except KeyboardInterrupt:
            pass
    else:
        print("Opening in default browser...")
        webbrowser.open(URL)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    if server_process:
        print("Closing backend server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
