Write-Host "========================================" -ForegroundColor Green
Write-Host "   Starting HanzlaGPT SSH Tunnel" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Creating SSH tunnel via serveo.net..." -ForegroundColor Yellow
Write-Host "This will expose your localhost:8000 to the internet" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Keep this window open to maintain the tunnel!" -ForegroundColor Red
Write-Host ""
Write-Host "After you see the tunnel URL:" -ForegroundColor Cyan
Write-Host "1. Copy the https:// URL" -ForegroundColor White
Write-Host "2. Update Vercel BACKEND_URL" -ForegroundColor White
Write-Host "3. Redeploy Vercel" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the tunnel" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# Start SSH tunnel
ssh -R 80:localhost:8000 serveo.net
