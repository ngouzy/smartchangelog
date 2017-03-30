import subprocess
import os

from typing import cast, List


class GitCmdError(Exception):
    """
    Git command error
    """


def git_command(*git_args: str) -> str:
    args = ['git'] + cast(List[str], list(git_args))
    cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode == 0 and len(cp.stderr) == 0:
        return cp.stdout.decode('utf-8').strip('\n')
    else:
        raise GitCmdError(cp.stderr.decode('utf-8').strip('\n'))


def is_inside_work_tree() -> bool:
    try:
        result = git_command('rev-parse', '--is-inside-work-tree')
        return result == 'true'
    except GitCmdError:
        return False


def get_gitdir() -> str:
    if is_inside_work_tree():
        path = os.path.join(git_command('rev-parse', '--show-toplevel'), '.git')
        return os.path.abspath(path)
    else:
        raise GitCmdError("You have to be inside a git work tree")


def log(revision_range: str) -> str:
    return git_command("log", revision_range, "--date", "iso")
