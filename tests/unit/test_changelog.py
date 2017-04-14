from smartchangelog import datetools
from smartchangelog.changelog import Changelog, Node
from smartchangelog.commit import Commit
from smartchangelog.commitmsg import CommitType
from tests.unit import data_file_path


class TestChangelog:
    def test_parse(self):
        # GIVEN
        with open(data_file_path('big.gitlog'), encoding='utf-8') as log_file:
            log = log_file.read()
        expected_commit_with_scope = Commit(
            id='a6f79b56acbb9e58327ecf91feed611bb614927f',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=datetools.str2date('2017-03-23 17:30:56 +0100'),
            type=CommitType.refactor,
            scope='changelog',
            subject="better model",
            body='NamedTuple rocks !'
        )
        expected_commit_without_scope = Commit(
            id='597ec5676235e18f5a607726603df944da5be7fe',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=datetools.str2date('2017-03-22 15:28:45 +0100'),
            type=None,
            scope=None,
            subject='Merge branch develop into master',
            body=None
        )
        # WHEN
        changelog = Changelog.parse(log)
        # THEN
        assert (len(changelog) == 35)
        assert changelog[0] == expected_commit_with_scope
        assert changelog[1] == expected_commit_without_scope

    def test_groupby(self):
        # GIVEN
        with open(data_file_path('big.gitlog'), encoding='utf-8') as log_file:
            log = log_file.read()
        changelog = Changelog.parse(log)
        # WHEN
        node = changelog.groupby(Commit.type, Commit.scope)
        # THEN
        assert len(node) == len(changelog)


class TestNode:
    def test_len_with_empty_tree(self):
        # GIVEN
        tree = Node()
        # WHEN
        # THEN
        assert len(tree) == 1

    def test_len_with_small_tree(self):
        # GIVEN
        children = tuple([Node(name=str(i)) for i in range(10)])
        tree = Node(children=children)
        # WHEN
        actual = len(tree)
        # THEN
        assert actual == 10

    def test_len_with_tree(self):
        # GIVEN
        children = tuple([Node(name=str(i), children=tuple([Node(), Node()])) for i in range(10)])
        tree = Node(children=children)
        # WHEN
        actual = len(tree)
        # THEN
        assert actual == 20

    def test_report_with_big_git_log(self):
        # GIVEN
        with open(data_file_path('big.gitlog'), encoding='utf-8') as log_file:
            log = log_file.read()
        changelog = Changelog.parse(log)
        node = changelog.groupby(Commit.type, Commit.scope)
        with open(data_file_path('big.md'), encoding='utf-8') as md_file:
            expected = md_file.read()
        # WHEN
        report = node.report()
        # THEN
        assert report == expected
