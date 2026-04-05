# Forensic Log Tracker

A modular CLI tool for digital forensic professionals and students. Designed to execute, document, and cryptographically sign forensic commands during investigations — producing structured, auditable evidence records.

---

## What it does

When you run a command through `flt`, it:

- Executes the command via the system shell (bash or PowerShell)
- Logs the output, truncated to a configurable preview
- Attaches a formal legal explanation for the command (German, from `explanations.yaml`)
- Hashes the output with SHA256 for integrity verification
- Optionally signs the log file with your GPG key
- Organizes everything under a named case folder

All evidence is written as plain Markdown `.log` files alongside a `.meta.json` sidecar. Reports are generated as a single `case_report.md` per case.

---

## Requirements

- Python 3.9+
- GPG (GNU Privacy Guard)
- Linux (tested on Kali) or Windows

---

## Installation
```
pip install forensic-log-tracker
```

---

## Configuration

Edit `~/.config/forensic-log-tracker/config.yaml` before first use:

```yaml
project:
  analyst: "Your Name"
  timezone: "Europe/Berlin"   # Any IANA timezone string

output:
  preview_lines: 20           # Lines shown in log preview
  hash_algorithm: "sha256"
  comment_type: "Comment"     # "Comment" or "Callout" (Obsidian-style)

gpg:
  enabled: true
  auto_verify: true
  default_key: ""             # Optional: GPG key fingerprint

logging:
  level: INFO                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

To add or extend tool explanations, edit `config/explanations.yaml`. Each entry maps a command (and optional flags) to a formal explanation used in log output and reports.

---

## Usage

### Create a case

```bash
flt new-case case001 --description "Investigating suspicious USB device"
```

Creates `logs/case001/` and writes a `description.txt`.

---

### Run a forensic command

```bash
flt run "strings /bin/ls" --case case001
```

Produces:
- `logs/case001/<timestamp>_command.log` — Markdown log with output preview, explanation, and hash
- `logs/case001/<timestamp>_command.meta.json` — structured metadata (command, hash, timestamp)
- `logs/case001/<timestamp>_command.log.sig` — GPG detached signature (if enabled)

---

### Dry-run mode

```bash
flt run "fdisk -l /dev/sdb" --case case001 --dry-run
```

Logs the command with its explanation and timestamp but does not execute it. Useful for documenting intended actions before touching evidence.

---

### Add a comment

```bash
flt comment --case case001 --text "Drive was write-protected before imaging."
```

Creates a `_comment.log` file with the analyst name and timestamp. Signed with GPG if enabled.

---

### List all cases

```bash
flt list-cases
```

---

### View case description

```bash
flt case-info --case case001
```

---

### Analyze a case

```bash
flt analyze --case case001
```

Lists all log files and signatures present in the case folder.

---

### Generate a report

```bash
flt report --case case001
```

Writes `logs/case001/case001_report.md` containing:
- Case description
- Chronological timeline of all commands and comments
- Output excerpts, SHA256 hashes, legal context, and GPG signature status per entry

To skip GPG verification during report generation:

```bash
flt report --case case001 --no-verify
```

---

### Verify output hashes

```bash
flt verify-output --case case001
```

Recomputes the SHA256 hash of each log's output block and compares it against the stored value. Reports OK or Mismatch per file.

---

### Verify a signature manually

```bash
gpg --verify logs/case001/<logfile>.log.sig
```

---

## Testing

Tests run inside Docker to ensure a clean, isolated environment.

```bash
# Build and run tests separately
make build
make test

# Build and run in one step
make run_test

# Remove leftover Docker images
make clean
```

---

## File structure

```
forensic-log-tracker/
├── core/               # Execution, logging, hashing, signing, legal explanations
├── utils/              # Config loading, path resolution, reporting, comments
├── config/
│   ├── config.yaml     # Runtime configuration
│   └── explanations.yaml  # Tool explanation database
├── templates/          # Jinja2 template for legal explanation rendering
├── forensic_log_tracker/
│   └── cli.py          # CLI entry point
├── test/               # pytest test suite
├── setup.sh            # Linux setup script
├── setup.ps1           # Windows setup script
└── Makefile            # Docker test targets
```

Logs are written to `logs/<case-id>/` and are excluded from version control by default.

---

## .gitignore

Make sure your `.gitignore` includes the following to avoid committing evidence or keys:

```
logs/
*.sig
*.log
*.meta.json
forensic-log-venv/
__pycache__/
```

---

## License

MIT — free to use, modify, and extend.
