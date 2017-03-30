#!/usr/bin/env python3
"""
Git commit hook:
 .git/hooks/commit-msg
"""

import argparse

from smartchangelog.commit import CommitMsg, CommitSyntaxError
from smartchangelog import __version__
from smartchangelog.githook import install, uninstall


def main() -> None:
    parser = argparse.ArgumentParser(description="Git commit message checker",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=CommitMsg.help())
    parser.add_argument("-v", "--version", help="print commit-msg version number", action="version",
                        version=__version__)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("msg", help="the commit message to check", nargs="?")
    group.add_argument("-i", "--install_hook", action="store_true")
    group.add_argument("-u", "--uninstall_hook", action="store_true")

    args = parser.parse_args()

    if args.install_hook:
        hook_path = install()
        if hook_path:
            print("commit-msg hook installed in {path}".format(path=hook_path))
    elif args.uninstall_hook:
        hook_path = uninstall()
        if hook_path:
            print("commit-msg hook removed from {path}".format(path=hook_path))
    else:
        msg = args.msg
        if "COMMIT_EDITMSG" in msg:
            with open(args.msg) as msg_file:
                msg = msg_file.read()
        try:
            CommitMsg.parse(msg)
        except CommitSyntaxError as e:
            parser.error("{error}\n\n{help}".format(error=e, help=CommitMsg.help()))

    exit(0)


if __name__ == "__main__":
    main()
