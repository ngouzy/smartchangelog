import re
from datetime import datetime
from typing import List, Tuple, NamedTuple, Callable, Any, IO, cast
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
    id: str
    author: str
    date: datetime
    type: CommitType = None
    scope: str = None
    subject: str = None
    body: str = None
    footer: str = None


class Commit(_Commit):
    class Message(NamedTuple):
        type: CommitType = None
        scope: str = None
        subject: str = None
        body: str = None
        footer: str = None

    @classmethod
    def parse(cls, commit: str) -> 'Commit':
        m = re.match('commit (?P<id>[a-z0-9]{40})(?:\n|.)+Author: (?P<author>.*)(?:\n|.)+'
                     'Date: (?P<date>.*)(?P<message>(.|\n)*)',
                     commit)
        gd = m.groupdict()
        message = cls.parse_message(gd['message'])
        commit_id = gd['id']
        author = gd['author']
        date = DateUtil.str2date(gd['date'].strip())
        return cls(
            id=commit_id,
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

    @classmethod
    def property_name(cls, prop: property) -> str:
        i = int(x=prop.__doc__.split(' ')[-1])
        return tuple(cls._fields)[i]


class Node:
    def __init__(self, name: str = None, criterion: property = None, children: Tuple['Node'] = None,
                 value: Commit = None) -> None:
        self._parent: 'Node' = None
        self.name = name
        self.criterion = criterion
        self._children: Tuple['Node'] = None
        self.children = children
        self.value = value

    @property
    def parent(self) -> 'Node':
        return self._parent

    @property
    def children(self) -> Tuple['Node']:
        return self._children

    @children.setter
    def children(self, children: Tuple['Node']) -> None:
        if children is not None:
            for node in children:
                node._parent = self
        self._children = children

    def depth_level(self) -> int:
        if self.parent is None:
            return 0
        else:
            return self.parent.depth_level() + 1

    def __len__(self):
        if not self.children:
            return 1
        nb_children = 0
        for child in self.children:
            nb_children += len(child)
        return nb_children

    @classmethod
    def print_multilines(cls, name: str, value: str, file: IO):
        if value:
            lines = value.split('\n')
            if len(lines) == 1:
                print("    * {name}: {value}".format(name=name, value=value), file=file)
            else:
                print("    * {name}:".format(name=name), file=file)
                for line in lines:
                    print("        - {line}".format(line=line), file=file)

    @classmethod
    def print_leaf(cls, commit: Commit, file: IO) -> None:
        print("* subject: {subject}".format(subject=commit.subject or ''), file=file)
        cls.print_multilines(name='body', value=commit.body, file=file)
        cls.print_multilines(name='footer', value=commit.footer, file=file)
        print("    * date: {date}".format(date=DateUtil.date2str(commit.date)), file=file)
        print("    * author: {author}".format(author=commit.author), file=file)
        print("    * commit: {id}".format(id=commit.id), file=file)

    def print_header(self, node: 'Node', file: IO):
        print(
            "{header} {criterion_name}: {name}".format(
                header="#" * (self.depth_level() + 1),
                criterion_name=Commit.property_name(node.criterion),
                name=node.name
            ),
            file=file
        )
        print(file=file)

    def report(self) -> str:
        sio = StringIO()
        with sio:
            if self.children is None:
                self.print_leaf(commit=self.value, file=sio)
            else:
                for node in self.children:
                    if node.name:
                        self.print_header(node=node, file=sio)
                    print(node.report().strip('\n'), file=sio)
                    print(file=sio)
            string = sio.getvalue()
            return string


class Changelog(List[Commit]):
    @classmethod
    def parse(cls, log: str) -> 'Changelog':
        raw_commits = re.findall('(commit [a-z0-9]{40}\n(?:.|\n)*?)(?=commit [a-z0-9]{40}|$)', log)
        return Changelog([Commit.parse(rc) for rc in raw_commits])

    def groupby(self, *criteria: property) -> Node:
        if len(criteria) == 0:
            # Sort
            date_prop = cast(property, Commit.date)
            date_getter = cast(Callable[[Commit], Any], date_prop.fget)
            self.sort(key=date_getter)
            return self.node()

        criteria_list = list(criteria)
        criterion = criteria_list.pop(0)
        criterion_getter = cast(Callable[[Commit], Any], criterion.fget)

        # Filter
        # noinspection PyTypeChecker
        categorized_changelog = Changelog([commit for commit in self if criterion_getter(commit) is not None])
        # noinspection PyTypeChecker
        uncategorized_commits = Changelog([commit for commit in self if criterion_getter(commit) is None])

        # Sort
        categorized_changelog.sort(key=criterion_getter)

        # Arrange
        raw_result = self.groupby_to_list(groupby(iterable=categorized_changelog, key=criterion_getter))
        children_list: List[Node] = []
        for key, group in raw_result:
            cl = Changelog(group)
            children_list.append(Node(name=str(key), criterion=criterion, children=cl.groupby(*criteria_list).children))
        if len(uncategorized_commits) > 0:
            children_list.append(uncategorized_commits.node(name="unknown", criterion=criterion))
        children = cast(Tuple[Node], tuple(children_list))

        return Node(children=children)

    def node(self, name: str=None, criterion: property=None) -> Node:
        # noinspection PyTypeChecker
        children = cast(Tuple[Node], tuple(Node(value=commit) for commit in self))
        return Node(name=name, criterion=criterion, children=children)

    @classmethod
    def groupby_to_list(cls, iterable: Iterable):
        return [[key, [i for i in group]] for key, group in iterable]









