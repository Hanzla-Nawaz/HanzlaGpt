@echo off
echo ========================================
echo    Starting HanzlaGPT SSH Tunnel
echo ========================================
echo.

echo Creating SSH tunnel via serveo.net...
echo This will expose your localhost:8000 to the internet
echo.
echo IMPORTANT: Keep this window open to maintain the tunnel!
echo.
echo After you see the tunnel URL:
echo 1. Copy the https:// URL
echo 2. Update Vercel BACKEND_URL
echo 3. Redeploy Vercel
echo.
echo Press Ctrl+C to stop the tunnel
echo ========================================

ssh -R 80:localhost:8000 serveo.net
