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

PARSERS = {
    "mount": parse_mount,
    "losetup": parse_losetup,
    "mkdir": parse_mkdir,
    "unzip": parse_unzip,
    "dd": parse_dd,
    "strings": parse_strings,
    "mmls": parse_mmls,
}
