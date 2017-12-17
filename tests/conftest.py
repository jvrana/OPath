import pytest
from magicdir import MagicDir
from pathlib import Path
from magicdir import utils


@pytest.fixture(scope="function")
def testing_dirs(tmpdir):
    env1 = Path(tmpdir, 'env1')
    env2 = Path(tmpdir, 'env2')

    if env1.is_dir():
        utils.rmtree(env1)
    if env2.is_dir():
        utils.rmtree(env2)


    env1.mkdir()
    env2.mkdir()
    return env1, env2

@pytest.fixture(scope="function")
def env(tmpdir):
    env = MagicDir('bin')
    env.set_dir(tmpdir)
    env.add('A1')
    env.A1.add('A2')
    env.add('B1')
    env.B1.add('B2')
    return env
