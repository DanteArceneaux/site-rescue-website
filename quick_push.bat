@echo off
title Quick Git Push
color 0A

cd "C:\Users\dante\OneDrive\Desktop\Automation"

echo ========================================
echo   QUICK GIT PUSH
echo ========================================
echo.

:: Check if there are changes
git status

echo.
echo ----------------------------------------
set /p COMMIT_MSG="Enter commit message (or press Enter for 'Update'): "

if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update

echo.
echo Adding all changes...
git add .

echo Committing with message: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"

echo Pushing to GitHub...
git push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Changes pushed to GitHub
    echo ========================================
    echo.
    echo View at: https://github.com/DanteArceneaux/site-rescue-website
) else (
    echo.
    echo ERROR: Push failed. See error above.
)

echo.
pause
