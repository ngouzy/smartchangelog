import inspect

import pytest

import commitmsg


@pytest.fixture(scope="module")
def commitmsg_script():
    return inspect.getfile(commitmsg)
