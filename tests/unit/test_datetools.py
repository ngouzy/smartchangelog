from datetime import datetime, timezone, timedelta

from smartchangelog import datetools


def test_str2date():
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
    date = datetools.str2date(string)
    # THEN
    assert date == expected


def test_date2str():
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
    string = datetools.date2str(dt)
    # THEN
    assert string == expected
