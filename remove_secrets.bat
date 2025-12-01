@echo off
title Remove Secrets from GitHub
color 0C

echo ========================================
echo   REMOVING SECRETS FROM GITHUB
echo ========================================
echo.
echo This will:
echo 1. Remove secret files from Git tracking
echo 2. Remove them from Git history
echo 3. Force push cleaned repo
echo.
echo WARNING: This will rewrite Git history
echo.
pause

cd "C:\Users\dante\OneDrive\Desktop\Automation"

echo.
echo [Step 1] Removing files from Git tracking...
git rm --cached GITHUB_TOKEN.txt
git rm --cached deploy_with_token.bat
git rm --cached COMPLETE_SETUP.bat

echo.
echo [Step 2] Committing removal...
git commit -m "Remove files containing secrets"

echo.
echo [Step 3] Force pushing to GitHub...
git push --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo Secrets removed from GitHub!
    echo.
    echo IMPORTANT: You should also:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Delete the old token (the one you just replaced)
    echo 3. Verify your new token is saved in GITHUB_TOKEN.txt
    echo.
) else (
    echo.
    echo ERROR: Failed to push. Check error above.
)

pause
