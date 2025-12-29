# 🚀 Code Analyzer - Quick Reference

## 📦 Initial Setup

### 1. Install Git
```bash
install-git.bat
# Then close and reopen terminal
```

### 2. Initialize Git Repository
```bash
setup-git-repo.bat
```

### 3. Connect to GitHub
```bash
connect-github.bat
# Follow prompts to connect to your GitHub repo
```

## 🔄 Daily Workflow

### Quick Status Check
```bash
git-status.bat
```

### Create New Feature Branch
```bash
create-branch.bat
# Example: feature/add-dark-mode
```

### Save Your Work
```bash
quick-commit.bat
# Or specify message: quick-commit.bat "Fixed bug in analysis logic"
```

### Manual Git Commands
```bash
# Check what changed
git status
git diff

# Stage and commit
git add .
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## 📁 Project Files

### Application Files
- `index.html` - Main HTML structure
- `styles.css` - Styling and animations
- `script.js` - Analysis logic and UI
- `README.md` - Project documentation

### Git & GitHub Scripts
- `install-git.bat` - Install Git via winget
- `setup-git-repo.bat` - Initialize local repository
- `connect-github.bat` - Connect to GitHub
- `create-branch.bat` - Create/switch branches
- `git-status.bat` - View repository status
- `quick-commit.bat` - Quick commit & push

### Documentation
- `GIT_SETUP.md` - Git installation guide
- `GITHUB_SETUP.md` - GitHub integration guide
- `QUICKSTART.md` - This file

## 🎯 Common Tasks

### Starting New Feature
```bash
1. create-branch.bat
2. Enter: feature/your-feature-name
3. Make code changes
4. quick-commit.bat
5. Enter commit message
```

### Pushing to GitHub
```bash
quick-commit.bat
# Choose 'y' when asked to push
```

### Viewing Changes
```bash
git-status.bat
```

### Switching Branches
```bash
git checkout main
git checkout feature/your-branch
```

## 🔗 Useful Links

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com
- **Creating PAT**: https://github.com/settings/tokens

## ⚡ Keyboard Shortcuts (in code)

- `Ctrl+Enter` or `Cmd+Enter` - Analyze code

## 💡 Tips

1. **Commit often** - Small, frequent commits are better than large ones
2. **Use branches** - One branch per feature/fix
3. **Write clear commit messages** - Describe WHAT and WHY
4. **Pull before push** - Always pull latest changes first
5. **Use .gitignore** - Don't commit temp files or dependencies

## 🆘 Help

**Git not found?**
- Run `install-git.bat`
- Close and reopen terminal

**GitHub connection failed?**
- Use Personal Access Token, not password
- Check repository URL is correct
- See `GITHUB_SETUP.md` for details

**Lost changes?**
```bash
git reflog  # Find lost commits
git checkout <commit-hash>  # Recover
```

---

**Next Steps:**
1. Create GitHub repository: https://github.com/new
2. Run `connect-github.bat`
3. Start coding with `create-branch.bat`!
