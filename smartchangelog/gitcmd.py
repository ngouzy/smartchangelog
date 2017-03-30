import subprocess

from typing import cast, List


def git_command(*git_args: str) -> subprocess.CompletedProcess:
    args = ['git'] + cast(List[str], list(git_args))
    completed_process = subprocess.run(args,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    return completed_process


def is_inside_work_tree() -> bool:
    completed_process = git_command('rev-parse', '--is-inside-work-tree')
    if completed_process.returncode == 0 and len(completed_process.stderr) == 0:
        if completed_process.stdout.decode('utf-8').strip('\n') == 'true':
            return True
    return False
