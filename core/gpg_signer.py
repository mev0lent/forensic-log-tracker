# core/gpg_signer.py
import subprocess
from pathlib import Path

def sign_file(log_path: Path) -> bool:
    sig_path = log_path.with_suffix(log_path.suffix + ".sig")
    try:
        subprocess.run(
            ["gpg", "--batch", "--yes", "--output", str(sig_path), "--detach-sign", str(log_path)],
            check=True
        )
        print(f"🔐 Logdatei signiert: {sig_path.name}")
        return True
    except subprocess.CalledProcessError:
        print("[!] GPG-Signatur fehlgeschlagen – ist ein Schlüssel verfügbar?")
        return False

