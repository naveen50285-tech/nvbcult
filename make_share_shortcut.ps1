$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\karth\Desktop\Share NVB Cult Online.lnk")
$Shortcut.TargetPath = "C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\Create_Public_Link.bat"
$Shortcut.WorkingDirectory = "C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace"
$Shortcut.IconLocation = "C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\app_icon.ico, 0"
$Shortcut.Description = "NVB Cult - Share Public Internet Link"
$Shortcut.Save()
Write-Host "Shortcut created successfully on Desktop!"
