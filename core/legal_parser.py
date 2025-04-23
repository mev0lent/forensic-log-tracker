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
}

