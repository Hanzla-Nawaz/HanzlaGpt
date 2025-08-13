Write-Host "========================================" -ForegroundColor Green
Write-Host "   Starting HanzlaGPT Backend Tunnel" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting ngrok tunnel to localhost:8000..." -ForegroundColor Yellow
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

# Start ngrok tunnel
.\ngrok.exe http 8000
