import re
from datetime import datetime
from typing import List, Tuple, NamedTuple
from itertools import groupby
from collections import Iterable
from io import StringIO

from commitmsg import CommitMsg, CommitSyntaxError, CommitType


class DateUtil:
    date_format = "%Y-%m-%d %H:%M:%S %z"

    @classmethod
    def str2date(cls, string: str) -> datetime:
        return datetime.strptime(string, cls.date_format)

    @classmethod
    def date2str(cls, dt: datetime) -> str:
        return dt.strftime(cls.date_format)


class _Commit(NamedTuple):
    commit_id: str
    author: str
    date: datetime
    type: CommitType
    scope: str
    subject: str
    body: str
    footer: str


class Commit(_Commit):
    class Message(NamedTuple):
        type: CommitType
        scope: str
        subject: str
        body: str
        footer: str

    @classmethod
    def parse(cls, commit: str) -> 'Commit':
        m = re.match('commit (?P<commit_id>[a-z0-9]{40})(?:\n|.)+Author: (?P<author>.*)(?:\n|.)+'
                     'Date: (?P<date>.*)(?P<message>(.|\n)*)',
                     commit)
        gd = m.groupdict()
        message = cls.parse_message(gd['message'])
        commit_id = gd['commit_id']
        author = gd['author']
        date = DateUtil.str2date(gd['date'].strip())
        return cls(
            commit_id=commit_id,
            author=author,
            date=date,
            type=message.type,
            scope=message.scope,
            subject=message.subject,
            body=message.body,
            footer=message.footer
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
                body=body,
                footer=None
            )


class Changelog(List[Commit]):
    @classmethod
    def parse(cls, log: str) -> 'Changelog':
        raw_commits = re.findall('(commit [a-z0-9]{40}\n(?:.|\n)*?)(?=commit|$)', log)
        return Changelog([Commit.parse(rc) for rc in raw_commits])

    def groupby(self, *criteria: Tuple[property]):
        if len(criteria) == 0:
            self.sort(key=Commit.date.fget)
            return self
        criteria_list: List[property] = list(criteria)
        criterion = criteria_list.pop(0)
        # Filter
        categorized_changelog = Changelog([commit for commit in self if criterion.fget(commit) is not None])
        uncategorized_commits = [commit for commit in self if criterion.fget(commit) is None]
        # Sort
        categorized_changelog.sort(key=criterion.fget)
        # Arrange
        result = self.groupby_to_list(groupby(categorized_changelog, criterion.fget))
        for item in result:
            cl = Changelog(item[1])
            item[1] = cl.groupby(*criteria_list)
        if len(uncategorized_commits) > 0:
            result.append(["unknown", uncategorized_commits])
        return result

    @classmethod
    def groupby_to_list(cls, iterable: Iterable):
        return [[key, [i for i in group]] for key, group in iterable]

    def pretty(self):
        with StringIO() as report:
            for item in self.groupby(Commit.type, Commit.scope):
                commit_type = item[0]
                group = item[1]
                if isinstance(commit_type, CommitType):
                    print("# type: {type}".format(type=commit_type.name), file=report)
                    print("", file=report)
                    for subitem in group:
                        scope = subitem[0]
                        subgroup = subitem[1]
                        print("## scope: {scope}".format(scope=scope), file=report)
                        print("", file=report)
                        for commit in subgroup:
                            print("* subject: {subject}".format(subject=commit.subject or ''), file=report)
                            print("    * body: {body}".format(body=commit.body or ''), file=report)
                            print("    * footer: {footer}".format(footer=commit.footer or ''), file=report)
                            print("    * date: {date}".format(date=DateUtil.date2str(commit.date)), file=report)
                            print("    * author: {author}".format(author=commit.author), file=report)
                        print("", file=report)
                else:
                    print("# type: {type}".format(type=commit_type), file=report)
                    print("", file=report)
                    for commit in group:
                        print("* subject: {subject}".format(subject=commit.subject), file=report)
                        print("    * body: {body}".format(body=commit.body or ''), file=report)
                        print("    * date: {date}".format(date=DateUtil.date2str(commit.date)), file=report)
                        print("    * author: {author}".format(author=commit.author), file=report)
                print("", file=report)
            return report.getvalue()











