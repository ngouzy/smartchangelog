from smartchangelog import datetools
from smartchangelog.commit import Commit
from smartchangelog.commitmsg import CommitType
from tests.unit import data_file_path


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