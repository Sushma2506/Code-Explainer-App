@echo off
echo ========================================
echo Create New Git Branch
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed
    pause
    exit /b 1
)

REM Check if we're in a Git repository
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not a Git repository
    echo Run setup-git-repo.bat first
    pause
    exit /b 1
)

REM Show current branch
echo Current branch:
git branch --show-current
echo.

REM Show all branches
echo All branches:
git branch -a
echo.

echo Common branch naming conventions:
echo   feature/add-syntax-highlighting
echo   bugfix/fix-console-error
echo   improvement/better-ui
echo   docs/update-readme
echo.

set /p branch_name="Enter new branch name: "

if "%branch_name%"=="" (
    echo ERROR: Branch name cannot be empty
    pause
    exit /b 1
)

REM Check if branch already exists
git show-ref --verify --quiet refs/heads/%branch_name%
if %errorlevel% equ 0 (
    echo.
    echo Branch '%branch_name%' already exists!
    set /p switch="Do you want to switch to it? (y/n): "
    if /i "%switch%"=="y" (
        git checkout %branch_name%
        echo.
        echo Switched to branch '%branch_name%'
    )
) else (
    echo.
    echo Creating and switching to branch '%branch_name%'...
    git checkout -b %branch_name%
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo Branch created successfully!
        echo ========================================
        echo.
        echo You are now on branch: %branch_name%
        echo.
        echo Next steps:
        echo 1. Make your changes
        echo 2. git add .
        echo 3. git commit -m "Description of changes"
        echo 4. git push -u origin %branch_name%
        echo.
    ) else (
        echo ERROR: Failed to create branch
    )
)

echo.
pause
