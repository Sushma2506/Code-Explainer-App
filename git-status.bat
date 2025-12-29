@echo off
echo ========================================
echo Git Repository Status
echo ========================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed
    pause
    exit /b 1
)

echo Current Branch:
git branch --show-current
echo.

echo ----------------------------------------
echo Working Directory Status:
echo ----------------------------------------
git status
echo.

echo ----------------------------------------
echo Recent Commits (last 5):
echo ----------------------------------------
git log --oneline -5 --graph
echo.

echo ----------------------------------------
echo Remote Repository:
echo ----------------------------------------
git remote -v
echo.

echo ----------------------------------------
echo Local Branches:
echo ----------------------------------------
git branch
echo.

echo ========================================
echo Quick Commands:
echo ========================================
echo   create-branch.bat     - Create new branch
echo   git add .             - Stage all changes
echo   git commit -m "msg"   - Commit changes
echo   git push              - Push to GitHub
echo   git pull              - Pull from GitHub
echo.

pause
