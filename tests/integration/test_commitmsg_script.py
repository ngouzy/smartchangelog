import pytest

import smartchangelog.scripts.commitmsg
from smartchangelog.tools import set_args, set_commit_editmsg, commitmsg_script_path


def test_help_arg():
    # GIVEN
    with set_args(commitmsg_script_path, "-h"), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg.main()
    # THEN
    assert e.value.code == 0


def test_right_msg_arg():
    # GIVEN
    with set_args(commitmsg_script_path, 'feat(ui): add button'), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg.main()
    # THEN
    assert e.value.code == 0


def test_wrong_msg_arg():
    # GIVEN
    with set_args(commitmsg_script_path, 'wrong commit message'), pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg.main()
    # THEN
    assert e.value.code != 0


def test_right_msg_file():
    # GIVEN
    with set_commit_editmsg('feat(ui): add button') as f, \
         set_args(commitmsg_script_path, f.name), \
         pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg.main()
    # THEN
    assert e.value.code == 0


def test_wrong_msg_file():
        # GIVEN
        with set_commit_editmsg('bad format') as f, \
             set_args(commitmsg_script_path, f.name), \
             pytest.raises(SystemExit) as e:
            # WHEN
            smartchangelog.scripts.commitmsg.main()
        # THEN
        assert e.value.code != 0


def test_version_arg():
    # GIVEN
    expected_version = smartchangelog.__version__
    with set_args(commitmsg_script_path, "--version") as result, pytest.raises(SystemExit) as e:
        # WHEN
        smartchangelog.scripts.commitmsg.main()
    stdout, stderr = result
    version = stdout.read().strip("\n")
    # THEN
    assert e.value.code == 0
    assert version == expected_version

