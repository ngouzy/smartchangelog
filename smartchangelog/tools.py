import inspect
import os
import sys
from contextlib import contextmanager
from io import StringIO

from typing import Iterator, TextIO, cast

from smartchangelog.scripts import commitmsg_script

"""Path of the file containing commitmsg_script.py file"""
commitmsg_script_path = inspect.getfile(commitmsg_script)


@contextmanager
def set_commit_editmsg(msg: str) -> Iterator[TextIO]:
    filename = 'COMMIT_EDITMSG'
    with open(filename, mode='w') as f:
        f.write(msg)
    try:
        yield cast(TextIO, f)
    finally:
        if os.path.isfile(filename):
            os.remove(filename)


@contextmanager
def set_args(*args):
    old = list(sys.argv)
    sys.argv[:] = args
    oldout, olderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        sys.argv[:] = old
        sys.stdout, sys.stderr = oldout, olderr
