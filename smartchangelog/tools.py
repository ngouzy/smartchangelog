import inspect
import os
import subprocess
import sys
from contextlib import contextmanager
from io import StringIO

from typing import List, Iterator, TextIO, cast

from smartchangelog.scripts import commitmsg_script

"""Path of the file containing commitmsg module"""
commitmsg_script_path = inspect.getfile(commitmsg_script)


def git_command(*git_args: str) -> subprocess.CompletedProcess:
    args = ['git'] + cast(List[str], list(git_args))
    completed_process = subprocess.run(args,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0
    return completed_process


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
