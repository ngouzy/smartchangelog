import inspect
import re
from enum import Enum

from typing import NamedTuple


class CommitSyntaxError(Exception):
    """
    Invalid commit syntax error
    """


class CommitType(Enum):
    feat = 'new feature for the user, not a new feature for build script'
    fix = 'bug fix for the user, not a fix to a build script'
    docs = 'changes to the documentation'
    style = 'formatting, missing semi colons, etc; no production code change'
    refactor = 'refactoring production code, eg.renaming a variable'
    test = 'adding missing tests, refactoring tests; no production code change'
    chore = 'updating gradle scripts, continuous integration scripts,  etc; no production code change'

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.index() < other.index()
        return NotImplemented

    def index(self):
        return [ct for ct in CommitType].index(self)

    def __str__(self):
        return self.name


class FirstLine(NamedTuple):
    type: CommitType
    scope: str
    subject: str


class CommitMsg:
    """
    Your commit message have to follow this format:
    <type>(<scope>): <subject>

    <body>

    <footer>
    Where :
    Message first line (type, scope and subject)
        The first line cannot be longer than {firstline_max_length} characters.
        The type and scope should always be lowercase as shown
        below.
        Allowed <type> values: {allowed_types}
        Example <scope> values:
            * ui
            * business
            * model
            * widget
            * config
            etc.
        The <scope> can be empty (e.g. if the change is a global or difficult
        to assign to a single component), in which case the parentheses are
        omitted.

    Message body (optional)
        If there is a body, it must have a blank line between the first line and
        the body.
        The body cannot be longer than {bodyline_max_length} characters.
        uses the imperative, present tense: "change" not "changed" nor
        "changes"
        includes motivation for the change and contrasts with previous behavior

    Message footer
        Referencing issues or user stories (Jira references)
        If there is a footer, it must have a body and it must have a blank line between the body and
        the footer.
        The footer cannot be longer than {footerline_max_length} characters.
    """
    FIRSTLINE_PATTERN = re.compile('^([a-z]+)(?:\(([^\n\t]+)\))?: (.+)$')
    FIRSTLINE_MAX_LENGTH = 70
    BODY_MAX_LENGTH = 80
    FOOTER_MAX_LENGTH = 80

    def __init__(self, msg_type: CommitType, scope: str, subject: str, body: str = None, footer: str = None) -> None:
        self.type = msg_type
        self.scope = scope
        self.subject = subject
        self.body = body
        self.footer = footer

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    @classmethod
    def parse(cls, msg: str) -> 'CommitMsg':
        msg_parts = msg.split("\n\n")
        firstline = cls.parse_firstline(msg_parts[0])
        if len(msg_parts) > 1:
            body = msg_parts[1]
            cls.parse_body(body)
        else:
            body = None
        if len(msg_parts) > 2:
            footer = msg_parts[2]
            cls.parse_footer(footer)
        else:
            footer = None
        return cls(firstline.type, firstline.scope, firstline.subject, body, footer)

    @classmethod
    def parse_firstline(cls, firstline: str) -> FirstLine:
        if len(firstline) > cls.FIRSTLINE_MAX_LENGTH:
            raise CommitSyntaxError("First line can not be greater than {length} characters".format(
                length=cls.FIRSTLINE_MAX_LENGTH))
        result = cls.FIRSTLINE_PATTERN.search(firstline)
        if "\n" in firstline.strip():
            raise CommitSyntaxError("Two blank lines have to separate the first line and body part")
        if result is None:
            raise CommitSyntaxError("{firstline} doesn't follow the first line commit message pattern: {pattern}"
                                    .format(firstline=firstline, pattern=cls.FIRSTLINE_PATTERN.pattern))
        commit_type_str, scope, subject = result.groups()
        try:
            commit_type = CommitType[commit_type_str]
        except KeyError:
            raise CommitSyntaxError("{commit_type} is not an available commit type".format(commit_type=commit_type_str))
        return FirstLine(type=commit_type, scope=scope, subject=subject)

    @classmethod
    def parse_body(cls, body: str) -> str:
        for line in body.split('\n'):
            if len(line) > cls.BODY_MAX_LENGTH:
                raise CommitSyntaxError("Body line can not be greater than {length} characters".format(
                    length=cls.BODY_MAX_LENGTH))
        return body

    @classmethod
    def parse_footer(cls, footer: str) -> str:
        for line in footer.split('\n'):
            if len(line) > cls.FOOTER_MAX_LENGTH:
                raise CommitSyntaxError("Footer line can not be greater than {length} characters".format(
                    length=cls.FOOTER_MAX_LENGTH))
        return footer

    @classmethod
    def format_allowed_types(cls) -> str:
        return "\n" + "\n".join("\t* {name}: {doc}".format(name=ct.name, doc=ct.value) for ct in CommitType)

    @classmethod
    def help(cls) -> str:
        return inspect.getdoc(cls).format(allowed_types=cls.format_allowed_types(),
                                          firstline_max_length=cls.FIRSTLINE_MAX_LENGTH,
                                          bodyline_max_length=cls.BODY_MAX_LENGTH,
                                          footerline_max_length=cls.FOOTER_MAX_LENGTH)

