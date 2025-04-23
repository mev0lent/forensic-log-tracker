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

# Ask for the repo path
echo "[!] Please enter the absolute path to your forensic-log-tracker directory."
echo "    Example: /home/kali/Documents/forensic-log-tracker"
echo
read -rp "[?] Path: " repo_path

# Expand ~ to full path if used
repo_path="${repo_path/#\~/$HOME}"

# Validate directory
if [[ ! -d "$repo_path" ]]; then
    echo "[x] Error: Directory does not exist: $repo_path"
    exit 1
fi

# Validate expected structure
if [[ ! -f "$repo_path/cli.py" ]]; then
    echo "[x] Error: 'cli.py' not found in that directory. Is this the correct repo?"
    exit 1
fi

# Write .flt_env config
echo "FLT_REPO=\"$repo_path\"" > "$HOME/.flt_env"
chmod +x "$repo_path/cli.py"

# Add alias to shell config
shell_rc="$HOME/.bashrc"
[[ $SHELL == *zsh ]] && shell_rc="$HOME/.zshrc"

echo "" >> "$shell_rc"
echo "# forensic-log-tracker CLI" >> "$shell_rc"
echo "alias flt='python3 \$FLT_REPO/cli.py'" >> "$shell_rc"
echo "export FLT_REPO=\"$repo_path\"" >> "$shell_rc"

# Python environment setup
echo
echo "[+] Installing virtualenv and setting up Python environment..."
sudo apt update
sudo apt install -y python3-virtualenv

cd "$repo_path"
virtualenv -p python3 log-tracker-env
source log-tracker-env/bin/activate
pip install -r requirements.txt

echo "[+] Python virtual environment created and dependencies installed."

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
echo "[+] Setup complete"
echo "[+] Alias 'flt' added to: $shell_rc"
echo "[!] Run: source $shell_rc or restart your terminal to activate the alias"
echo
echo "[+] Example usage:"
echo "    flt new-case case001 --description 'Example case'"
echo "    flt run \"ls -la\" --case case001"
echo