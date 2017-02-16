import inspect

import pytest

import commitmsg


@pytest.fixture(scope="module")
def commitmsg_script():
    """Get path of the file containing commitmsg module"""
    return inspect.getfile(commitmsg)
