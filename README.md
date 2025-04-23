# Forensic Log Tracker

> A modular, secure CLI tool for forensic professionals and students.  
> Designed to log, document, and digitally sign command outputs during digital forensic investigations.

---

## What is this?

**Forensic Log Tracker** is a Python-based command logging system for **Kali Linux** (or any Linux distro), enabling forensic analysts to:

- ✅ Execute shell commands and automatically log the results
- ✅ Generate legal explanations per command (in **German**, for legal accuracy)
- ✅ Digitally sign logs using **GPG** for integrity and authenticity
- ✅ Structure evidence cleanly by **case**
- ✅ Generate full **Markdown reports** per case
- ✅ Verify outputs with cryptographic hashes (SHA256)

---

## ️ Setup

### Requirements

- Linux (tested on Kali)
- Python 3.9+
- GPG (GNU Privacy Guard)

---

### Setup Steps

```bash
# 1. Clone the repository
git clone <REPOSITORY-URL>
cd forensic-log-tracker

# 2. Set up a Python virtual environment
sudo apt install python3-virtualenv
virtualenv -p python3 log-tracker-env
chmod +x log-tracker-env/bin/activate
source log-tracker-env/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

> Always run commands from the **base directory of the repo** (where `cli.py` lives).

---

### Generate a GPG Key (once)

```bash
gpg --full-generate-key
```

Choose:
- Key type: RSA and RSA
- Key size: 4096 bits
- Expiry: 0 (no expiration)
- Name/email: can be fake (used offline)

---

## Configuration

### `config/config.yaml`

Customize the following values:

```yaml
analyst_name: "Your Name"
default_output_lines: 20
default_timezone: "UTC"

gpg:
  enabled: true
  auto_verify: true

output:
  preview_lines: 20
  include_sha256: true
  report_format: "md"
```

### `config/explanations.yaml`

This file maps commands (and their flags) to **formal explanations**.

> Explanations are written in formal terms. You can expand this YAML to include more tools and options.

---

## Basic CLI Usage

### Create a case folder

```bash
python cli.py new-case case001 --description "Investigating suspicious USB stick"
```

### Run a forensic command

```bash
python cli.py run "strings /bin/ls" --case case001
```

- Creates a `.log` and `.log.sig` file in `logs/case001/`
- Output is limited to configured preview lines
- Log includes legal explanation and SHA256

#### Simulate a command without executing it (dry-run)

```bash
python cli.py run "fdisk -l /dev/sdb" --case case001 --dry-run
```
The command is not actually executed.
A log file is still created with:
- Timestamp
- Command name
explanation (if available)

- The output section will contain:

```bash
[!] DRY RUN: Der Command wurde nicht wirklich ausgeführt.
```

Useful for documenting intended actions without modifying data or evidence

### Analyze logs for a case

```bash
python cli.py analyze --case case001
```

### View case info

```bash
python cli.py case-info --case case001
```

---

### Generate a full report

```bash
python cli.py report --case case001
```

Creates:  
`logs/case001/case001_report.md`

Includes:
- All commands
- Output excerpts
- SHA256 hash of each output
- Legal explanation
- GPG signature status

---

### Verify output hashes

```bash
python cli.py verify-output --case case001
```

This checks whether the SHA256 hash stored in each log matches the actual output hash.

---

## About GPG Signing

GPG ensures:
- ✅ Logs are **authentic and unaltered**
- ✅ Each `.log` file has a matching `.sig` signature
- ✅ Signatures can be verified using:

```bash
gpg --verify logs/case001/logfile.log.sig
```

---

## Example Log File

```markdown
# 2025-04-17T14:52:33Z
## Fall: case001

### Befehl:
`strings /bin/ls`

### Output (Auszug):
<FIRST_FEW_OUTPUT_LINES>

### Erklärung:
Das Tool `strings` wurde verwendet ...

### SHA256 Output Hash:
`a6f7...d3`
```

---

## Optional: Make It Shorter to Call

```bash
chmod +x cli.py
```

Then run:

```bash
./cli.py run "ls -la" --case case001
```

Or use an alias:

```bash
alias flt="python /full/path/to/cli.py"
flt report --case case001
```

---

## Folder Structure

```
forensic-log-tracker/
├── cli.py
├── core/
│   ├── executor.py
│   ├── case_manager.py
│   ├── logger.py
│   ├── gpg_signer.py
│   └── legalizer.py
├── utils/
│   └── reporting.py
├── config/
│   ├── config.yaml
│   └── explanations.yaml
├── templates/
│   └── legal.md.j2
├── logs/  # auto-generated, excluded from git
└── requirements.txt
```

---

## .gitignore tip

Make sure your `.gitignore` includes:

```
logs/
*.sig
*.log
.env/
__pycache__/
log-tracker-env/
```

To protect private evidence logs and signatures.

---

## License

MIT – free to use, extend, and improve.

---

## Contributing

You can help by:
- Adding more legal explanations
- Improving export/report styles
- Converting to HTML/PDF
- Adding GUI or web layer

