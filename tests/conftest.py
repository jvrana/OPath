import pytest
from magicdir import MagicDir
from pathlib import Path
from magicdir import utils


@pytest.fixture(scope="module")
def this_dir():
    return Path(__file__).absolute().parent


@pytest.fixture(scope="function")
def testing_dirs():
    env1 = Path(this_dir(), 'env1')
    env2 = Path(this_dir(), 'env2')

    if env1.is_dir():
        utils.rmtree(env1)
    if env2.is_dir():
        utils.rmtree(env2)


    env1.mkdir()
    env2.mkdir()
    return env1, env2


@pytest.fixture(scope="function")
def env():
    env = MagicDir('bin')
    env.set_dir(testing_dirs()[0])
    env.add('A1')
    env.A1.add('A2')
    env.add('B1')
    env.B1.add('B2')
    return env
