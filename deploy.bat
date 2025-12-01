@echo off
echo ========================================
echo Deploying to Netlify...
echo ========================================
cd website
netlify deploy --prod
pause
