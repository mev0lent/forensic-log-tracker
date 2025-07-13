
from core.logger import write_log


def test_write_log_normal_output(tmp_path):
    case_dir = tmp_path / "CASE-01"
    case_dir.mkdir()

    timestamp = "2024-05-22T10:33:45.123"
    cmd = "ls -la"
    output = "total 0\ndrwxr-xr-x"
    explanation = "Lists directory contents"
    output_hash = "abc123"

    log_path = write_log(
        case_dir=case_dir,
        cmd=cmd,
        output=output,
        explanation=explanation,
        timestamp=timestamp,
        max_lines=20,
        dry_run=False,
        output_hash=output_hash
    )

    assert log_path.exists()

    content = log_path.read_text(encoding="utf-8")

    assert "Timestamp: 2024-05-22T10:33:45.123" in content
    assert "Command:\n`ls -la`" in content
    assert "```\n" in content and "total 0" in content
    assert "Explanation:\nLists directory contents" in content
    assert f"SHA256 Output Hash:\n`{output_hash}`" in content


def test_write_log_dry_run(tmp_path):
    case_dir = tmp_path / "CASE-02"
    case_dir.mkdir()

    log_path = write_log(
        case_dir=case_dir,
        cmd="rm -rf /",
        output="(dangerous output)",
        explanation="Simulated delete",
        timestamp="2024-05-22T11:00:00.000",
        max_lines=20,
        dry_run=True,
        output_hash="dry123"
    )

    content = log_path.read_text(encoding="utf-8")

    assert "[!] DRY RUN" in content
    assert "SHA256 Output Hash:\n`dry123`" in content
