import inspect
import subprocess
from typing import List

import commitmsg


"""Path of the file containing commitmsg module"""
commitmsg_script_path = inspect.getfile(commitmsg)


def git_command(*git_args: List[str]) -> subprocess.CompletedProcess:
    args = ['git'] + list(git_args)
    completed_process = subprocess.run(args,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       encoding="utf-8")
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0
    return completed_process
