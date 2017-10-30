import pytest
from magicdir import *
from pathlib import Path

@pytest.fixture(scope="module")
def this_dir():
    return Path(__file__).absolute().parent

@pytest.fixture(scope="function")
def testing_dirs():
    env1 = Path(this_dir(), 'env1')
    env2 = Path(this_dir(), 'env2')

    if env1.is_dir():
        rmtree(env1)
    if env2.is_dir():
        rmtree(env2)


    env1.mkdir()
    env2.mkdir()
    return env1, env2
