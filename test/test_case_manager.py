import os
from unittest.mock import patch
from core.case_manager import create_case_folder


def test_create_case_folder_writes_description(tmp_path):
    case = "TEST123"
    description = "This is a test case."

    # Simulate get_case_log_path returning a temp path
    with patch("core.case_manager.get_case_log_path", return_value=tmp_path):
        create_case_folder(case, description)

        # Check directory exists
        assert tmp_path.exists()
        assert tmp_path.is_dir()

        # Check that description.txt exists
        desc_path = tmp_path / "description.txt"
        assert desc_path.exists()

        # Verify contents of the description file
        content = desc_path.read_text(encoding="utf-8")
        assert f"Case-ID: {case}" in content
        assert f"Description: {description}" in content