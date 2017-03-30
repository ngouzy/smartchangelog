import os
import pytest

from smartchangelog.gitcmd import is_inside_work_tree
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
    path = os.getcwd()
    # WHEN
    result = is_inside_work_tree()
    # THEN
    assert not result


