import hashlib
from pathlib import Path

import pytest

from integrity import verify_sha256


def test_verify_sha256_aceita_e_rejeita(tmp_path):
    p = tmp_path / "arquivo.txt"
    p.write_bytes(b"abc")
    verify_sha256(p, hashlib.sha256(b"abc").hexdigest())
    with pytest.raises(ValueError, match="SHA-256"):
        verify_sha256(p, "0" * 64)
