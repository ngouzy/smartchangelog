from changelog import parse, Commit, DateUtil
from commitmsg import CommitMsg, CommitType

from datetime import datetime, timezone, timedelta
import inspect
import os


class TestDateUtil:
    def test_str2date(self):
        # GIVEN
        expected = datetime(
            year=2017,
            month=3,
            day=21,
            hour=16,
            minute=9,
            second=13,
            tzinfo=timezone(timedelta(hours=1))
        )
        string = '2017-03-21 16:09:13 +0100'
        # WHEN
        date = DateUtil.str2date(string)
        # THEN
        assert date == expected

    def test_date2str(self):
        # GIVEN
        expected = '2017-03-21 16:09:13 +0100'
        dt = datetime(
            year=2017,
            month=3,
            day=21,
            hour=16,
            minute=9,
            second=13,
            tzinfo=timezone(timedelta(hours=1))
        )
        # WHEN
        string = DateUtil.date2str(dt)
        # THEN
        assert string == expected


class TestCommit:
    def test_parse(self):
        # GIVEN
        with open(logfile_path('one.log'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            message=CommitMsg(
                msg_type=CommitType.feat,
                scope='conso',
                subject='OEM-372',
                body='add field for nbAlerts'
            )
        )
        # WHEN
        commit = Commit.parse(log)
        # THEN
        assert commit == expected

    def test_equality_with_same_commit(self):
        # GIVEN
        c1 = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            raw_message="feat(conso): OEM-372\nadd field for nbAlerts"
        )
        c2 = Commit(
            commit_id='a2b6660b767113353b6203ef658074a1af73bab6',
            author='Patrick Boursier <patrick.boursier@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            raw_message="refactor(account): resizeDrawable method"
        )
        # WHEN
        # THEN
        assert c1 != c2

    def test_equality_with_other_commit(self):
        # GIVEN
        c1 = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            raw_message="feat(conso): OEM-372\nadd field for nbAlerts"
        )
        c2 = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            raw_message="feat(conso): OEM-372\nadd field for nbAlerts"
        )
        # WHEN
        # THEN
        assert c1 == c2

    def test_equality_with_other_class(self):
        # GIVEN
        c = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            raw_message="feat(conso): OEM-372\nadd field for nbAlerts"
        )
        s = "a string"
        # WHEN
        # THEN
        assert c != s


class TestParse:
    def test_parser(self):
        # GIVEN
        with open(logfile_path('big.log'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected_commit_with_raw_message = Commit(
            commit_id='6f0c30e4d03f342280f74a57aa5d263bde4c869b',
            author='Frederic DEMANY <frederic.demany@orange.com>',
            date=DateUtil.str2date('2017-03-21 16:09:13 +0100'),
            raw_message="Merge branch 'develop' of ssh://forge.orange-labs.fr/mobilecare/CoreApps_Android into develop"
        )
        expected_commit_with_message = Commit(
            commit_id='00ce370f41b52329bb47b642373fbb0ba48a74d3',
            author='Frederic DEMANY <frederic.demany@orange.com>',
            date=DateUtil.str2date('2017-03-21 16:09:02 +0100'),
            message=CommitMsg(
                msg_type=CommitType.feat,
                scope='o2',
                subject='OEMAND-412',
                body='prepaid case'
            )
        )
        # WHEN
        commits = parse(log)
        # THEN
        assert (len(commits) == 107)
        assert commits[0] == expected_commit_with_raw_message
        assert commits[1] == expected_commit_with_message


# Tools

def logfile_path(logfilename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'data', logfilename)
