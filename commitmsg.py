#!/usr/local/bin/python3
"""
Git commit hook:
 .git/hooks/commit-msg
"""

import argparse
import re
import inspect
from enum import Enum

import pytest
import sys
from mypy import api


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
    except CommitSyntaxError:
        parser.error(CommitMsg.help())
        exit(1)
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


class CommitMsg:
    """
    Commit message

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
    FIRSTLINE_PATTERN = re.compile("^([a-z]+)(?:\(([a-z]+)\))?: (.+)$")
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
        firstline = msg_parts[0]
        if len(firstline) > CommitMsg.FIRSTLINE_MAX_LENGTH:
            raise CommitSyntaxError("First line can not be greater than {length} characters".format(
                length=CommitMsg.FIRSTLINE_MAX_LENGTH))
        if len(msg_parts) > 1:
            body = msg_parts[1]
            for line in body.split('\n'):
                if len(line) > CommitMsg.BODY_MAX_LENGTH:
                    raise CommitSyntaxError("Body line can not be greater than {length} characters".format(
                        length=CommitMsg.BODY_MAX_LENGTH))
        else:
            body = None
        if len(msg_parts) > 2:
            footer = msg_parts[2]
            for line in footer.split('\n'):
                if len(line) > CommitMsg.FOOTER_MAX_LENGTH:
                    raise CommitSyntaxError("Footer line can not be greater than {length} characters".format(
                        length=CommitMsg.FOOTER_MAX_LENGTH))
        else:
            footer = None
        result = CommitMsg.FIRSTLINE_PATTERN.search(firstline)
        if result is None:
            raise CommitSyntaxError("{firstline} doesn't follow the commit message pattern")
        commit_type_str, scope, subject = result.groups()
        try:
            commit_type = CommitType[commit_type_str]
        except KeyError:
            raise CommitSyntaxError("{commit_type} is not an available commit type".format(commit_type=commit_type_str))
        return CommitMsg(commit_type, scope, subject, body, footer)

    @staticmethod
    def format_allowed_types() -> str:
        return "\n" + "\n".join("\t* {name}: {doc}".format(name=ct.name, doc=ct.value) for ct in CommitType)

    @staticmethod
    def help() -> str:
        return inspect.getdoc(CommitMsg).format(allowed_types=CommitMsg.format_allowed_types(),
                                                firstline_max_length=CommitMsg.FIRSTLINE_MAX_LENGTH,
                                                bodyline_max_length=CommitMsg.BODY_MAX_LENGTH,
                                                footerline_max_length=CommitMsg.FOOTER_MAX_LENGTH)


#
# Tests
#

class TestCommitMsg:
    class TestParse:
        def test_right_msg_with_first_line(self):
            # GIVEN
            msg = "feat(ui): add button"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope == "ui"
            assert commit_msg.subject == "add button"
            assert commit_msg.body is None
            assert commit_msg.footer is None

        def test_right_msg_with_first_line_but_without_scope(self):
            # GIVEN
            msg = "fix: commit-msg hook exit"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.fix
            assert commit_msg.scope is None
            assert commit_msg.subject == "commit-msg hook exit"
            assert commit_msg.body is None
            assert commit_msg.footer is None

        def test_right_msg_with_no_scope(self):
            # GIVEN
            msg = "feat: add button"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope is None
            assert commit_msg.subject == "add button"
            assert commit_msg.body is None
            assert commit_msg.footer is None

        def test_right_msg_with_first_line_and_body_(self):
            # GIVEN
            msg = "" + \
                  "feat(ui): add button\n" + \
                  "\n" + \
                  "body first line\n" + \
                  "body second line"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope == "ui"
            assert commit_msg.subject == "add button"
            assert commit_msg.body == "body first line\nbody second line"
            assert commit_msg.footer is None

        def test_right_msg_with_first_line_and_simple_body_and_simple_footer(self):
            # GIVEN
            msg = "feat(ui): add button\n" + \
                  "\n" + \
                  "body\n" + \
                  "\n" + \
                  "footer"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope == "ui"
            assert commit_msg.subject == "add button"
            assert commit_msg.body == "body"
            assert commit_msg.footer == "footer"

        def test_wrong_msg_with_first_line(self):
            # GIVEN
            msg = "bad message"
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)

        def test_wrong_msg_with_too_long_subject(self):
            # GIVEN
            msg = "feat(ui): " + "a" * 80
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)

        def test_wrong_msg_with_too_long_body(self):
            # GIVEN
            msg = "feat(ui): add button\n" + \
                  "\n" + \
                  "b" * 90
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)

        def test_wrong_msg_with_too_long_footer(self):
            # GIVEN
            msg = "feat(ui): add button\n" + \
                  "\n" + \
                  "body\n" + \
                  "\n" + \
                  "f" * 90
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)

        def test_wrong_msg_with_unknown_type(self):
            # GIVEN
            msg = "unknown(ui): add button"
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)

        def test_wrong_msg_with_bad_separator_between_firstline_and_body(self):
            # GIVEN
            msg = "feat(ui): add button\n" + \
                  "body"
            # WHEN
            # THEN
            with pytest.raises(CommitSyntaxError):
                CommitMsg.parse(msg)


def test_static_type_check_with_mypy():
    current_file = inspect.getfile(inspect.currentframe())
    params = '{file} --ignore-missing-imports'.format(file=current_file)
    result = api.run(params)
    if result[0]:
        # FIXME: begin: There is a bug in mypy version 0.471 about support iteration on enums
        # see https://github.com/python/mypy/issues/2305
        # So, we have to remove irrelevant errors
        check_type_errors = "\n".join((error for error in result[0].strip().split("\n") if error.split("error: ")[1] not in (
            '"CommitType" expects no type arguments, but 1 given',
            'Invalid type "commit_type_str"',
            'Iterable expected',
            '"CommitType" has no attribute "__iter__"'
        )))
        # FIXME: end
        if len(check_type_errors) > 0:
            raise(Exception(check_type_errors))
    if result[1]:
        raise(Exception(result[1]))


if __name__ == "__main__":
    main()