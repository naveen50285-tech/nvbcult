@echo off
title NVB Cult - Streamlit App Launcher
cd /d "%~dp0"
echo ========================================================
echo   NVB CULT (Next Vision Brand) - STREAMLIT APP
echo   "DREAM - PLAN - ACHIEVE" // Est. 2026
echo ========================================================
echo.
echo Starting Streamlit app on http://localhost:8501...
echo.
python -m streamlit run streamlit_app.py
pause
