# GitHub Integration Guide

## Prerequisites
✅ Git installed (run `install-git.bat` if not done)  
✅ Git repository initialized (run `setup-git-repo.bat` if not done)  
✅ GitHub account created (https://github.com/signup)

## Option 1: Automated GitHub Setup (Easiest)

### Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `code-analyzer` (or your preferred name)
3. Description: "AI-powered code analyzer with line-by-line explanations and improvement suggestions"
4. **Important**: Leave "Initialize this repository" options UNCHECKED (no README, .gitignore, or license)
5. Click "Create repository"

### Step 2: Run the Setup Script
After creating the GitHub repository, run:
```bash
connect-github.bat
```
This script will:
- Prompt for your GitHub repository URL
- Add GitHub as remote origin
- Push your code to GitHub
- Set up tracking for the main branch

## Option 2: Manual GitHub Setup

### 1. Create GitHub Repository
Follow Step 1 from Option 1 above.

### 2. Connect Local Repository to GitHub
```bash
# Replace USERNAME and REPO_NAME with your values
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Enter GitHub Credentials
When prompted:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password!)

### Creating a Personal Access Token (PAT)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "Code Analyzer Development"
4. Expiration: Choose your preference (90 days recommended)
5. Scopes: Check **`repo`** (full control of private repositories)
6. Click "Generate token"
7. **COPY THE TOKEN** - you won't see it again!
8. Use this token as your password when Git prompts you

## Working with Branches

### Create a New Feature Branch
```bash
# Create and switch to new branch
git checkout -b feature/add-syntax-highlighting

# Or use the script
create-branch.bat
```

### Common Branch Commands
```bash
# List all branches
git branch

# Switch to existing branch
git checkout branch-name

# See which branch you're on
git branch --show-current

# Delete a branch (after merging)
git branch -d branch-name
```

## Typical Workflow

### 1. Make Changes on a Feature Branch
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make your changes in code editor
# ...

# Check what changed
git status
git diff

# Stage changes
git add .

# Commit changes
git commit -m "Add new feature: description"

# Push to GitHub
git push -u origin feature/new-feature
```

### 2. Create Pull Request on GitHub
1. Go to your repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Select your feature branch
4. Add description of changes
5. Click "Create pull request"

### 3. Merge and Clean Up
After PR is approved:
```bash
# Switch back to main
git checkout main

# Pull latest changes
git pull origin main

# Delete local feature branch
git branch -d feature/new-feature
```

## Syncing with GitHub

### Push Changes to GitHub
```bash
# Push current branch
git push

# Push specific branch
git push origin branch-name

# Force push (use with caution!)
git push --force
```

### Pull Changes from GitHub
```bash
# Pull and merge
git pull

# Pull from specific branch
git pull origin main

# Fetch without merging
git fetch
```

## Useful Git Commands

```bash
# See commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# Stash changes temporarily
git stash
git stash pop

# View remote repository info
git remote -v
```

## GitHub CLI (Optional)

For advanced workflows, install GitHub CLI:
```bash
winget install --id GitHub.cli
```

Then you can:
```bash
# Create repository from command line
gh repo create

# Create pull request
gh pr create

# View pull requests
gh pr list
```

## Troubleshooting

### "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin YOUR_GITHUB_URL
```

### Authentication Issues
- Use Personal Access Token, not password
- Enable 2FA on GitHub for better security
- Consider using SSH keys instead of HTTPS

### "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

---

**Next Steps:**
1. Run `connect-github.bat` to connect to GitHub
2. Use `create-branch.bat` when starting new features
3. Commit regularly with meaningful messages
4. Push to GitHub frequently to back up your work
