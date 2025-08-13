@echo off
echo ========================================
echo    Getting LocalTunnel URL...
echo ========================================
echo.

echo Starting localtunnel and getting URL...
lt --port 8000 --subdomain hanzlagpt-backend

echo.
echo ========================================
echo           URL Retrieved!
echo ========================================
echo.
echo Copy the https:// URL from above
echo Update Vercel BACKEND_URL with that URL
echo.
echo Press any key to exit...
pause > nul
