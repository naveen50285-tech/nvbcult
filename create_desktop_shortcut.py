import os
import subprocess

def make_shortcut():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(base_dir, "Launch_NVB_Cult_App.bat")
    ico_path = os.path.join(base_dir, "app_icon.ico")
    desktop_dir = os.path.expanduser("~/Desktop")
    if not os.path.exists(desktop_dir):
        desktop_dir = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    
    lnk_path = os.path.join(desktop_dir, "NVB Cult App.lnk")

    # Create the launcher bat file if not exists
    bat_content = f"""@echo off
title NVB Cult App Launcher
cd /d "%~dp0"
python app.py
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"Created batch launcher at: {bat_path}")

    # Use PowerShell WScript.Shell to create the .lnk shortcut
    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{lnk_path}')
    $Shortcut.TargetPath = '{bat_path}'
    $Shortcut.WorkingDirectory = '{base_dir}'
    $Shortcut.IconLocation = '{ico_path}, 0'
    $Shortcut.Description = 'NVB Cult — Official App (Dream • Plan • Achieve)'
    $Shortcut.Save()
    """
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if os.path.exists(lnk_path):
        print(f"[OK] Desktop Shortcut successfully created on your Windows Desktop:\n  {lnk_path}")
    else:
        print(f"Notice: Could not write .lnk directly, bat launcher is available at: {bat_path}")

if __name__ == "__main__":
    make_shortcut()
