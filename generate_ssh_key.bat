@echo off
chcp 65001 >nul
echo ============================================
echo SSH Key Generator
echo ============================================
echo.
echo Generating SSH Key...
echo.

ssh-keygen -t ed25519 -C "deskmate@computer" -f %USERPROFILE%\.ssh\id_ed25519 -N ""

if errorlevel 1 (
    echo Failed to generate SSH key!
    pause
    exit /b 1
)

echo.
echo ============================================
echo SSH Key Generated Successfully!
echo ============================================
echo.
echo Your SSH Public Key (copy the line below):
echo ============================================
type %USERPROFILE%\.ssh\id_ed25519.pub
echo ============================================
echo.

start https://github.com/settings/keys

echo.
echo Next steps:
echo 1. On the webpage, click [New SSH key]
echo 2. Title: My Computer
echo 3. Key: Paste the SSH public key above
echo 4. Click [Add SSH key]
echo 5. Then run: ssh -T git@github.com
echo.
echo Press any key to exit...
pause >nul
