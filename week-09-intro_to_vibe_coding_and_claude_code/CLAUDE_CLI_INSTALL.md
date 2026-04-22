# Claude CLI Installation Guide for Windows PowerShell

## Quick Install (One-Liner)

Open **PowerShell as Administrator** and run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

## Step-by-Step Installation

If you prefer a manual approach or the one-liner doesn't work:

**1. Install Git for Windows (required prerequisite):**
```powershell
winget install Git.Git
```

**2. Install Node.js (if not already installed):**
```powershell
winget install OpenJS.NodeJS
```

**3. Install Claude CLI via npm:**
```powershell
npm install -g @anthropics/claude-code
```

**4. Verify installation:**
```powershell
claude doctor
```

## Troubleshooting PATH Issues

If you get "command not found" after installation:

```powershell
# Check if .local/bin is in PATH
$env:PATH -split ';' | Select-String '\.local\\bin'

# If not found, add it permanently:
$PathToAdd = "$env:USERPROFILE\.local\bin"
$CurrentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
if ($CurrentPath -notlike "*$PathToAdd*") {
    [Environment]::SetEnvironmentVariable('PATH', "$CurrentPath;$PathToAdd", 'User')
}
```

After adding to PATH, **close and reopen PowerShell completely**.

## Requirements

- **Windows 10+** with PowerShell 5.1 or later
- **Pro, Max, Team, or Enterprise Claude account** (Claude Code is not available on the free plan)
- Git for Windows (for native Windows setup)

## Additional Resources

- [Claude Code Setup Guide](https://docs.claude.com/en/docs/claude-code/setup) — Official documentation
- [Claude Code CLI Reference](https://docs.claude.com/en/docs/claude-code/cli-reference) — Full CLI commands

## Notes

- Do not use `sudo npm install -g` as this can lead to permission issues and security risks
- Claude v2.1.84+ (April 2026) includes PowerShell tool support as an opt-in preview
- Run `claude doctor` after installation to verify your setup and check the installation type and version
