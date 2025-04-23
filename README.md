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
```

# 2. Make the setup script executable and run it
```bash
chmod +x setup.sh
./setup.sh
```

---

## Configuration

### `config/config.yaml`

Customize the following values:

```yaml
project:
  analyst: "Max Mustermann"
  timezone: "UTC"

execution:
  default_output_lines: 20
  dry_run_label: "[!] DRY RUN: Command not executed."

output:
  language: "de"              # "en", "de" – for future translation of explanations
  format: "md"                # "md", "html", "pdf" - NOT WORKING YET
  preview_lines: 20
  include_sha256: true
  hash_algorithm: "sha256"

gpg:
  enabled: true
  auto_verify: true
  default_key: ""             # optional: GPG fingerprint

logging:
  level: INFO                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### `config/explanations.yaml`

This file maps commands (and their flags) to **formal explanations**.

> Explanations are written in formal terms. You can expand this YAML to include more tools and options.

---

## Basic CLI Usage

### Create a case folder

```bash
flt new-case case001 --description "Investigating suspicious USB stick"
```

### Run a forensic command

```bash
flt run "strings /bin/ls" --case case001
```

- Creates a `.log` and `.log.sig` file in `logs/case001/`
- Output is limited to configured preview lines
- Log includes legal explanation and SHA256

#### Simulate a command without executing it (dry-run)

```bash
flt run "fdisk -l /dev/sdb" --case case001 --dry-run
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
flt analyze --case case001
```

### View case info

```bash
flt case-info --case case001
```

---

### Generate a full report

```bash
flt report --case case001
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
flt verify-output --case case001
```

This checks whether the SHA256 hash stored in each log matches the actual output hash.

---

## About GPG Signing

GPG ensures:
- ✅ Logs are **authentic and unaltered**
- ✅ Each `.log` file has a matching `.sig` signature
- ✅ Signatures can be verified using:

```bash
gpg --verify path/to/repo/logs/case001/logfile.log.sig
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

