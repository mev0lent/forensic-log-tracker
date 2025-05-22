# core/legal_parser.py
import argparse

def parse_mount(args):
    parser = argparse.ArgumentParser(prog="mount", add_help=False)
    parser.add_argument("-o", dest="o_flags", type=str, default="")
    parsed, _ = parser.parse_known_args(args)
    return ["-o"] + parsed.o_flags.split(",") if parsed.o_flags else []

def parse_losetup(args):
    parser = argparse.ArgumentParser(prog="losetup", add_help=False)
    parser.add_argument("--find", action="store_true")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("-o", dest="offset", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.find: flags.append("--find")
    if parsed.show: flags.append("--show")
    if parsed.offset: flags.append("-o")
    return flags

def parse_mkdir(args):
    parser = argparse.ArgumentParser(prog="mkdir", add_help=False)
    parser.add_argument("-p", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-p"] if parsed.p else []

def parse_unzip(args):
    parser = argparse.ArgumentParser(prog="unzip", add_help=False)
    parser.add_argument("-d", dest="dir", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-d"] if parsed.dir else []

def parse_dd(args):
    # dd doesn’t use flags, just key=value
    flags = [a.split("=")[0] for a in args if "=" in a]
    return flags

def parse_strings(args):
    parser = argparse.ArgumentParser(prog="strings", add_help=False)
    parser.add_argument("-n", dest="num", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-n"] if parsed.num else []

def parse_mmls(args):
    parser = argparse.ArgumentParser(prog="mmls", add_help=False)
    parser.add_argument("-t", dest="type", type=str)
    parser.add_argument("-b", dest="block", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.type: flags.append("-t")
    if parsed.block: flags.append("-b")
    return flags

def parse_touch(args):
    return []  # no meaningful flags for forensic impact

def parse_shasum(args):
    parser = argparse.ArgumentParser(prog="shasum", add_help=False)
    parser.add_argument("-a", dest="algo", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-a"] if parsed.algo else []

def parse_mount_extended(args):
    flags = parse_mount(args)
    parser = argparse.ArgumentParser(prog="mount", add_help=False)
    parser.add_argument("-t", dest="type", type=str)
    parser.add_argument("-o", dest="o_flags", type=str)
    parsed, _ = parser.parse_known_args(args)
    if parsed.type:
        flags.append("-t")
    return flags

def parse_md5sum(args):
    parser = argparse.ArgumentParser(prog="md5sum", add_help=False)
    parser.add_argument("-c", dest="check", action="store_true")
    parser.add_argument("--tag", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.check: flags.append("-c")
    if parsed.tag: flags.append("--tag")
    return flags

def parse_squashfs(args):
    # Typically used as a file system, no CLI parser assumed
    return []

def parse_autopsy(args):
    # GUI tool, typically launched without arguments
    return []

def parse_awk(args):
    parser = argparse.ArgumentParser(prog="awk", add_help=False)
    parser.add_argument("-F", dest="delimiter", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-F"] if parsed.delimiter else []

def parse_basename(args):
    # Usually no flags
    return []

def parse_cal(args):
    parser = argparse.ArgumentParser(prog="cal", add_help=False)
    parser.add_argument("-m", action="store_true")  # Monday start
    parsed, _ = parser.parse_known_args(args)
    return ["-m"] if parsed.m else []

def parse_cat(args):
    parser = argparse.ArgumentParser(prog="cat", add_help=False)
    parser.add_argument("-n", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-n"] if parsed.n else []

def parse_cd(args):
    # Shell built-in, no flags
    return []

def parse_chmod(args):
    parser = argparse.ArgumentParser(prog="chmod", add_help=False)
    parser.add_argument("-R", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-R"] if parsed.R else []

def parse_chown(args):
    parser = argparse.ArgumentParser(prog="chown", add_help=False)
    parser.add_argument("-R", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-R"] if parsed.R else []

def parse_clear(args):
    return []

def parse_cp(args):
    parser = argparse.ArgumentParser(prog="cp", add_help=False)
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-p", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.r: flags.append("-r")
    if parsed.p: flags.append("-p")
    return flags

def parse_cron(args):
    # Not typically executed with flags; usually a daemon or system service
    return []

def parse_crontab(args):
    parser = argparse.ArgumentParser(prog="crontab", add_help=False)
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-e", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.l: flags.append("-l")
    if parsed.r: flags.append("-r")
    if parsed.e: flags.append("-e")
    return flags

def parse_crunch(args):
    parser = argparse.ArgumentParser(prog="crunch", add_help=False)
    parser.add_argument("-t", dest="pattern", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-t"] if parsed.pattern else []

def parse_curl(args):
    parser = argparse.ArgumentParser(prog="curl", add_help=False)
    parser.add_argument("-O", action="store_true")
    parser.add_argument("-o", dest="output", type=str)
    parser.add_argument("-L", action="store_true")
    parser.add_argument("-I", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.O: flags.append("-O")
    if parsed.output: flags.append("-o")
    if parsed.L: flags.append("-L")
    if parsed.I: flags.append("-I")
    return flags

def parse_cut(args):
    parser = argparse.ArgumentParser(prog="cut", add_help=False)
    parser.add_argument("-d", dest="delimiter", type=str)
    parser.add_argument("-f", dest="fields", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.delimiter: flags.append("-d")
    if parsed.fields: flags.append("-f")
    return flags

def parse_dc3dd(args):
    # dc3dd accepts similar flags to dd; just return key=value flags
    return [a.split("=")[0] for a in args if "=" in a]

def parse_dcfldd(args):
    # Similar to dc3dd
    return [a.split("=")[0] for a in args if "=" in a]

def parse_exiftool(args):
    # Many flags possible, but -all and -filename are common
    flags = [arg for arg in args if arg.startswith("-")]
    return flags

def parse_fdisk(args):
    parser = argparse.ArgumentParser(prog="fdisk", add_help=False)
    parser.add_argument("-l", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-l"] if parsed.l else []

def parse_file(args):
    # file -i (MIME type) and -b (brief) are most common
    parser = argparse.ArgumentParser(prog="file", add_help=False)
    parser.add_argument("-i", action="store_true")
    parser.add_argument("-b", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.i: flags.append("-i")
    if parsed.b: flags.append("-b")
    return flags

def parse_find(args):
    parser = argparse.ArgumentParser(prog="find", add_help=False)
    parser.add_argument("-name", dest="name", type=str)
    parser.add_argument("-type", dest="type", type=str)
    parser.add_argument("-exec", dest="exec", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.name: flags.append("-name")
    if parsed.type: flags.append("-type")
    if parsed.exec: flags.append("-exec")
    return flags

def parse_fls(args):
    parser = argparse.ArgumentParser(prog="fls", add_help=False)
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-m", dest="meta", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.r: flags.append("-r")
    if parsed.meta: flags.append("-m")
    return flags

def parse_grep(args):
    parser = argparse.ArgumentParser(prog="grep", add_help=False)
    parser.add_argument("-i", action="store_true")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-E", action="store_true")
    parser.add_argument("-A", dest="after", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.i: flags.append("-i")
    if parsed.r: flags.append("-r")
    if parsed.E: flags.append("-E")
    if parsed.after: flags.append("-A")
    return flags

def parse_hashcat(args):
    parser = argparse.ArgumentParser(prog="hashcat", add_help=False)
    parser.add_argument("-m", dest="mode", type=str)
    parser.add_argument("-a", dest="attack_mode", type=str)
    parser.add_argument("--force", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.mode: flags.append("-m")
    if parsed.attack_mode: flags.append("-a")
    if parsed.force: flags.append("--force")
    return flags

def parse_hexdump(args):
    parser = argparse.ArgumentParser(prog="hexdump", add_help=False)
    parser.add_argument("-C", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-C"] if parsed.C else []

def parse_history(args):
    # shell builtin, often no flags
    return []

def parse_icat(args):
    parser = argparse.ArgumentParser(prog="icat", add_help=False)
    parser.add_argument("-r", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-r"] if parsed.r else []

def parse_istat(args):
    # typically no flags, just image + inode
    return []

def parse_ls(args):
    parser = argparse.ArgumentParser(prog="ls", add_help=False)
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-a", action="store_true")
    parser.add_argument("-h", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.l: flags.append("-l")
    if parsed.a: flags.append("-a")
    if parsed.h: flags.append("-h")
    return flags

def parse_ps(args):
    parser = argparse.ArgumentParser(prog="ps", add_help=False)
    parser.add_argument("aux", nargs="?", default=None)
    parser.add_argument("-e", action="store_true")
    parser.add_argument("-f", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.aux == "aux": flags.append("aux")
    if parsed.e: flags.append("-e")
    if parsed.f: flags.append("-f")
    return flags

def parse_sha1sum(args):
    parser = argparse.ArgumentParser(prog="sha1sum", add_help=False)
    parser.add_argument("-c", dest="check", action="store_true")
    parser.add_argument("--tag", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.check: flags.append("-c")
    if parsed.tag: flags.append("--tag")
    return flags

def parse_ss(args):
    parser = argparse.ArgumentParser(prog="ss", add_help=False)
    parser.add_argument("-t", action="store_true")
    parser.add_argument("-u", action="store_true")
    parser.add_argument("-l", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.t: flags.append("-t")
    if parsed.u: flags.append("-u")
    if parsed.l: flags.append("-l")
    return flags

def parse_stat(args):
    parser = argparse.ArgumentParser(prog="stat", add_help=False)
    parser.add_argument("-c", dest="format", type=str)
    parsed, _ = parser.parse_known_args(args)
    return ["-c"] if parsed.format else []

def parse_tar(args):
    parser = argparse.ArgumentParser(prog="tar", add_help=False)
    parser.add_argument("-x", action="store_true")
    parser.add_argument("-c", action="store_true")
    parser.add_argument("-f", dest="file", type=str)
    parser.add_argument("-C", dest="directory", type=str)
    parsed, _ = parser.parse_known_args(args)

    flags = []
    if parsed.x: flags.append("-x")
    if parsed.c: flags.append("-c")
    if parsed.file: flags.append("-f")
    if parsed.directory: flags.append("-C")
    return flags

def parse_wxhexeditor(args):
    # GUI tool, rarely invoked with CLI flags
    return []

def parse_xxd(args):
    parser = argparse.ArgumentParser(prog="xxd", add_help=False)
    parser.add_argument("-r", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-r"] if parsed.r else []

def parse_sha256sum(args):
    parser = argparse.ArgumentParser(prog="sha256sum", add_help=False)
    parser.add_argument("-c", dest="check", action="store_true")
    parser.add_argument("--tag", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    flags = []
    if parsed.check: flags.append("-c")
    if parsed.tag: flags.append("--tag")
    return flags

def parse_7z(args):
    # 7z supports lots of flags, here's a simple baseline
    parser = argparse.ArgumentParser(prog="7z", add_help=False)
    parser.add_argument("mode", nargs="?", default=None)  # e.g. "x", "a", "t"
    parsed, _ = parser.parse_known_args(args)
    return [parsed.mode] if parsed.mode else []

def parse_lsblk(args):
    parser = argparse.ArgumentParser(prog="lsblk", add_help=False)
    parser.add_argument("-f", action="store_true")
    parser.add_argument("-o", dest="columns", type=str)
    parsed, _ = parser.parse_known_args(args)
    flags = []
    if parsed.f: flags.append("-f")
    if parsed.columns: flags.append("-o")
    return flags

def parse_fsstat(args):
    parser = argparse.ArgumentParser(prog="fsstat", add_help=False)
    parser.add_argument("-t", action="store_true")
    parsed, _ = parser.parse_known_args(args)
    return ["-t"] if parsed.t else []

PARSERS = {
    "mount": parse_mount_extended,
    "losetup": parse_losetup,
    "mkdir": parse_mkdir,
    "unzip": parse_unzip,
    "dd": parse_dd,
    "strings": parse_strings,
    "mmls": parse_mmls,
    "touch": parse_touch,
    "shasum": parse_shasum,
    "md5sum": parse_md5sum,
    "SquashFS": parse_squashfs,
    "autopsy": parse_autopsy,
    "awk": parse_awk,
    "basename": parse_basename,
    "cal": parse_cal,
    "cat": parse_cat,
    "cd": parse_cd,
    "chmod": parse_chmod,
    "chown": parse_chown,
    "clear": parse_clear,
    "cp": parse_cp,
    "cron": parse_cron,
    "crontab": parse_crontab,
    "crunch": parse_crunch,
    "curl": parse_curl,
    "cut": parse_cut,
    "dc3dd": parse_dc3dd,
    "dcfldd": parse_dcfldd,
    "exiftool": parse_exiftool,
    "fdisk": parse_fdisk,
    "file": parse_file,
    "find": parse_find,
    "fls": parse_fls,
    "grep": parse_grep,
    "hashcat": parse_hashcat,
    "hexdump": parse_hexdump,
    "history": parse_history,
    "icat": parse_icat,
    "istat": parse_istat,
    "ls": parse_ls,
    "ps": parse_ps,
    "sha1sum": parse_sha1sum,
    "ss": parse_ss,
    "stat": parse_stat,
    "tar": parse_tar,
    "wxHexEditor": parse_wxhexeditor,
    "xxd": parse_xxd,
    "sha256sum": parse_sha256sum,
    "7z": parse_7z,
    "lsblk": parse_lsblk,
    "fsstat": parse_fsstat,
}

