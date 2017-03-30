import inspect

import pytest

import smartchangelog
from smartchangelog.scripts import changelog_script
from smartchangelog.tools import set_args

"""Path of the file containing changelog_script.py file"""
changelog_script_path = inspect.getfile(changelog_script)


def test_range_arg():
    # GIVEN
    with set_args(changelog_script_path, '--range', '0.0.1..0.0.8') as result, \
            pytest.raises(
            SystemExit) as e:
        # WHEN
        changelog_script.main()
    stdout, stderr = result
    printed_report = stdout.read()
    # THEN
    assert e.value.code == 0
    assert printed_report


def test_range_arg_with_groupby():
    # GIVEN
    with set_args(changelog_script_path, '--range', '0.0.1..0.0.8', '--groupby', 'type', 'scope') as result, \
            pytest.raises(
            SystemExit) as e:
        # WHEN
        changelog_script.main()
    stdout, stderr = result
    printed_report = stdout.read()
    # THEN
    assert e.value.code == 0
    assert printed_report


def test_version_arg():
    # GIVEN
    expected_version = smartchangelog.__version__
    with set_args(changelog_script_path, "--version") as result, pytest.raises(SystemExit) as e:
        # WHEN
        changelog_script.main()
    stdout, stderr = result
    version = stdout.read().strip("\n")
    # THEN
    assert e.value.code == 0
    assert version == expected_version
