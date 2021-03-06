import pytest

import smartchangelog.scripts.commitmsg_script
from smartchangelog.tools import set_args, set_commit_editmsg, commitmsg_script_path
from smartchangelog import githook
# noinspection PyUnresolvedReferences
from tests.integration import temp_dir


def test_help_arg():
    # GIVEN
    with set_args(commitmsg_script_path, "-h"), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    # THEN
    assert e.value.code == 0


def test_right_msg_arg():
    # GIVEN
    with set_args(commitmsg_script_path, 'feat(ui): add button'), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    # THEN
    assert e.value.code == 0


def test_wrong_msg_arg():
    # GIVEN
    with set_args(commitmsg_script_path, 'wrong commit message'), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    # THEN
    assert e.value.code != 0


def test_right_msg_file():
    # GIVEN
    with set_commit_editmsg('feat(ui): add button') as f, \
         set_args(commitmsg_script_path, f.name), \
         pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    # THEN
    assert e.value.code == 0


def test_wrong_msg_file():
        # GIVEN
        with set_commit_editmsg('bad format') as f, \
             set_args(commitmsg_script_path, f.name), \
             pytest.raises(SystemExit) as e:
            # WHEN
            smartchangelog.scripts.commitmsg_script.main()
        # THEN
        assert e.value.code != 0


def test_version_arg():
    # GIVEN
    expected_version = smartchangelog.__version__
    with set_args(commitmsg_script_path, "--version") as result, pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    stdout, stderr = result
    version = stdout.read().strip("\n")
    # THEN
    assert e.value.code == 0
    assert version == expected_version


@pytest.mark.usefixtures("temp_dir")
def test_install_arg():
    # GIVEN
    with set_args(commitmsg_script_path, "-i") as result, pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    stdout, stderr = result
    install_msg = stdout.read().strip("\n")
    # THEN
    assert e.value.code == 0
    assert install_msg == 'commit-msg hook installed in .git/hooks/commit-msg'


@pytest.mark.usefixtures("temp_dir")
def test_uninstall_arg():
    # GIVEN
    githook.install()
    with set_args(commitmsg_script_path, "-u") as result, pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg_script.main()
    stdout, stderr = result
    uninstall_msg = stdout.read().strip("\n")
    # THEN
    assert e.value.code == 0
    assert uninstall_msg == 'commit-msg hook removed from .git/hooks/commit-msg'



