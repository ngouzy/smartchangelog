import os
import pytest

from smartchangelog.gitcmd import GitCmdError, is_inside_work_tree, get_gitdir
from tests.unit import data_dir_path


@pytest.fixture(scope='function')
def cmd():
    old_cmd = os.getcwd()
    yield None
    os.chdir(old_cmd)


@pytest.mark.usefixtures('cmd')
def test_is_inside_work_tree_ok():
    # GIVEN
    os.chdir(data_dir_path())
    # WHEN
    result = is_inside_work_tree()
    # THEN
    assert result


@pytest.mark.usefixtures('cmd')
def test_is_inside_work_tree_ko():
    # GIVEN
    os.chdir(os.path.expanduser('~'))
    # WHEN
    result = is_inside_work_tree()
    # THEN
    assert not result


@pytest.mark.usefixtures('cmd')
def test_get_gitdir_ok():
    # GIVEN
    os.chdir(data_dir_path())
    # WHEN
    gitdir_path = get_gitdir()
    # THEN
    assert os.path.split(gitdir_path)[-1] == '.git'


@pytest.mark.usefixtures('cmd')
def test_get_gitdir_ko():
    # GIVEN
    os.chdir(os.path.expanduser('~'))
    # WHEN
    with pytest.raises(GitCmdError):
        get_gitdir()
        # THEN
        pass


