import re
from collections import Iterable
from io import StringIO
from itertools import groupby

from typing import List, Tuple, Callable, Any, IO, cast

from smartchangelog import datetools
from smartchangelog.commit import Commit


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
        print("    * date: {date}".format(date=datetools.date2str(commit.date)), file=file)
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









