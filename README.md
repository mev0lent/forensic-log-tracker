# Forensic Log Tracker

> A modular, secure CLI tool for forensic professionals and students. Designed to log, document, and digitally sign command outputs during digital forensic investigations.

---

## 🔍 What is this?

**Forensic Log Tracker** is a logging tool built for **Kali Linux** (or any Linux distro), allowing forensic analysts to:
- ✅ Execute system commands and log the output
- ✅ Automatically generate legal explanations for those commands
- ✅ Digitally sign each log with **GPG**
- ✅ Organize cases and maintain chain-of-custody integrity

---

## 🚀 Features

| Feature                        | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| 🧪 Case Management            | Create and manage forensic cases individually                |
| 🧾 Legal Explanations         | Auto-generated explanations based on the command used        |
| 🔐 GPG Signature              | Every log is optionally signed with a GPG key                |
| 📄 Clean Markdown Logs       | Human-readable, printable reports for court or review        |
| 🧠 Configurable               | Default line limits, analyst name, templates via `config.yaml` |
| ✅ Modular Core              | Easy to extend with your own tools, formats or export logic |

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

### 3. (Optional) Generate a GPG key

```bash
gpg --full-generate-key
```

---

## 🧑‍💻 Usage

### 📁 Create a new case

```bash
python cli.py new-case case001 --description "Investigating suspicious USB stick"
```

### ▶️ Run a command inside a case

```bash
python cli.py run "strings /bin/ls" --case case001
```

This creates:
- A signed `.log` file in `logs/case001/`
- A `.sig` file with the detached GPG signature

### 🔍 Analyze the case folder

```bash
python cli.py analyze --case case001
```

### 📂 List all existing cases

```bash
python cli.py list-cases
```

### 📋 Show case description

```bash
python cli.py case-info --case case001
```

---

## 🧾 Example Log Output

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
The `strings` tool was used to extract printable characters from a binary. This helps identify human-readable data such as paths, passwords, or configs without altering evidence.

### 🔐 SHA256 Output Hash:
`a6f7...d3`
```

---

## 🔐 Verifying Signatures

```bash
gpg --verify logs/case001/2025-04-17T14-52-33_command.log.sig
```

---

## 🛠 Configuration (`config/config.yaml`)

```yaml
analyst_name: "Max Mustermann"
default_output_lines: 20
default_timezone: "UTC"
```

---

## 📁 Project Structure

```
forensic-log-tracker/
├── cli.py                  # CLI interface
├── core/
│   ├── executor.py         # Executes and logs commands
│   ├── case_manager.py     # Creates case folders
│   ├── logger.py           # Writes logs to Markdown
│   ├── gpg_signer.py       # Signs logs with GPG
│   ├── legalizer.py        # Renders legal explanations
├── config/
│   ├── config.yaml         # General settings
│   └── explanations.yaml   # Tool-to-explanation mapping
├── templates/
│   └── legal.md.j2         # Jinja2 template for explanation section
├── logs/                   # Auto-created logs per case
└── requirements.txt
```

---

## ✅ Ideal For

- Cybersecurity students
- Digital forensics courses
- CTF players who want traceability
- Forensic experts writing chain-of-custody documentation
- Academic use cases

---

## 📄 License

MIT – free to use, extend, and improve.  
Pull requests are welcome!

---

## 📬 Contributions

Feel free to fork the repo, open issues, or create pull requests.  
You can contribute:
- New explanation templates
- Export functionality (e.g., PDF)
- Log search & filtering
- Timeline views

