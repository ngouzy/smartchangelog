import sys
import os

from . import *


@pytest.fixture(scope='function')
def sys_argv():
    old_sys_argv = sys.argv
    yield
    sys.argv = old_sys_argv


@pytest.fixture(scope='function')
def commit_msg_file(filename):
    yield


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_help_arg(commitmsg_script, capsys):
    # GIVEN
    sys.argv = [commitmsg_script, "-h"]
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    # THEN
    assert e.value.code == 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_right_msg_arg(commitmsg_script, capsys):
    # GIVEN
    sys.argv = [commitmsg_script, 'feat(ui): add button']
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    # THEN
    assert e.value.code == 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_wrong_msg_arg(commitmsg_script, capsys):
    # GIVEN
    sys.argv = [commitmsg_script, 'wrong commit message']
    # WHEN
    with pytest.raises(SystemExit) as e:
        commitmsg.main()
    capsys.readouterr()
    assert e.value.code != 0


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sys_argv")
def test_right_msg_file(commitmsg_script, capsys):
    # GIVEN
    filename = 'COMMIT_EDITMSG'
    sys.argv = [commitmsg_script, filename]
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
def test_wrong_msg_file(commitmsg_script, capsys):
    # GIVEN
    filename = 'COMMIT_EDITMSG'
    sys.argv = [commitmsg_script, filename]
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
