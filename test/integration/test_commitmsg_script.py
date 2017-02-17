import sys
import os

import pytest

import commitmsg
from test.support import commitmsg_script_path


@pytest.fixture(scope='function')
def sys_argv():
    old_sys_argv = sys.argv
    yield
    sys.argv = old_sys_argv


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_help_arg(capsys):
    # GIVEN
    sys.argv = [commitmsg_script_path, "-h"]
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    # THEN
    assert e.value.code == 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_right_msg_arg(capsys):
    # GIVEN
    sys.argv = [commitmsg_script_path, 'feat(ui): add button']
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    # THEN
    assert e.value.code == 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_wrong_msg_arg(capsys):
    # GIVEN
    sys.argv = [commitmsg_script_path, 'wrong commit message']
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    assert e.value.code != 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_right_msg_file(capsys):
    # GIVEN
    filename = 'COMMIT_EDITMSG'
    sys.argv = [commitmsg_script_path, filename]
    with open(filename, 'w') as f:
        f.write('feat(ui): add button')
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    # THEN
    assert e.value.code == 0
    # CLEAN
    capsys.readouterr()
    if os.path.isfile(filename):
        os.remove(filename)


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_wrong_msg_file(capsys):
    # GIVEN
    filename = 'COMMIT_EDITMSG'
    sys.argv = [commitmsg_script_path, filename]
    with open(filename, 'w') as f:
        f.write('bad format')
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    # THEN
    assert e.value.code != 0
    # CLEAN
    capsys.readouterr()
    if os.path.isfile(filename):
        os.remove(filename)
