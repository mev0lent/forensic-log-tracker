# core/hasher.py
import hashlib

def sha256_from_string(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
