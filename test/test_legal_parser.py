from core import legal_parser


def test_parse_mount_with_o_flag():
    args = ["-o", "loop,ro"]
    result = legal_parser.parse_mount(args)
    assert result == ["-o", "loop", "ro"]


def test_parse_losetup_multiple_flags():
    args = ["--find", "--show", "-o", "512"]
    result = legal_parser.parse_losetup(args)
    assert "-o" in result and "--find" in result and "--show" in result


def test_parse_mkdir_with_p_flag():
    assert legal_parser.parse_mkdir(["-p"]) == ["-p"]


def test_parse_unzip_with_d_flag():
    assert legal_parser.parse_unzip(["-d", "/tmp"]) == ["-d"]
    assert legal_parser.parse_unzip([]) == []


def test_parse_dd_with_key_values():
    args = ["if=image.dd", "of=/dev/sda", "bs=512"]
    assert set(legal_parser.parse_dd(args)) == {"if", "of", "bs"}


def test_parse_sha256sum_with_flags():
    args = ["-c", "--tag"]
    result = legal_parser.parse_sha256sum(args)
    assert "-c" in result and "--tag" in result


def test_parse_ls_with_multiple_flags():
    args = ["-l", "-a"]
    result = legal_parser.parse_ls(args)
    assert "-l" in result and "-a" in result


def test_parse_find_with_exec_and_name():
    args = ["-name", "*.txt", "-exec", "rm"]
    result = legal_parser.parse_find(args)
    assert "-name" in result and "-exec" in result
