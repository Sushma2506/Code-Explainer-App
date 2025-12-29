@echo off
echo ========================================
echo Connect to GitHub Repository
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please run install-git.bat first and restart your terminal
    echo.
    pause
    exit /b 1
)

REM Check if already connected to GitHub
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo This repository is already connected to GitHub:
    git remote get-url origin
    echo.
    set /p reconnect="Do you want to reconnect to a different repository? (y/n): "
    if /i not "%reconnect%"=="y" (
        echo.
        echo Keeping existing GitHub connection.
        pause
        exit /b 0
    )
    echo.
    echo Removing existing remote...
    git remote remove origin
    echo.
)

echo Please create a repository on GitHub first:
echo 1. Go to https://github.com/new
echo 2. Name it 'code-analyzer' (or your preferred name)
echo 3. Do NOT initialize with README, .gitignore, or license
echo 4. Click 'Create repository'
echo.
echo Copy the repository URL (should look like):
echo   https://github.com/your-username/code-analyzer.git
echo.

set /p repo_url="Paste your GitHub repository URL: "

if "%repo_url%"=="" (
    echo ERROR: Repository URL cannot be empty
    pause
    exit /b 1
)

echo.
echo Adding GitHub remote...
git remote add origin %repo_url%

if %errorlevel% neq 0 (
    echo ERROR: Failed to add remote
    pause
    exit /b 1
)

echo.
echo Verifying remote...
git remote -v
echo.

echo Renaming branch to 'main' (if needed)...
git branch -M main
echo.

echo Pushing to GitHub...
echo.
echo You may be prompted for credentials:
echo   Username: Your GitHub username
echo   Password: Use a Personal Access Token (NOT your password!)
echo.
echo To create a token: https://github.com/settings/tokens
echo   - Click 'Generate new token (classic)'
echo   - Select 'repo' scope
echo   - Copy the token and use it as password
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Successfully connected to GitHub!
    echo ========================================
    echo.
    echo Your code is now backed up on GitHub at:
    echo %repo_url%
    echo.
    echo You can view it in your browser:
    for /f "tokens=1,* delims=.git" %%a in ("%repo_url%") do set repo_web=%%a
    echo %repo_web%
    echo.
) else (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo Common issues:
    echo - Using password instead of Personal Access Token
    echo - Repository URL is incorrect
    echo - Network connection issues
    echo.
    echo Please check GITHUB_SETUP.md for troubleshooting
    echo.
)

pause
