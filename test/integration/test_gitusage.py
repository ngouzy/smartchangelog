import os
import shutil
import tempfile

import pytest

from test.support import commitmsg_script_path, git_command


# noinspection PyShadowingNames
@pytest.fixture(scope='function')
def temp_dir():
    temporary_directory = tempfile.mkdtemp()
    sample_file_path = os.path.join(temporary_directory, "sample_file.txt")
    with open(sample_file_path, mode="w") as sample_file:
        sample_file.write("sample content")
    old_cwd = os.getcwd()
    os.chdir(temporary_directory)

    git_command('init')
    git_command('config', 'user.name', 'Nicolas Gouzy')
    git_command('config', 'user.email', 'nicolas.gouzy@gmail.com')

    git_hook_commit_msg_path = os.path.join(temporary_directory, ".git", "hooks", "commit-msg")
    shutil.copy(commitmsg_script_path, git_hook_commit_msg_path)
    assert os.path.isfile(git_hook_commit_msg_path)

    os.chmod(git_hook_commit_msg_path, 0o755)

    git_command('add', '.')

    yield None

    os.chdir(old_cwd)


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_right_msg():
    git_command('commit', '-m', 'feat(ui): sample')


@pytest.mark.usefixtures("temp_dir")
def test_git_commit_with_wrong_msg():
    with pytest.raises(AssertionError):
        git_command('commit', '-m', 'wrong commit message')
