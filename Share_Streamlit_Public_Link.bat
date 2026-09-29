@echo off
title NVB Cult Streamlit - Public Internet Link
cd /d "%~dp0"
echo ========================================================
echo   NVB CULT STREAMLIT - PUBLIC INTERNET TUNNEL
echo   "DREAM - PLAN - ACHIEVE" // Est. 2026
echo ========================================================
echo.
echo Checking if NVB Cult Streamlit is active on port 8501...
netstat -ano | findstr :8501 >nul
if errorlevel 1 (
    echo [!] Streamlit is not running! Starting Streamlit in background...
    start /b python -m streamlit run streamlit_app.py --server.headless true --server.port 8501
    timeout /t 4 >nul
)

echo.
echo Generating free instant public HTTPS link for Streamlit...
echo Anyone in the world can open this link on their mobile or PC!
echo (Keep this terminal window OPEN while sharing the link)
echo.
echo ========================================================
ssh -o StrictHostKeyChecking=no -R 80:localhost:8501 nokey@localhost.run
pause
