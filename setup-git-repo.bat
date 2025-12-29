@echo off
echo ========================================
echo Setting Up Git Repository
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

echo Git is installed!
echo.

REM Check if user configured Git
git config --global user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Please configure your Git identity:
    echo.
    set /p username="Enter your name: "
    set /p useremail="Enter your email: "
    
    git config --global user.name "%username%"
    git config --global user.email "%useremail%"
    git config --global init.defaultBranch main
    
    echo.
    echo Git configured successfully!
    echo.
)

REM Check if already a Git repository
if exist ".git" (
    echo This directory is already a Git repository.
    echo.
    git status
) else (
    echo Initializing Git repository...
    git init
    echo.
    
    echo Adding files...
    git add .
    echo.
    
    echo Creating initial commit...
    git commit -m "Initial commit: Code Analyzer web application"
    echo.
    
    echo ========================================
    echo Git repository set up successfully!
    echo ========================================
    echo.
    echo You can now use Git commands like:
    echo   git status
    echo   git log
    echo   git add filename
    echo   git commit -m "message"
    echo.
)

pause
