@echo off
echo ========================================
echo    HanzlaGPT Backend Setup Script
echo ========================================
echo.

echo Step 1: Installing ngrok...
echo Downloading ngrok for Windows...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo.
echo Step 2: Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo.
echo Step 3: Cleaning up...
del ngrok.zip

echo.
echo ========================================
echo           Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start your backend: python main.py
echo 2. In new terminal: ngrok http 8000
echo 3. Copy the https:// URL from ngrok output
echo 4. Update Vercel BACKEND_URL with that URL
echo 5. Redeploy Vercel
echo.
echo Press any key to exit...
pause > nul
