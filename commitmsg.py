#!/usr/bin/env python3
"""
Git commit hook:
 .git/hooks/commit-msg
"""

import argparse
import re
import inspect
from enum import Enum
from typing import NamedTuple


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


class CommitSyntaxError(Exception):
    """
    Invalid commit syntax error
    """


class CommitType(Enum):
    feat = 'new feature for the user, not a new feature for build script'
    fix = 'bug fix for the user, not a fix to a build script'
    docs = 'changes to the documentation'
    style = 'formatting, missing semi colons, etc; no production code change'
    refactor = 'refactoring production code, eg.renaming a variable'
    test = 'adding missing tests, refactoring tests; no production code change'
    chore = 'updating gradle scripts, continuous integration scripts,  etc; no production code change'


# FirstLine = NamedTuple(
#     'FirstLine',
#     [
#         ('type', CommitType),
#         ('scope', str),
#         ('subject', str)
#     ]
# )

class FirstLine(NamedTuple):
    type: CommitType
    scope: str
    subject: str


class CommitMsg:
    """
    Your commit message have to follow this format:
    <type>(<scope>): <subject>

    <body>

    <footer>
    Where :
    Message first line (type, scope and subject)
        The first line cannot be longer than {firstline_max_length} characters.
        The type and scope should always be lowercase as shown
        below.
        Allowed <type> values: {allowed_types}
        Example <scope> values:
            * ui
            * business
            * model
            * widget
            * config
            etc.
        The <scope> can be empty (e.g. if the change is a global or difficult
        to assign to a single component), in which case the parentheses are
        omitted.

    Message body (optional)
        If there is a body, it must have a blank line between the first line and
        the body.
        The body cannot be longer than {bodyline_max_length} characters.
        uses the imperative, present tense: "change" not "changed" nor
        "changes"
        includes motivation for the change and contrasts with previous behavior

    Message footer
        Referencing issues or user stories (Jira references)
        If there is a footer, it must have a body and it must have a blank line between the body and
        the footer.
        The footer cannot be longer than {footerline_max_length} characters.
    """
    FIRSTLINE_PATTERN = re.compile("^([a-z]+)(?:\(([^\n\t]+)\))?: (.+)$")
    FIRSTLINE_MAX_LENGTH = 70
    BODY_MAX_LENGTH = 80
    FOOTER_MAX_LENGTH = 80

    def __init__(self, msg_type: CommitType, scope: str, subject: str, body: str = None, footer: str = None) -> None:
        self.type = msg_type
        self.scope = scope
        self.subject = subject
        self.body = body
        self.footer = footer

    @staticmethod
    def parse(msg: str) -> 'CommitMsg':
        msg_parts = msg.split("\n\n")
        firstline = CommitMsg.parse_firstline(msg_parts[0])
        if len(msg_parts) > 1:
            body = msg_parts[1]
            CommitMsg.parse_body(body)
        else:
            body = None
        if len(msg_parts) > 2:
            footer = msg_parts[2]
            CommitMsg.parse_footer(footer)
        else:
            footer = None
        return CommitMsg(firstline.type, firstline.scope, firstline.subject, body, footer)

    @staticmethod
    def parse_firstline(firstline: str) -> FirstLine:
        if len(firstline) > CommitMsg.FIRSTLINE_MAX_LENGTH:
            raise CommitSyntaxError("First line can not be greater than {length} characters".format(
                length=CommitMsg.FIRSTLINE_MAX_LENGTH))
        result = CommitMsg.FIRSTLINE_PATTERN.search(firstline)
        if "\n" in firstline.strip():
            raise CommitSyntaxError("Two blank lines have to separate the first line and body part")
        if result is None:
            raise CommitSyntaxError("{firstline} doesn't follow the first line commit message pattern: {pattern}"
                                    .format(firstline=firstline, pattern=CommitMsg.FIRSTLINE_PATTERN.pattern))
        commit_type_str, scope, subject = result.groups()
        try:
            commit_type = CommitType[commit_type_str]
        except KeyError:
            raise CommitSyntaxError("{commit_type} is not an available commit type".format(commit_type=commit_type_str))
        return FirstLine(type=commit_type, scope=scope, subject=subject)

    @staticmethod
    def parse_body(body: str) -> str:
        for line in body.split('\n'):
            if len(line) > CommitMsg.BODY_MAX_LENGTH:
                raise CommitSyntaxError("Body line can not be greater than {length} characters".format(
                    length=CommitMsg.BODY_MAX_LENGTH))
        return body

    @staticmethod
    def parse_footer(footer: str) -> str:
        for line in footer.split('\n'):
            if len(line) > CommitMsg.FOOTER_MAX_LENGTH:
                raise CommitSyntaxError("Footer line can not be greater than {length} characters".format(
                    length=CommitMsg.FOOTER_MAX_LENGTH))
        return footer

    @staticmethod
    def format_allowed_types() -> str:
        return "\n" + "\n".join("\t* {name}: {doc}".format(name=ct.name, doc=ct.value) for ct in CommitType)

    @staticmethod
    def help() -> str:
        return inspect.getdoc(CommitMsg).format(allowed_types=CommitMsg.format_allowed_types(),
                                                firstline_max_length=CommitMsg.FIRSTLINE_MAX_LENGTH,
                                                bodyline_max_length=CommitMsg.BODY_MAX_LENGTH,
                                                footerline_max_length=CommitMsg.FOOTER_MAX_LENGTH)


if __name__ == "__main__":
    main()
