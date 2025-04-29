#!/bin/bash

clear

cat << "EOF"
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
EOF

echo
echo "[+] Welcome to the Forensic Log Tracker Setup!"
echo

# Detect project root automatically
repo_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[+] Setting up the project at: $repo_path"

# Create virtual environment if it doesn't exist
if [[ ! -d "$repo_path/forensic-log-venv" ]]; then
    echo "[+] Creating Python virtual environment..."
    python3 -m venv "$repo_path/forensic-log-venv"
else
    echo "[*] Virtual environment already exists. Skipping creation."
fi

# Activate virtual environment
source "$repo_path/forensic-log-venv/bin/activate"

# Upgrade pip and install project dependencies
echo "[+] Installing project dependencies using pyproject.toml..."
pip install --upgrade pip
pip install .

# Decide which shell RC file to use
shell_rc="$HOME/.bashrc"
if [[ $SHELL == *zsh ]]; then
    shell_rc="$HOME/.zshrc"
fi

# Check if flt alias already exists
if ! grep -q "alias flt=" "$shell_rc"; then
    echo "" >> "$shell_rc"
    echo "# forensic-log-tracker CLI" >> "$shell_rc"
    echo "alias flt='$repo_path/forensic-log-venv/bin/flt'" >> "$shell_rc"
    echo "[+] Alias 'flt' added to: $shell_rc"
else
    echo "[*] Alias 'flt' already exists in $shell_rc. Skipping alias addition."
fi

# ⚠️ DO NOT source .bashrc/.zshrc here (different shell syntax!)
echo
echo "[!] Please run 'source $shell_rc' manually after setup to activate the 'flt' alias."
echo

# GPG key check and prompt
echo
echo "[!] Checking for existing GPG keys..."
if gpg --list-keys | grep -q sec; then
    echo "[+] GPG key already exists. Skipping generation."
else
    echo "[!] No GPG key found."
    echo "[!] It's recommended to create one now."
    read -rp "[?] Generate a new GPG key now? (y/n): " gen_key
    if [[ "$gen_key" =~ ^[Yy]$ ]]; then
        gpg --full-generate-key
    else
        echo "[!] Skipping GPG key creation. You can run 'gpg --full-generate-key' later."
    fi
fi

echo
echo "[+] Setup complete!"
echo
echo "[!] IMPORTANT: To start using forensic-log-tracker:"
echo "    1. Run: source $shell_rc     # To load the 'flt' alias"
echo "    2. Run: source forensic-log-venv/bin/activate   # To activate the virtual environment"
echo
echo "[+] Example usage afterwards:"
echo "    flt new-case case001 --description \"Example case\""
echo "    flt run \"ls -la\" --case case001"
echo
echo "[+] Happy tracking!"
