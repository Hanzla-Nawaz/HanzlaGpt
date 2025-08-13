@echo off
echo ========================================
echo    Starting HanzlaGPT Backend Tunnel
echo ========================================
echo.

echo Starting ngrok tunnel to localhost:8000...
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

.\ngrok.exe http 8000
