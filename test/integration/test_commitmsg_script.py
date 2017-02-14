import subprocess

from . import *


# noinspection PyShadowingNames
def test_help_arg(commitmsg_script):
    # GIVEN
    # WHEN
    completed_process = subprocess.run([commitmsg_script, '-h'],
                                       stdout=subprocess.PIPE,
                                       encoding="utf-8")
    # THEN
    expected = commitmsg.CommitMsg.help().replace(" ", "")
    actual = completed_process.stdout.replace(" ", "")
    assert expected in actual


# noinspection PyShadowingNames
def test_right_msg_arg(commitmsg_script):
    # GIVEN
    # WHEN
    completed_process = subprocess.run([commitmsg_script, 'feat(ui): add button'],
                                       stderr=subprocess.PIPE,
                                       encoding="utf-8")
    # THEN
    assert completed_process.returncode == 0
    assert len(completed_process.stderr) == 0


# noinspection PyShadowingNames
def test_wrong_msg_arg(commitmsg_script):
    # GIVEN
    # WHEN
    completed_process = subprocess.run([commitmsg_script, 'wrong commit message'],
                                       stderr=subprocess.PIPE,
                                       encoding="utf-8")
    # THEN
    assert completed_process.returncode != 0
    expected = commitmsg.CommitMsg.help().replace(" ", "")
    actual = completed_process.stderr.replace(" ", "")
    assert expected in actual
