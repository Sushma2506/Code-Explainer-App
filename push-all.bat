@echo off
echo ========================================
echo Commit All Files and Push to GitHub
echo ========================================
echo.

REM Check Git status
echo Checking repository status...
git status
echo.

echo ----------------------------------------
echo This will add ALL files and push to GitHub
echo ----------------------------------------
echo.

set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Step 1: Adding all files...
git add .

echo.
echo Step 2: Committing...
set /p message="Enter commit message (or press Enter for default): "

if "%message%"=="" (
    set message=Add code analyzer project files and documentation
)

git commit -m "%message%"

if %errorlevel% neq 0 (
    echo.
    echo No changes to commit or commit failed
    pause
    exit /b 1
)

echo.
echo Step 3: Pushing to GitHub...
git push

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Successfully pushed to GitHub!
    echo ========================================
    echo.
    echo View your repository at:
    git remote get-url origin
    echo.
) else (
    echo.
    echo Push failed. You may need to:
    echo 1. Connect to GitHub first: connect-github.bat
    echo 2. Or set upstream: git push -u origin main
    echo.
)

pause
