import os
import shutil
import subprocess
import tempfile
from typing import List

from . import *


def git_command(*git_args: List) -> subprocess.CompletedProcess:
    args = ['git'] + list(git_args)
    completed_process = subprocess.run(args,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       encoding="utf-8")
    return completed_process


# noinspection PyShadowingNames
@pytest.fixture(scope='function')
def temp_dir(commitmsg_script):
    temporary_directory = tempfile.mkdtemp()
    with open(file=os.path.join(temporary_directory, "sample_file.txt"), mode="w") as sample_file:
        sample_file.write("sample content")
    old_cwd = os.getcwd()
    os.chdir(temporary_directory)

    completed_process = git_command('init')
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0

    completed_process = git_command('config', 'user.name', 'Nicolas Gouzy')
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0

    git_hook_commit_msg_path = os.path.join(temporary_directory, ".git", "hooks", "commit-msg")
    shutil.copy(commitmsg_script, git_hook_commit_msg_path)
    completed_process = git_command('add', '.')
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0

    yield None

    os.chdir(old_cwd)


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_right_msg():
    completed_process = git_command('commit', '-m', 'feat(ui): sample')
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_wrong_msg():
    completed_process = git_command('commit', '-m', 'wrong commit message')
    assert completed_process.returncode != 0
    assert len(completed_process.stderr) > 0
