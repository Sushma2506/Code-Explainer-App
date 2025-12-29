@echo off
echo ========================================
echo Installing Git for Windows using winget
echo ========================================
echo.

echo Checking if winget is available...
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: winget is not available on this system.
    echo.
    echo Please use one of these alternatives:
    echo 1. Windows 11 or Windows 10 with App Installer from Microsoft Store
    echo 2. Manual download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo.
echo Installing Git...
winget install --id Git.Git -e --source winget

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Git installed successfully!
    echo ========================================
    echo.
    echo IMPORTANT: You must CLOSE and REOPEN your terminal
    echo for Git to be available in your PATH.
    echo.
    echo After reopening terminal, run: git --version
    echo.
) else (
    echo.
    echo Installation failed. Please try manual installation:
    echo https://git-scm.com/download/win
    echo.
)

pause
