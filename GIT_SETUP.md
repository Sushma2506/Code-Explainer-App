# Git Installation and Setup Guide

## Step 1: Install Git for Windows

### Option A: Using winget (Recommended - Fastest)
Open Command Prompt or PowerShell as Administrator and run:
```bash
winget install --id Git.Git -e --source winget
```

### Option B: Manual Download
1. Visit: https://git-scm.com/download/win
2. Download the latest version (64-bit recommended)
3. Run the installer with these recommended settings:
   - ✅ Use Visual Studio Code as Git's default editor (or your preferred editor)
   - ✅ Git from the command line and also from 3rd-party software
   - ✅ Use bundled OpenSSH
   - ✅ Use the OpenSSL library
   - ✅ Checkout Windows-style, commit Unix-style line endings
   - ✅ Use MinTTY
   - ✅ Default (fast-forward or merge)
   - ✅ Git Credential Manager
   - ✅ Enable file system caching
   - ✅ Enable symbolic links

## Step 2: Configure Git (After Installation)

After installing, open a **NEW** terminal and run these commands:

```bash
# Set your name and email (required for commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Optional: Set your preferred editor
git config --global core.editor "code --wait"  # For VS Code
```

## Step 3: Initialize Repository for Code Analyzer

Navigate to the project directory and run:
```bash
cd C:\Users\saira\.gemini\antigravity\scratch\code-analyzer

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Code Analyzer web application"
```

## Step 4: Common Git Commands

```bash
# Check status
git status

# View changes
git diff

# Add specific file
git add filename.js

# Commit changes
git commit -m "Description of changes"

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout branch-name
```

## Step 5: Optional - Connect to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/yourusername/code-analyzer.git
git push -u origin main
```

## Verify Installation

After installation, close and reopen your terminal, then run:
```bash
git --version
```

You should see something like: `git version 2.x.x`

---

**Note**: After installing Git, you MUST close and reopen your terminal for the changes to take effect!
