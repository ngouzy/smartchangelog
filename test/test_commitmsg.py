import pytest

from commitmsg import CommitMsg, CommitSyntaxError, CommitType

import inspect

import pytest
from mypy import api


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
        check_type_errors = "\n".join(
            (error for error in result[0].strip().split("\n") if error.split("error: ")[1] not in (
                '"CommitType" expects no type arguments, but 1 given',
                'Invalid type "commit_type_str"',
                'Iterable expected',
                '"CommitType" has no attribute "__iter__"'
            )))
        # FIXME: end
        if len(check_type_errors) > 0:
            raise (Exception(check_type_errors))
    if result[1]:
        raise (Exception(result[1]))
