$ws = New-Object -ComObject WScript.Shell

$s1 = $ws.CreateShortcut('C:\Users\karth\Desktop\NVB Cult Streamlit App.lnk')
$s1.TargetPath = 'C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\Launch_Streamlit_App.bat'
$s1.WorkingDirectory = 'C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace'
$s1.Save()

$s2 = $ws.CreateShortcut('C:\Users\karth\Desktop\Share NVB Cult Streamlit Online.lnk')
$s2.TargetPath = 'C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace\Share_Streamlit_Public_Link.bat'
$s2.WorkingDirectory = 'C:\Users\karth\.gemini\antigravity\scratch\nvb-marketplace'
$s2.Save()

Write-Output "Shortcuts created successfully."
