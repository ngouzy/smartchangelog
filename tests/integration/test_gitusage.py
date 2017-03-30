import os
import tempfile

import pytest

from smartchangelog import githook
from smartchangelog.gitcmd import git_command, GitCmdError


@pytest.fixture(scope='function')
def temp_dir():
    temporary_directory = tempfile.mkdtemp()
    old_cwd = os.getcwd()
    os.chdir(temporary_directory)

    git_command('init')
    git_command('config', 'user.name', 'Nicolas Gouzy')
    git_command('config', 'user.email', 'nicolas.gouzy@gmail.com')

    githook.install()

    sample_file_path = os.path.join(temporary_directory, "sample_file.txt")
    with open(sample_file_path, mode="w") as sample_file:
        sample_file.write("sample content")

    git_command('add', '.')

    yield None

    os.chdir(old_cwd)


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_right_msg():
    # GIVEN
    # WHEN
    result = git_command('commit', '-m', 'feat(ui): sample')
    # THEN
    assert result


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_wrong_msg():
    # GIVEN
    # WHEN
    with pytest.raises(GitCmdError):
        git_command('commit', '-m', 'wrong commit message')
        # THEN
        pass


