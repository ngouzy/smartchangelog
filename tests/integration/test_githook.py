import os
import shutil

import pytest

from smartchangelog import githook
# noinspection PyUnresolvedReferences
from tests.integration import hook_path, temp_dir


@pytest.mark.usefixtures("temp_dir")
def test_githook_install():
    # GIVEN
    # WHEN
    commitmsg_hook_path = githook.install()
    # THEN
    assert os.path.abspath(commitmsg_hook_path) == os.path.join(hook_path(), 'commit-msg')


@pytest.mark.usefixtures("temp_dir")
def test_githook_install_without_githook_folder():
    # GIVEN
    shutil.rmtree(hook_path())
    # WHEN
    commitmsg_hook_path = githook.install()
    # THEN
    assert os.path.abspath(commitmsg_hook_path) == os.path.join(hook_path(), 'commit-msg')


@pytest.mark.usefixtures("temp_dir")
def test_githook_uninstall():
    # GIVEN
    githook.install()
    expected_commitmsg_hook_path = os.path.join(hook_path(), 'commit-msg')
    # WHEN
    commitmsg_hook_path = githook.uninstall()
    # THEN
    assert os.path.abspath(commitmsg_hook_path) == expected_commitmsg_hook_path


@pytest.mark.usefixtures("temp_dir")
def test_githook_uninstall_without_githook_folder():
    # GIVEN
    shutil.rmtree(hook_path())
    # WHEN
    commitmsg_hook_path = githook.uninstall()
    # THEN
    assert commitmsg_hook_path is None
