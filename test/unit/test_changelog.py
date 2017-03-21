from changelog import parse, Commit, DateUtil
from datetime import datetime, timezone, timedelta


class TestParse:
    def test_parser(self):
        # GIVEN
        with open('data/big.log', encoding='utf-8') as logfile:
            log = logfile.read()
        # WHEN
        commits = parse(log)
        # THEN
        assert (len(commits) == 107)


class TestCommit:
    def test_parse(self):
        # GIVEN
        with open('data/one.log', encoding='utf-8') as logfile:
            log = logfile.read()
        expected = Commit(commit_id='2d6b8b7d11cea43bab36da37afdca3c300f92333',
                          author='Vincent Boesch <vincent.boesch@orange.com>',
                          date=DateUtil.str2date('2017-03-21 14:45:48 +0100'),
                          message="feat(conso): OEM-372\nadd field for nbAlerts")
        # WHEN
        commit = Commit.parse(log)
        # THEN
        assert commit == expected


class TestDateUtil:
    def test_str2date(self):
        # GIVEN
        expected = datetime(year=2017, month=3, day=21, hour=16, minute=9, second=13,
                            tzinfo=timezone(timedelta(hours=1)))
        string = '2017-03-21 16:09:13 +0100'
        # WHEN
        date = DateUtil.str2date(string)
        # THEN
        assert date == expected

    def test_date2str(self):
        # GIVEN
        expected = '2017-03-21 16:09:13 +0100'
        dt = datetime(year=2017, month=3, day=21, hour=16, minute=9, second=13,
                      tzinfo=timezone(timedelta(hours=1)))
        # WHEN
        string = DateUtil.date2str(dt)
        # THEN
        assert string == expected
