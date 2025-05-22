import pytest
from pathlib import Path
from utils.commenter import write_comment


@pytest.fixture
def setup_test_environment(monkeypatch, tmp_path):
    tmp_case_dir = tmp_path / "case123"
    tmp_case_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("utils.commenter.load_config", lambda: {
        "TIMEZONE": None,
        "project": {"analyst": "Max Mustermann"},
        "output": {
            "comment_type": "Callout"
        },
        "gpg": {"enabled": True}
    })

    monkeypatch.setattr("utils.commenter.get_case_log_path", lambda case, create=False: tmp_case_dir)
    monkeypatch.setattr("utils.commenter.sign_file", lambda path: None)

    return tmp_case_dir


def test_write_callout(setup_test_environment):
    comment_file = write_comment("case123", "Dies ist ein Testkommentar.")
    assert comment_file.exists()

    content = comment_file.read_text()
    assert ">[!Info] Comment from analyst: Max Mustermann" in content
    assert "> Dies ist ein Testkommentar." in content


def test_write_comment(monkeypatch, tmp_path):
    tmp_case_dir = tmp_path / "case456"
    tmp_case_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("utils.commenter.load_config", lambda: {
        "TIMEZONE": None,
        "project": {"analyst": "Erika Musterfrau"},
        "output": {
            "comment_type": "Comment"
        },
        "gpg": {"enabled": False}
    })

    monkeypatch.setattr("utils.commenter.get_case_log_path", lambda case, create=False: tmp_case_dir)
    monkeypatch.setattr("utils.commenter.sign_file", lambda path: None)

    comment_file = write_comment("case456", "Ein klassischer Kommentar.")
    assert comment_file.exists()

    content = comment_file.read_text()
    assert "#### [+] Comment from analyst: Erika Musterfrau" in content
    assert "Ein klassischer Kommentar." in content
