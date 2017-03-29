#!/usr/bin/env python3
"""
Git commit hook:
 .git/hooks/commit-msg
"""

import argparse

from smartchangelog.commit import CommitMsg, CommitSyntaxError


def main() -> None:
    parser = argparse.ArgumentParser(description="Git commit message checker",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=CommitMsg.help())
    parser.add_argument("msg", help="the commit message to check")
    args = parser.parse_args()
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
