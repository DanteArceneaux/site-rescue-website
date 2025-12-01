@echo off
echo ========================================
echo   DEPLOYING TO GITHUB
echo ========================================
echo.

cd "C:\Users\dante\OneDrive\Desktop\Automation"

echo Checking authentication...
gh auth status
if errorlevel 1 (
    echo.
    echo ERROR: Not authenticated with GitHub
    echo Please run: gh auth login
    pause
    exit /b 1
)

echo.
echo Creating repository and pushing code...
gh repo create site-rescue-website --public --source=. --remote=origin --push

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create repository
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Repository created: https://github.com/dantearcene/site-rescue-website
echo.
echo Next step: Connect to Netlify
echo   1. Go to: https://app.netlify.com/sites/zesty-dodol-376e53/configuration/deploys
echo   2. Click "Link repository"
echo   3. Select "site-rescue-website"
echo   4. Deploy!
echo.
pause
