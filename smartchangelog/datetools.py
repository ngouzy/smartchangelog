from datetime import datetime

date_format = "%Y-%m-%d %H:%M:%S %z"


def str2date(string: str) -> datetime:
    return datetime.strptime(string, date_format)


def date2str(dt: datetime) -> str:
    return dt.strftime(date_format)