import inspect
import os

from smartchangelog.changelog import Changelog, Commit, Node
from smartchangelog.commit import CommitType
from smartchangelog import datetools


class TestCommit:
    def test_parse(self):
        # GIVEN
        with open(data_file_path('one.gitlog'), encoding='utf-8') as log_file:
            log = log_file.read()
        expected = Commit(
            id='a6f79b56acbb9e58327ecf91feed611bb614927f',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=datetools.str2date('2017-03-23 17:30:56 +0100'),
            type=CommitType.refactor,
            scope='changelog',
            subject='better model',
            body='NamedTuple rocks !'
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

    def test_property_name(self):
        # GIVEN
        prop = Commit.author
        # WHEN
        property_name = Commit.property_name(prop)
        # THEN
        assert property_name == 'author'


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
            body='NamedTuple rocks !',
            footer=None
        )
        expected_commit_without_scope = Commit(
            id='597ec5676235e18f5a607726603df944da5be7fe',
            author='Nicolas Gouzy <nicolas.gouzy@orange.com>',
            date=datetools.str2date('2017-03-22 15:28:45 +0100'),
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


# Tools

def data_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'data', filename)
