import pytest
from pathlib import Path
import uuid


@pytest.fixture(scope="function")
def file_env(env):
    env.A1.add_file('test.txt', attr='testtxt')
    env.A1.add_file('test.json', attr='testjson')
    return env


def test_file_basics(file_env):
    assert file_env.testtxt.name == 'test.txt'
    assert Path(file_env.A1.abspath, 'test.txt') == file_env.testtxt.abspath


def test_file_denied_access(file_env):

    with pytest.raises(AttributeError):
        file_env.testtxt.add('something')

    with pytest.raises(AttributeError):
        file_env.testtxt.paths

    with pytest.raises(AttributeError):
        file_env.testtxt.abspaths

    with pytest.raises(AttributeError):
        file_env.testtxt.mkdirs()


def test_file_write_remove(file_env):
    file_env.rmdirs()
    file_env.mkdirs()
    assert not file_env.testtxt.abspath.is_file()
    assert not file_env.testtxt.abspath.is_dir()
    file_env.testtxt.write('w', 'data')
    assert file_env.testtxt.abspath.is_file()

    file_env.testtxt.rm()
    assert not file_env.testtxt.abspath.is_file()


def test_file_dump_load(file_env):
    file_env.rmdirs()
    file_env.mkdirs()

    mydata = {'x': 5, 'y': 4}
    file_env.testjson.dump(mydata, 'w')
    loaded = file_env.testjson.load('r')


def test_open(file_env):

    file_env.mkdirs()
    data = str(uuid.uuid4())
    file_env.testtxt.write('w', data)

    assert file_env.A1.read_file('test.txt', 'r') == data
    assert file_env.testtxt.open('r').read() == data
    assert file_env.testtxt.read('r') == data


def test_raise_filename_error(file_env):

    file_env.mkdirs()

    data = str(uuid.uuid4())
    file_env.testtxt.write('w', data)

    with pytest.raises(AttributeError):
        file_env.A1.add_file(file_env.testtxt.name)

    with pytest.raises(AttributeError):
        file_env.A1.add_file("new_file.txt", attr='A1')

    with pytest.raises(AttributeError):
        file_env.A1.add_file(file_env.testtxt.name, attr='dflkdjlf')

def test_retrieve_existing_file(file_env):

    file_env.mkdirs()
    data = str(uuid.uuid4())
    f = file_env.A1.add_file("test.txt", attr="testtxt")
    f2 = file_env.A1.add_file("test.txt", attr="testtxt")
    assert f == f2

    file_env.add_file('log.txt', attr='log')
    file_env.add_file('log.txt', attr='log')


def test_dynamic_file_creation(file_env):

    file_env.rmdirs()
    file_env.mkdirs()

    data = str(uuid.uuid4())
    file_env.A2.add_file("new_file.txt", attr="file").write('w', data)
    assert file_env.file.read('r') == data


def test_write_file_exists(file_env):

    file_env.rmdirs()
    file_env.mkdirs()

    data = str(uuid.uuid4())
    file_env.A2.add_file("new_file.txt", attr="file").write('w', data)
    assert file_env.file.read('r') == data