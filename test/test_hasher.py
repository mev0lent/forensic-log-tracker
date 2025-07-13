import pytest
import hashlib
from core.hasher import compute_hash


def test_sha256_hash_correctness():
    data = "hello"
    expected = hashlib.sha256(data.encode("utf-8")).hexdigest()
    assert compute_hash(data, "sha256") == expected


def test_md5_hash_correctness():
    data = "hello"
    expected = hashlib.md5(data.encode("utf-8")).hexdigest()
    assert compute_hash(data, "md5") == expected


def test_sha1_hash_correctness():
    data = "hello"
    expected = hashlib.sha1(data.encode("utf-8")).hexdigest()
    assert compute_hash(data, "sha1") == expected


def test_unsupported_algorithm():
    with pytest.raises(ValueError, match="Unsupported hashing algorithm"):
        compute_hash("data", "fakehash")


def test_empty_input_sha512():
    data = ""
    expected = hashlib.sha512(data.encode("utf-8")).hexdigest()
    assert compute_hash(data, "sha512") == expected
