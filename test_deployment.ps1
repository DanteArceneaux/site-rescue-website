Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TESTING SITE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Fetching live site..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "https://zesty-dodol-376e53.netlify.app/" -UseBasicParsing
$content = $response.Content

Write-Host ""
Write-Host "Checking for NEW pricing ($1,500)..." -ForegroundColor Yellow
if ($content -match "1,500") {
    Write-Host "✅ FOUND: $1,500 pricing" -ForegroundColor Green
} else {
    Write-Host "❌ NOT FOUND: Still showing old $300 pricing" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking for Care Plan ($125/mo)..." -ForegroundColor Yellow
if ($content -match "125") {
    Write-Host "✅ FOUND: $125/mo Care Plan" -ForegroundColor Green
} else {
    Write-Host "❌ NOT FOUND: Still showing $50/mo" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking for Growth Plan ($350/mo)..." -ForegroundColor Yellow
if ($content -match "350|Growth Plan") {
    Write-Host "✅ FOUND: $350/mo Growth Plan" -ForegroundColor Green
} else {
    Write-Host "❌ NOT FOUND: Growth Plan not deployed" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking GitHub repository..." -ForegroundColor Yellow
try {
    $github = Invoke-WebRequest -Uri "https://github.com/dantearcene/site-rescue-website" -UseBasicParsing
    Write-Host "✅ GitHub repo exists and is accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot access GitHub repo" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($content -match "1,500" -and $content -match "125" -and $content -match "350") {
    Write-Host "🎉 NEW SITE IS LIVE!" -ForegroundColor Green
    Write-Host "All pricing updates are deployed." -ForegroundColor Green
} else {
    Write-Host "⚠️ OLD SITE STILL SHOWING" -ForegroundColor Yellow
    Write-Host "Need to complete Netlify GitHub connection." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Live site: https://zesty-dodol-376e53.netlify.app" -ForegroundColor Cyan
Write-Host ""
pause
