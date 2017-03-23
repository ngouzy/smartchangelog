import inspect
import os
from datetime import datetime, timezone, timedelta

from changelog import Changelog, Commit, DateUtil
from commitmsg import CommitType


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
        with open(data_file_path('one.log'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected = Commit(
            commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
            author='Vincent Boesch <vincent.boesch@orange.com>',
            date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
            type=CommitType.feat,
            scope='conso',
            subject='OEM-372',
            body='add field for nbAlerts',
            footer=None
        )
        # WHEN
        changelog_item = Commit.parse(log)
        # THEN
        assert changelog_item == expected

    def test_strip_lines(self):
        # GIVEN
        string = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Phasellus non erat imperdiet, pellentesque nibh et, porta velit.

                Fusce sit amet elit ac magna congue accumsan sed ut tellus.
            Nullam at velit tincidunt, sodales mi quis, gravida metus.


            Quisque pellentesque ipsum nec nunc vehicula tincidunt.
        """
        expected = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n" \
                   "Phasellus non erat imperdiet, pellentesque nibh et, porta velit.\n" \
                   "\n" \
                   "Fusce sit amet elit ac magna congue accumsan sed ut tellus.\n" \
                   "Nullam at velit tincidunt, sodales mi quis, gravida metus.\n" \
                   "\n" \
                   "\n" \
                   "Quisque pellentesque ipsum nec nunc vehicula tincidunt."
        # WHEN
        actual = Commit.strip_lines(string)
        # THEN
        assert actual == expected


class TestChangelog:
    def test_parse(self):
        # GIVEN
        with open(data_file_path('big.log'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected_commit_without_scope = Commit(
            commit_id='6f0c30e4d03f342280f74a57aa5d263bde4c869b',
            author='Frederic DEMANY <frederic.demany@orange.com>',
            date=DateUtil.str2date('2017-03-21 16:09:13 +0100'),
            type=None,
            scope=None,
            subject="Merge branch 'develop' of ssh://forge.orange-labs.fr/mobilecare/CoreApps_Android into develop",
            body=None,
            footer=None
        )
        expected_commit_with_scope = Commit(
            commit_id='00ce370f41b52329bb47b642373fbb0ba48a74d3',
            author='Frederic DEMANY <frederic.demany@orange.com>',
            date=DateUtil.str2date('2017-03-21 16:09:02 +0100'),
            type=CommitType.feat,
            scope='o2',
            subject='OEMAND-412',
            body='prepaid case',
            footer=None
        )
        # WHEN
        commits = Changelog.parse(log)
        # THEN
        assert (len(commits) == 107)
        assert commits[0] == expected_commit_without_scope
        assert commits[1] == expected_commit_with_scope


# Tools

def data_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'data', filename)
