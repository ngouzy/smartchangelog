import re
from datetime import datetime
from typing import List


class DateUtil:
    date_format = "%Y-%m-%d %H:%M:%S %z"

    @classmethod
    def str2date(cls, string: str) -> datetime:
        return datetime.strptime(string, cls.date_format)

    @classmethod
    def date2str(cls, dt: datetime) -> str:
        return dt.strftime(cls.date_format)


class Commit:
    def __init__(self, commit_id: str, author: str, date: datetime, message: str) -> None:
        self.commit_id = commit_id
        self.author = author
        self.date = date
        self.message = message

    @classmethod
    def parse(cls, commit: str) -> 'Commit':
        m = re.match('commit (?P<commit_id>[a-z0-9]{40})(?:\n|.)+Author: (?P<author>.*)(?:\n|.)+'
                     'Date: (?P<date>.*)(?P<message>(.|\n)*)',
                     commit)
        gd = m.groupdict()
        message = "\n".join(line.strip() for line in gd['message'].split('\n'))
        return Commit(commit_id=gd['commit_id'],
                      author=gd['author'],
                      date=DateUtil.str2date(gd['date'].strip()),
                      message=message.strip('\n'))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented


def parse(log: str) -> List[str]:
    return re.findall('(commit [a-z0-9]{40}\n(?:.|\n)*?)(?=commit|$)', log)
