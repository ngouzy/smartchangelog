import re
from datetime import datetime

from typing import NamedTuple, cast

from smartchangelog import datetools
from smartchangelog.commitmsg import CommitType, CommitMsg, CommitSyntaxError


class _Commit(NamedTuple):
    id: str
    author: str
    date: datetime
    type: CommitType = None
    scope: str = None
    subject: str = None
    body: str = None


class Commit(_Commit):
    class Message(NamedTuple):
        type: CommitType = None
        scope: str = None
        subject: str = None
        body: str = None

    @classmethod
    def parse(cls, commit: str) -> 'Commit':
        m = re.match('commit (?P<id>[a-z0-9]{40})(?:\n|.)+Author: (?P<author>.*)(?:\n|.)+'
                     'Date: (?P<date>.*)(?P<message>(.|\n)*)',
                     commit)
        gd = m.groupdict()
        message = cls.parse_message(gd['message'])
        commit_id = gd['id']
        author = gd['author']
        date = datetools.str2date(gd['date'].strip())
        return cls(
            id=commit_id,
            author=author,
            date=date,
            type=message.type,
            scope=message.scope,
            subject=message.subject,
            body=message.body
        )

    @classmethod
    def strip_lines(cls, string) -> str:
        return "\n".join(line.strip() for line in string.strip(' \n').split('\n'))

    @classmethod
    def parse_message(cls, message: str) -> Message:
        message = cls.strip_lines(message)
        try:
            cm = CommitMsg.parse(message)
            return cls.Message(**cm.__dict__)
        except CommitSyntaxError:
            message = re.sub("\n+", "\n", message)
            lines = message.split('\n', maxsplit=1)
            subject = lines[0] or None
            body = None
            if len(lines) > 1:
                body = lines[1] or None
            return cls.Message(
                type=None,
                scope=None,
                subject=subject,
                body=body
            )

    @classmethod
    def property_name(cls, prop: property) -> str:
        # fixme: change implementation, use _Commit.__dict__
        i = int(prop.__doc__.split(' ')[-1])
        return tuple(cls._fields)[i]

    @classmethod
    def property(cls, name: str):
        prop = cast(property, _Commit.__dict__[name])
        return prop
