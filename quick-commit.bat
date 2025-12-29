@echo off
echo ========================================
echo Quick Commit and Push
echo ========================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed
    pause
    exit /b 1
)

git status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not a Git repository
    pause
    exit /b 1
)

echo Current branch: 
git branch --show-current
echo.

echo Changed files:
git status --short
echo.

if "%1"=="" (
    set /p commit_msg="Enter commit message: "
) else (
    set commit_msg=%*
)

if "%commit_msg%"=="" (
    echo ERROR: Commit message cannot be empty
    pause
    exit /b 1
)

echo.
echo Staging all changes...
git add .

echo.
echo Committing with message: "%commit_msg%"
git commit -m "%commit_msg%"

if %errorlevel% neq 0 (
    echo.
    echo Nothing to commit (no changes detected)
    pause
    exit /b 0
)

echo.
set /p push="Push to GitHub? (y/n): "
if /i "%push%"=="y" (
    echo.
    echo Pushing to GitHub...
    git push
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo Successfully committed and pushed!
        echo ========================================
    ) else (
        echo.
        echo Failed to push. You may need to set upstream:
        for /f "tokens=*" %%a in ('git branch --show-current') do set current_branch=%%a
        echo   git push -u origin %current_branch%
    )
) else (
    echo.
    echo Changes committed locally (not pushed to GitHub)
    echo Run 'git push' when ready to push
)

echo.
pause
