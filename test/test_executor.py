import pytest
from unittest.mock import patch, MagicMock
from core.executor import execute_command


def test_execute_command_dry_run_returns_expected_output():
    case = "CASE001"
    cmd = "echo Hello"
    dry_run = True

    with patch("core.executor.get_case_log_path") as mock_path, \
            patch("core.executor.get_legal_explanation", return_value="Legal info") as mock_legal, \
            patch("core.executor.compute_hash", return_value="fakehash") as mock_hash, \
            patch("core.executor.write_log", return_value="logfile.txt") as mock_log, \
            patch("core.executor.logger") as mock_logger:
        mock_path.return_value = MagicMock()

        logfile, output = execute_command(cmd, case, dry_run=dry_run)

        # Check logger was used
        mock_logger.info.assert_called_once_with(f"Executing command: {cmd}")

        # Assert dry run message is returned
        assert "[!] DRY RUN" in output
        assert logfile == "logfile.txt"

        # Check helper functions were used
        mock_legal.assert_called_once()
        mock_hash.assert_called_once()
        mock_log.assert_called_once()
