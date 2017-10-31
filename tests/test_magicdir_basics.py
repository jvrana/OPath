from magicdir import *
import pytest

@pytest.fixture(params=[True, False])
def a(request):
    env = MagicDir('bin', push_up=request.param)
    labels = ['a', 'b']

    for l1 in labels:
        env.add(l1)
        assert hasattr(env, l1)

        level = getattr(env, l1)
        for l2 in labels:

            next_level = l1 + l2
            getattr(env, l1).add(next_level)

            if request.param:
                assert hasattr(env, next_level)
            else:
                assert not hasattr(env, next_level)
            assert hasattr(level, next_level)

# def test_access(a):
#     pass

def test_attr():
    env = MagicDir('bin')
    name = 'somethigldj'
    attr = 'asldkfjlsdfj'
    env.add(name, attr = attr)
    assert hasattr(env, attr)
    assert not hasattr(env, name)

def test_unsanitized_attr():
    env = MagicDir('bin')
    env.add('something')
    with pytest.raises(AttributeError):
        env.add('alskdf;;asd;flj')
    with pytest.raises(AttributeError):
        env.add('in')
    with pytest.raises(AttributeError):
        env.add('something')
    with pytest.raises(AttributeError):
        env.add('something', attr='somethingelse')

def test_unique_attrs():
    env = MagicDir('bin')
    with pytest.raises(AttributeError):
        env.add('L1').add('L2')
        env.add('L1a').add('L2')

def test_path():
    env = MagicDir('bin')
    env.add('session1')
    env.session1.add('cat1')
    env.session1.add('cat2')
    env.add('session2')
    env.session2.add('cat1', attr="s2cat1")

    assert str(env.path) == 'bin'
    assert str(env.s2cat1.path) == 'bin/session2/cat1'
    assert str(env.cat1.path) == 'bin/session1/cat1'
    assert str(env.cat2.path) == 'bin/session1/cat2'

def test_print_tree():
    env = MagicDir('bin', push_up=True)
    env.add('session1')
    env.session1.add('cat1')
    env.session1.add('cat2')
    env.add('session2')
    env.session2.add('cat1', attr="s2cat1")

    print(env._children)

    env.print()

def test_paths():
    env = MagicDir('bin')
    env.add('session1')
    env.session1.add('cat1')
    env.session1.add('cat2')

    assert len(env.paths) == 4
    print(env.paths)

def test_resolve():
    env = MagicDir('bin')
    env.add('session1')
    env.session1.add('cat1')
    env.session1.add('cat2')
    print(env.paths.resolve)

def test_remove():

    env = MagicDir('bin', push_up=True)

    a1 = env.add('A1')
    env.A1.add('A2')
    b1 = env.add('B1')
    env.B1.add('B2')

    assert hasattr(env, 'A1')
    assert hasattr(env, 'B1')
    assert hasattr(env.A1, 'A2')
    assert hasattr(env.B1, 'B2')
    assert hasattr(env, 'A2')
    assert hasattr(env, 'B2')

    env.A1.remove_parent()

    g = env.descendents()

    # Cannot access A1 from env. Can still access A2 from a1
    assert not hasattr(env, 'A1')
    assert not hasattr(env, 'A2')
    assert hasattr(a1, 'A2')

    # B1 and B2 are still exist
    assert hasattr(env, 'B1')
    assert hasattr(env.B1, 'B2')
    assert hasattr(env, 'B2')

def test_remove_children():

    env = MagicDir('bin', push_up=True)

    a1 = env.add('A1')
    env.A1.add('A2')
    b1 = env.add('B1')
    env.B1.add('B2')

    assert hasattr(env, 'A1')
    assert hasattr(env, 'B1')
    assert hasattr(env.A1, 'A2')
    assert hasattr(env.B1, 'B2')
    assert hasattr(env, 'A2')
    assert hasattr(env, 'B2')

    print(env.children.remove_parent())

    g = env.descendents()
    assert len(g) == 0