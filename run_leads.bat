@echo off
title Lead Generation Pipeline
color 0A

cd "C:\Users\dante\OneDrive\Desktop\Automation"

echo ========================================
echo   LEAD GENERATION PIPELINE
echo ========================================
echo.
echo This will run:
echo   1. Lead Research Bot (finds businesses)
echo   2. Email Sender (sends outreach)
echo   3. Response Tracker (checks replies)
echo   4. Follow-Up Bot (sends follow-ups)
echo.
echo Press any key to start...
pause >nul

echo.
echo Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
python -c "import playwright" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Python packages...
    pip install -r requirements.txt
    
    echo Installing Playwright browsers...
    python -m playwright install chromium
)

echo.
echo ========================================
echo   STARTING PIPELINE
echo ========================================
echo.

python run_all.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   PIPELINE COMPLETE!
    echo ========================================
    echo.
    echo Check results:
    echo   - leads.csv (all leads and responses)
    echo   - scans/ folder (screenshots)
    echo.
) else (
    echo.
    echo ERROR: Pipeline failed. Check error above.
)

pause
