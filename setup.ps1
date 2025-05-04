# setup.ps1 - Windows setup script for forensic-log-tracker

Write-Host @"
           _.-=-._
         o~`  '  > `.
         `.  ,       :
           `"-.__/    `.
              `--'\     \
                 |     |
               .-'     ;-.
              /  |   .:    \
             (_.'|  |  `--/
                 \  \    /
                  `-.__/
        Forensic Log Tracker — Setup Utility
"@

Write-Host ""
Write-Host "[+] Welcome to the Forensic Log Tracker Setup!"
Write-Host ""

# Detect project root automatically
$repo_path = $PSScriptRoot

Write-Host "[+] Setting up the project at: $repo_path"

# Create virtual environment if it doesn't exist
$venv_path = Join-Path $repo_path "forensic-log-venv"
if (-not (Test-Path $venv_path)) {
    Write-Host "[+] Creating Python virtual environment..."
    python -m venv $venv_path
} else {
    Write-Host "[*] Virtual environment already exists. Skipping creation."
}

# Activate virtual environment
$activate_script = Join-Path $venv_path "Scripts\Activate.ps1"
. $activate_script

# Upgrade pip and install project dependencies
Write-Host "[+] Installing project dependencies using pyproject.toml..."
pip install --upgrade pip
pip install -e .

# Create a PowerShell function for the flt command
$profile_path = $PROFILE
$flt_function = @"

# forensic-log-tracker CLI
function flt {
    & "$venv_path\Scripts\flt.exe" `$args
}
"@

# Check if the profile exists, create it if it doesn't
if (-not (Test-Path $profile_path)) {
    $profile_dir = Split-Path $profile_path -Parent
    if (-not (Test-Path $profile_dir)) {
        New-Item -ItemType Directory -Path $profile_dir -Force | Out-Null
    }
    New-Item -ItemType File -Path $profile_path -Force | Out-Null
}

# Check if flt function already exists in the profile
$profile_content = Get-Content $profile_path -ErrorAction SilentlyContinue
if ($profile_content -notcontains "function flt {") {
    Add-Content -Path $profile_path -Value $flt_function
    Write-Host "[+] Function 'flt' added to PowerShell profile: $profile_path"
} else {
    Write-Host "[*] Function 'flt' already exists in PowerShell profile. Skipping addition."
}

# GPG key check and prompt
Write-Host ""
Write-Host "[!] Checking for existing GPG keys..."
$gpg_keys = gpg --list-keys
if ($gpg_keys -match "sec") {
    Write-Host "[+] GPG key already exists. Skipping generation."
} else {
    Write-Host "[!] No GPG key found."
    Write-Host "[!] It's recommended to create one now."
    $gen_key = Read-Host "[?] Generate a new GPG key now? (y/n)"
    if ($gen_key -match "^[Yy]$") {
        gpg --full-generate-key
    } else {
        Write-Host "[!] Skipping GPG key creation. You can run 'gpg --full-generate-key' later."
    }
}

Write-Host ""
Write-Host "[+] Setup complete!"
Write-Host ""
Write-Host "[!] IMPORTANT: To start using forensic-log-tracker:"
Write-Host "    1. Restart your PowerShell session or run: . $profile_path     # To load the 'flt' function"
Write-Host "    2. Run: . $activate_script   # To activate the virtual environment"
Write-Host ""
Write-Host "[+] Example usage afterwards:"
Write-Host "    flt new-case case001 --description ""Example case"""
Write-Host "    flt run ""ls -la"" --case case001"
Write-Host ""
Write-Host "[+] Happy tracking!"