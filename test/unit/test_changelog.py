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
        with open(data_file_path('one.gitlog'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected = Commit(
            commit_id='a6f79b56acbb9e58327ecf91feed611bb614927f',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=DateUtil.str2date('2017-03-23 17:30:56 +0100'),
            type=CommitType.refactor,
            scope='changelog',
            subject='better model',
            body='NamedTuple rocks !',
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
        with open(data_file_path('big.gitlog'), encoding='utf-8') as logfile:
            log = logfile.read()
        expected_commit_with_scope = Commit(
            commit_id='a6f79b56acbb9e58327ecf91feed611bb614927f',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=DateUtil.str2date('2017-03-23 17:30:56 +0100'),
            type=CommitType.refactor,
            scope='changelog',
            subject="better model",
            body='NamedTuple rocks !',
            footer=None
        )
        expected_commit_without_scope = Commit(
            commit_id='597ec5676235e18f5a607726603df944da5be7fe',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=DateUtil.str2date('2017-03-22 15:28:45 +0100'),
            type=None,
            scope=None,
            subject='Merge branch develop into master',
            body=None,
            footer=None
        )
        # WHEN
        changelog = Changelog.parse(log)
        # THEN
        assert (len(changelog) == 35)
        assert changelog[0] == expected_commit_with_scope
        assert changelog[1] == expected_commit_without_scope

    def test_groupby(self):
        # GIVEN
        with open(data_file_path('big.gitlog'), encoding='utf-8') as logfile:
            log = logfile.read()
        changelog = Changelog.parse(log)
        # WHEN
        result = changelog.groupby(Commit.type, Commit.scope)
        # THEN
        assert result


# Tools

def data_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'data', filename)
