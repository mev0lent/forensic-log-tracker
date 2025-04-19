#core/hasher.py# core/hasher.py
import hashlib

def compute_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Compute a hash for the given string using the specified algorithm.

    Supported: sha256, md5, sha1, sha512, etc.
    """
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(data.encode("utf-8"))
        return hasher.hexdigest()
    except ValueError as e:
        raise ValueError(f"[!] Unsupported hashing algorithm: {algorithm}") from e
