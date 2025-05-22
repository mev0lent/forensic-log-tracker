import pytest
from unittest.mock import patch, mock_open, MagicMock
from core.legalizer import get_legal_explanation


def test_get_legal_explanation_basic():
    fake_yaml = """
    mount:
      default: "Mount is used to attach file systems."
      -o: "The -o flag specifies options like read-only."
    """
    fake_template = "{{ tool }}\n{{ explanation }}"

    with patch("core.legalizer.get_config_path") as mock_config_path, \
            patch("core.legalizer.get_template_path") as mock_template_path, \
            patch("builtins.open", mock_open(read_data=fake_yaml)) as mock_yaml_open:
        # Mock YAML path
        mock_config_path.return_value.open = MagicMock(return_value=mock_open(read_data=fake_yaml).return_value)

        # Mock template path and file
        mock_template_path.return_value.exists.return_value = True
        mock_template_path.return_value.open = MagicMock(return_value=mock_open(read_data=fake_template).return_value)

        result = get_legal_explanation("mount -o ro")

        # Check the final rendered text
        assert "mount -o ro" in result
        assert "Mount is used to attach file systems." in result
        assert "The -o flag specifies options like read-only." in result


def test_sudo_prefix_handling():
    fake_yaml = "ls:\n  default: 'List directory contents.'"
    fake_template = "{{ tool }}\n{{ explanation }}"

    with patch("core.legalizer.get_config_path") as mock_config_path, \
            patch("core.legalizer.get_template_path") as mock_template_path, \
            patch("builtins.open", mock_open(read_data=fake_yaml)):
        mock_config_path.return_value.open = MagicMock(return_value=mock_open(read_data=fake_yaml).return_value)
        mock_template_path.return_value.exists.return_value = True
        mock_template_path.return_value.open = MagicMock(return_value=mock_open(read_data=fake_template).return_value)

        result = get_legal_explanation("sudo ls")

        assert "**[!] Note:** This command was executed with administrative rights" in result
