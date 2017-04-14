import os
import shutil
import tempfile

import pytest

from smartchangelog.gitcmd import git_command


@pytest.fixture(scope='function')
def temp_dir():
    temporary_directory = tempfile.mkdtemp()
    old_cwd = os.getcwd()
    os.chdir(temporary_directory)

    git_command('init')
    git_command('config', 'user.name', 'Nicolas Gouzy')
    git_command('config', 'user.email', 'nicolas.gouzy@gmail.com')

    yield temporary_directory

    os.chdir(old_cwd)
    shutil.rmtree(temporary_directory)


def hook_path():
    return os.path.join(os.getcwd(), '.git', 'hooks')