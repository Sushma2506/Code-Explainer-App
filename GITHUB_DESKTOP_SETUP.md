# Configuring Antigravity in GitHub Desktop

## Antigravity Executable Path

```
C:\Users\saira\AppData\Local\Programs\Antigravity\Antigravity.exe
```

## How to Add to GitHub Desktop

### Step 1: Open GitHub Desktop Settings
1. Open **GitHub Desktop**
2. Click **File** → **Options** (or press `Ctrl+,`)
3. Go to the **Integrations** tab

### Step 2: Configure External Editor
1. In the "External editor" dropdown, click **Select**
2. If Antigravity doesn't appear in the list:
   - Click **"Browse"** or **"Other"**
   - Navigate to: `C:\Users\saira\AppData\Local\Programs\Antigravity`
   - Select `Antigravity.exe`
   - Click **Open**

### Step 3: Verify Configuration
- You should now see "Antigravity" in the external editor dropdown
- Click **Save** or **OK**

## Using Antigravity from GitHub Desktop

After configuration, you can open your repository in Antigravity by:

1. **From the menu bar:**
   - Repository → Open in Antigravity
   - (Or press `Ctrl+Shift+A`)

2. **From the toolbar:**
   - Click the "Open in Antigravity" button

3. **Right-click on a file:**
   - Right-click any file in the changes list
   - Select "Open in Antigravity"

## Alternative: Create a Launcher Script

If GitHub Desktop has issues with direct .exe integration, create a launcher script:

### Create `launch-antigravity.bat`:
```batch
@echo off
start "" "C:\Users\saira\AppData\Local\Programs\Antigravity\Antigravity.exe" %*
```

Then in GitHub Desktop settings, point to this `.bat` file instead.

## Troubleshooting

**Can't find Antigravity.exe?**
- Copy this path and paste it in File Explorer:
  ```
  C:\Users\saira\AppData\Local\Programs\Antigravity
  ```

**GitHub Desktop doesn't recognize it?**
- Try the launcher script method above
- Make sure Antigravity is fully installed and can launch normally

**Want to open a specific folder?**
- In GitHub Desktop, click "Open in Antigravity"
- It will open the repository folder in Antigravity

---

**Quick Copy-Paste Path:**
```
C:\Users\saira\AppData\Local\Programs\Antigravity\Antigravity.exe
```
