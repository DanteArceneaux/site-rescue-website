# Refresh PATH to include Git
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "PATH refreshed!" -ForegroundColor Green
Write-Host ""
Write-Host "Testing Git..." -ForegroundColor Yellow
git --version

Write-Host ""
Write-Host "Git is now available!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run git commands in this terminal." -ForegroundColor Cyan
