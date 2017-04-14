import pytest

from smartchangelog.commitmsg import CommitMsg, CommitSyntaxError, CommitType


class TestCommitMsg:
    class TestParseFirstLine:
        def test_with_type_and_scope_and_subject(self):
            # GIVEN
            firstline = "feat(ui main): add button"
            # WHEN
            parsed_firstline = CommitMsg.parse_firstline(firstline)
            # THEN
            assert parsed_firstline.type == CommitType.feat
            assert parsed_firstline.scope == "ui main"
            assert parsed_firstline.subject == "add button"

        def test_with_firstline_with_type_and_subject_but_without_scope(self):
            # GIVEN
            msg = "fix: commit-msg hook exit"
            # WHEN
            firstline = CommitMsg.parse_firstline(msg)
            # THEN
            assert firstline.type == CommitType.fix
            assert firstline.scope is None
            assert firstline.subject == "commit-msg hook exit"

        def test_with_wrong_firstline_format(self):
            # GIVEN
            firstline = "bad message"
            with pytest.raises(CommitSyntaxError):
                # WHEN
                CommitMsg.parse_firstline(firstline)
                # THEN CommitSyntaxError is raised

        def test_with_unknown_type(self):
            # GIVEN
            firstline = "unknown(ui): add button"
            with pytest.raises(CommitSyntaxError):
                # WHEN
                CommitMsg.parse_firstline(firstline)
                # THEN CommitSyntaxError is raised

        def test_with_too_long_firstline_length(self):
            # GIVEN
            firstline = "feat(ui): " + "a" * (CommitMsg.FIRSTLINE_MAX_LENGTH + 1)
            with pytest.raises(CommitSyntaxError):
                # WHEN
                CommitMsg.parse_firstline(firstline)
                # THEN CommitSyntaxError is raised

    class TestParseBody:
        def test_with_too_long_body_line_length(self):
            # GIVEN
            body = "body\n" + \
                   "b" * (CommitMsg.BODY_MAX_LENGTH + 1)
            with pytest.raises(CommitSyntaxError):
                # WHEN
                CommitMsg.parse_body(body)
                # THEN CommitSyntaxError is raised

        def test_with_one_line_body(self):
            # GIVEN
            body = "body"
            # WHEN
            actual = CommitMsg.parse_body(body)
            # THEN
            assert actual == body

        def test_with_multi_line_body(self):
            # GIVEN
            body = "first line body\n" + \
                   "second line body"
            # WHEN
            actual = CommitMsg.parse_body(body)
            # THEN
            assert actual == body

    class TestParse:
        def test_with_firstline_but_without_body(self):
            # GIVEN
            msg = "feat: add button"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope is None
            assert commit_msg.subject == "add button"
            assert commit_msg.body is None

        def test_with_firstline_and_body(self):
            # GIVEN
            msg = "" + \
                  "feat(ui): add button\n" + \
                  "body first line\n" + \
                  "body second line"
            # WHEN
            commit_msg = CommitMsg.parse(msg)
            # THEN
            assert commit_msg.type == CommitType.feat
            assert commit_msg.scope == "ui"
            assert commit_msg.subject == "add button"
            assert commit_msg.body == "body first line\nbody second line"

    class TestEquality:
        def test_equality_with_same_commitmsg(self):
            # GIVEN
            cm1 = CommitMsg(
                msg_type=CommitType.feat,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
            cm2 = CommitMsg(
                msg_type=CommitType.feat,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
            # WHEN
            # THEN
            assert cm1 == cm2

        def test_equality_with_other_commitmsg(self):
            # GIVEN
            cm1 = CommitMsg(
                msg_type=CommitType.feat,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
            cm2 = CommitMsg(
                msg_type=CommitType.fix,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
            # WHEN
            # THEN
            assert cm1 != cm2

        def test_equality_with_other_class(self):
            # GIVEN
            cm = CommitMsg(
                msg_type=CommitType.feat,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
            s = "a string"
            # WHEN
            # THEN
            assert cm != s


class TestCommitType:
    def test_str(self):
        # GIVEN
        ct = CommitType.feat
        # WHEN
        string = str(ct)
        # THEN
        assert string == 'feat'

    def test_lt_with_commit_type(self):
        # GIVEN
        ct1 = CommitType.feat
        ct2 = CommitType.refactor
        # WHEN
        # THEN
        assert ct1 < ct2

    def test_lt_with_other_class(self):
        # GIVEN
        ct = CommitType.feat
        s = "a string"
        # WHEN
        # THEN
        with pytest.raises(TypeError):
            assert ct < s

