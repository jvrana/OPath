import pytest
from pathlib import Path
import shutil

@pytest.fixture(scope="module")
def this_dir():
    return Path(__file__).absolute().parent

@pytest.fixture(scope="function")
def testing_dirs():
    env1 = Path(this_dir(), 'env1')
    env2 = Path(this_dir(), 'env2')

    if env1.is_dir():
        shutil.rmtree(env1)
    if env2.is_dir():
        shutil.rmtree(env2)

    env1.mkdir(exist_ok=True)
    env2.mkdir(exist_ok=True)
    return env1, env2
