import uuid

from pathlib import Path


def test_mkdir_rmdir(env):
    # remove
    env.rmdirs()
    assert not env.all_exists()

    # make
    env.mkdirs()
    assert env.all_exists()
    assert Path(env._parent_dir, 'bin/A1/A2').absolute().is_dir()
    assert Path(env._parent_dir, 'bin/B1/B2').absolute().is_dir()

    # remove
    env.rmdirs()
    assert not env.all_exists()


def test_delete(env):
    env.mkdirs()

    a1 = env.A1
    oldpath = a1.abspath
    a1.remove_parent()
    assert oldpath == a1.abspath
    assert not hasattr(env, 'A1')
    assert not hasattr(env, 'A2')
    assert hasattr(a1, 'A2')

def test_cpdirs(env, testing_dirs):
    env.mkdirs()
    filename = '{}.txt'.format(str(uuid.uuid4()))
    with open(str(Path(env.A2.abspath, filename)), 'w') as f:
        f.write('this is some test text')

    envcopy = env.cpdirs(testing_dirs[1])

    assert Path(env.A2.abspath, filename).is_file()
    assert Path(envcopy.A2.abspath, filename).is_file()
    assert Path(testing_dirs[1], 'bin', 'A1', 'A2', filename).is_file()

    env.rmdirs()
    print(env.A2.abspath)
    print(envcopy.A2.abspath)
    assert not Path(env.A2.abspath, filename).is_file()
    assert Path(envcopy.A2.abspath, filename).is_file()


    a1copy = envcopy.A1.cpdirs(testing_dirs[0])

    assert a1copy.is_root()
    envcopy.A1.rmdirs()
    assert hasattr(a1copy, 'A2')


def test_mvdir(env, testing_dirs):
    # folder 1
    env.set_dir(testing_dirs[0])
    env.mkdirs()

    # write custom file
    filename = '{}.txt'.format(str(uuid.uuid4()))
    with open(str(Path(env.A2.abspath, filename)), 'w') as f:
        f.write('this is some test text')

    assert Path(env.A2.abspath, filename).is_file()
    assert not Path(testing_dirs[1], 'bin', 'A1', 'A2', filename).is_file()
    assert Path(testing_dirs[0], 'bin', 'A1', 'A2', filename).is_file()

    # folder 2
    env.mvdirs(testing_dirs[1])
    assert Path(env.A2.abspath, filename).is_file()
    assert Path(testing_dirs[1], 'bin', 'A1', 'A2', filename).is_file()
    assert not Path(testing_dirs[0], 'bin', 'A1', 'A2', filename).is_file()

def test_mvdir_doesnt_exist(env, testing_dirs):
    # folder 1
    env.set_dir(testing_dirs[0])
    env.rmdirs()
    # env.mkdirs()

    # folder 2
    env.mvdirs(testing_dirs[1])

def test_open(env):

    env.mkdirs()
    env.A2.open_file('open_test.txt', 'w').write("stuff")

    assert Path(env.A2.abspath, 'open_test.txt').is_file()

def test_read_write(env):

    env.mkdirs()
    env.A2.write_file('open_test.txt', 'w', 'stuff')

    assert Path(env.A2.abspath, 'open_test.txt').is_file()
    assert env.A2.read_file('open_test.txt', 'r') == 'stuff'

def test_ls(env):
    env.mkdirs()
    assert len(env.ls()) == 2

def test_glob(env):
    env.mkdirs()
    env.A2.write_file('open_text.txt', 'w', 'stuff')
    env.A2.write_file('open_text2.txt', 'w', 'stuff')
    assert len(env.glob('*.txt')) == 0
    assert len(env.A2.glob("*.txt")) == 2

def test_get(env):

    assert env.get('A1') is env.A1

# def test_print_tree(env):
#     env.mkdirs()
#     env.list_dir()