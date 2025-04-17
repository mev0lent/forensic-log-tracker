Perfect! Let's do the following:

1. ✅ **Polish and expand your `README.md`**:
   - Add a full usage tutorial
   - Mention `config.yaml` and `explanations.yaml` details
   - Introduce the new `report` command
   - Explain how to avoid typing `python cli.py` every time

2. ✨ Then we’ll make it ready for GitHub or delivery.

---

## ✅ Finalized `README.md` (FULLY EXPANDED)

Replace your current one with the following:

---

# 🧾 Forensic Log Tracker

> A modular, secure CLI tool for forensic professionals and students.  
> Designed to log, document, and digitally sign command outputs during digital forensic investigations.

---

## 🔍 What is this?

**Forensic Log Tracker** is a Python-based command logging system for **Kali Linux** (or any Linux distro), enabling forensic analysts and students to:

- ✅ Execute shell commands and automatically log the results
- ✅ Generate legal explanations per command (in **German**, for legal accuracy)
- ✅ Digitally sign logs using **GPG** for integrity and authenticity
- ✅ Structure evidence cleanly by **case**
- ✅ Generate full **Markdown reports** per case

---

## 🚀 Features

| Feature                        | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| 🧪 Case Management            | Create and manage forensic cases individually                |
| 🧾 Legal Explanations         | Auto-generated (German) legal summaries of used commands     |
| 🔐 GPG Signature              | Every log is signed with your GPG key                        |
| 📄 Clean Markdown Logs       | Logs are structured, printable, and readable                 |
| 🧠 Configurable               | Templates, analyst name, line limits via `config.yaml`       |
| 📄 Report Generation         | Full case summary generated as Markdown report               |
| ✅ Modular Core              | Easy to extend with your own tools or export logic           |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/forensic-log-tracker.git
cd forensic-log-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate a GPG key (once)

```bash
gpg --full-generate-key
```

Choose:
- Key type: RSA and RSA
- Key size: 4096 bits
- Expiry: 0 (no expiration)
- Name/email: can be fake (used offline)

---

## 🔧 Configuration

### 🛠 `config/config.yaml`

Customize the following values:

```yaml
analyst_name: "Your Name"
default_output_lines: 20
default_timezone: "UTC"
```

### 🧾 `config/explanations.yaml`

This file maps commands (and their flags) to **German legal explanations**.

Currently optimized for tools like:

- `strings`, `dd`, `ls`
- `mount` with `-o ro` (for safe, read-only mounts)

> All explanations are written in formal German to support forensic/legal documentation. You can expand this YAML with more tools or flags.

---

## 🧑‍💻 Basic Usage

### 📁 Create a case folder

```bash
python cli.py new-case case001 --description "Investigating suspicious USB stick"
```

### ▶️ Run a forensic command

```bash
python cli.py run "strings /bin/ls" --case case001
```

This creates:
- ✅ A signed `.log` file in `logs/case001/`
- ✅ A detached GPG signature `.sig` for the log

### 🔍 Analyze logs for a case

```bash
python cli.py analyze --case case001
```

### 📋 View case info

```bash
python cli.py case-info --case case001
```

### 📄 Generate a full report

```bash
python cli.py report --case case001
```

This creates `logs/case001/case001_report.md`, including:
- All commands
- Outputs
- Legal explanations
- GPG signature status

---

## 🔐 About GPG Signing

GPG ensures:
- ✅ The log file hasn't been altered
- ✅ The log author is cryptographically verifiable
- ✅ Each `.log` has a matching `.log.sig` signature

### 🔍 Verifying a signature

```bash
gpg --verify logs/case001/your_log_file.log.sig
```

---

## 🧾 Example Log File

```markdown
# 🕒 2025-04-17T14:52:33Z
## 🧪 Case: case001

### 🧩 Command:
`strings /bin/ls`

### 📤 Output (Excerpt):
```
ELF
GNU
/bin/sh
```

### 🧾 Legal Explanation:
Das Tool `strings` wurde verwendet, um druckbare Zeichenketten ...
(automatisch aus explanations.yaml generiert)

### 🔐 SHA256 Output Hash:
`a6f7...d3`
```

---

## ⚡ Optional: Make It Shorter to Call

Tired of typing `python cli.py` every time?

You can make it executable directly:

```bash
chmod +x cli.py
```

Then run it as:

```bash
./cli.py run "ls -la" --case mycase
```

Or add an alias to your shell:

```bash
alias flt="python /full/path/to/cli.py"
```

Then use:

```bash
flt run "mount -o ro /dev/sdb1 /mnt" --case usbcase
```

---

## 📁 Folder Structure

```
forensic-log-tracker/
├── cli.py                  # Main CLI interface (Typer)
├── core/
│   ├── executor.py         # Executes commands
│   ├── case_manager.py     # Creates new cases
│   ├── logger.py           # Builds logs
│   ├── gpg_signer.py       # Handles GPG signature
│   └── legalizer.py        # Legal explanation system (YAML + Jinja2)
├── config/
│   ├── config.yaml         # Analyst preferences
│   └── explanations.yaml   # Command-to-explanation mapping (DE)
├── templates/
│   └── legal.md.j2         # Jinja2 template
├── logs/                   # Auto-generated case folders & logs
└── requirements.txt
```

---

## ✅ Ideal For

- Cybersecurity students
- Digital forensics education
- Chain-of-custody documentation
- Internal investigation tracking
- Demonstration and training purposes

---

## 📄 License

MIT – free to use, extend, and improve.  
Pull requests welcome!

---

## 📬 Contributing

You can contribute by:
- Expanding `explanations.yaml` with more tools
- Adding export formats (HTML, PDF)
- Creating GUI wrappers
- Improving report styling and automation
