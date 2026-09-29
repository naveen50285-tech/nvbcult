@echo off
title NVB Cult - Public Internet Tunnel
cd /d "%~dp0"
echo ========================================================
echo   NVB CULT (Next Vision Brand) - PUBLIC INTERNET LINK
echo   "DREAM - PLAN - ACHIEVE" // Est. 2026
echo ========================================================
echo.
echo Checking if NVB Cult local server is active on port 8000...
netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo [!] Server is not running! Starting server in background...
    start /b python server.py 8000
    timeout /t 3 >nul
)

echo.
echo Generating free instant public HTTPS link...
echo Anyone in the world can open this link on their mobile or PC!
echo (Keep this terminal window OPEN while sharing the link)
echo.
echo ========================================================
ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run
pause
