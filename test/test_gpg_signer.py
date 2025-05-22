import subprocess
from unittest.mock import patch, MagicMock
from core.gpg_signer import sign_file
from pathlib import Path


def test_sign_file_success():
    test_path = Path("dummy.log")

    with patch("core.gpg_signer.subprocess.run") as mock_run:
        # Simulate successful run
        mock_run.return_value = MagicMock()
        result = sign_file(test_path)

        mock_run.assert_called_once_with(
            ["gpg", "--batch", "--yes", "--output", "dummy.log.sig", "--detach-sign", "dummy.log"],
            check=True
        )
        assert result is True


def test_sign_file_failure():
    test_path = Path("dummy.log")

    with patch("core.gpg_signer.subprocess.run", side_effect=subprocess.CalledProcessError(1, "gpg")):
        result = sign_file(test_path)
        assert result is False