import os
import shutil
import tempfile

import pytest

from smartchangelog import githook
from smartchangelog.gitcmd import git_command, GitCmdError
# noinspection PyUnresolvedReferences
from tests.integration import temp_dir


@pytest.fixture(scope='function')
def add_sample_file(temp_dir):
    temporary_directory = temp_dir
    githook.install()

    sample_file_path = os.path.join(temporary_directory, "sample_file.txt")
    with open(sample_file_path, mode="w") as sample_file:
        sample_file.write("sample content")

    git_command('add', '.')

    yield None


@pytest.mark.usefixtures("add_sample_file")
def test_git_commit_with_right_msg():
    # GIVEN
    # WHEN
    result = git_command('commit', '-m', 'feat(ui): sample')
    # THEN
    assert result


@pytest.mark.usefixtures("add_sample_file")
def test_git_commit_with_wrong_msg():
    # GIVEN
    # WHEN
    with pytest.raises(GitCmdError):
        git_command('commit', '-m', 'wrong commit message')
        # THEN
        pass
