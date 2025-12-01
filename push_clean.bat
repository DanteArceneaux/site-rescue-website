@echo off
title Push Clean Repository
color 0A

cd "C:\Users\dante\OneDrive\Desktop\Automation"

echo ========================================
echo   PUSHING CLEAN REPOSITORY
echo ========================================
echo.

echo [Step 1] Removing secret files from Git...
git rm --cached GITHUB_TOKEN.txt 2>nul
git rm --cached deploy_with_token.bat 2>nul
git rm --cached COMPLETE_SETUP.bat 2>nul
git rm --cached remove_secrets.bat 2>nul

echo.
echo [Step 2] Adding updated .gitignore...
git add .gitignore

echo.
echo [Step 3] Committing changes...
git commit -m "Update .gitignore to exclude secrets"

echo.
echo [Step 4] Pushing to GitHub...
git push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo Repository cleaned and pushed!
) else (
    echo.
    echo ERROR: Push failed. See error above.
)

echo.
pause
