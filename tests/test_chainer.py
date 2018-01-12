import pytest

from opath import ObjChain, ChainList


# TODO: better testing for push_up = False

def test_chain_list():
    x = ["the", "cow", "jumped"]
    x = ChainList(x)
    print(x)
    list(x)
    x.strip()
    assert [y.replace('e', 'a') for y in x] == list(x.replace("e", "a"))

    empty = ChainList([])
    assert list(empty) == []

def test_chain_equivalence():
    parent = ObjChain()
    assert parent.root == parent

    child = parent._create_and_add_child('child')
    assert child.root == parent

    grandchild = child._create_and_add_child('grandchild')
    assert grandchild.root == parent

    assert not grandchild.is_root()
    assert not child.is_root()
    assert parent.is_root()


@pytest.fixture(params=[True, False])
def test_chainer(request):
    pushup = request.param
    a = ObjChain(push_up=pushup)
    a._create_and_add_child('b1', )
    a._create_and_add_child('c1', )
    a.b1._create_and_add_child('b2', )
    a.b1.b2._create_and_add_child('b3', )
    a.c1._create_and_add_child('c2', )

    assert hasattr(a.c1, 'c2', )
    assert hasattr(a, 'b1')
    assert hasattr(a.b1, 'b2')
    assert hasattr(a.b1.b2, 'b3')

    if not pushup:
        assert not hasattr(a, 'b2')
        assert not hasattr(a, 'b3')
        assert not hasattr(a, 'c2')
    else:
        assert hasattr(a, 'b2')
        assert hasattr(a, 'b3')
        assert hasattr(a, 'c2')

def test_chainer_add_child(test_chainer):
    pass


def test_chaining():
    a = ObjChain(push_up=True)
    a._create_and_add_child('b1', )
    a._create_and_add_child('c1', )
    a.b1._create_and_add_child('b2', )
    b3 = a.b1.b2._create_and_add_child('b3', )
    a.c1._create_and_add_child('c2', )
    print(a.descendents().attr)
    assert set(a.descendents().attr) == set(['b1', 'c1', 'b2', 'b3', 'c2'])
    a.descendents()[1]
    set(a.descendents())
    assert set(b3.ancestors().attr) == set(['b2', 'b1', None])

    children = a.descendents()

    children += [1]
    assert type(children) is ChainList


def test_ancestors():
    a = ObjChain(push_up=True)
    a._create_and_add_child('b1', )
    a.b1._create_and_add_child('c1', )
    d1 = a.c1._create_and_add_child('d1', )

    assert len(a.descendents(include_self=False)) == 3
    assert len(a.descendents(include_self=True)) == 4

    assert len(d1.ancestors(include_self=False)) == 3
    assert len(d1.ancestors(include_self=True)) == 4


def test_remove():
    a = ObjChain(push_up=True)
    a._create_and_add_child('b1', )
    a.b1._create_and_add_child('c1', )
    a.c1._create_and_add_child('d1', )
    a.d1._create_and_add_child('e1')

    assert hasattr(a, 'b1')
    assert hasattr(a, 'c1')
    assert hasattr(a, 'd1')
    assert hasattr(a, 'e1')

    c1 = a.c1.remove_parent()
    assert hasattr(a, 'b1')
    assert not hasattr(a, 'c1')
    assert not hasattr(a, 'd1')
    assert not hasattr(a, 'e1')

    assert hasattr(c1, 'd1')
    assert hasattr(c1, 'e1')
    assert c1.root is c1
    assert c1.d1.root is c1
    assert c1.e1.root is c1


def test_remove_children():
    a = ObjChain(push_up=True)
    a._create_and_add_child('b1', )
    a._create_and_add_child('b2', )
    a.b1._create_and_add_child('c1', )
    a.c1._create_and_add_child('d1', )
    a.d1._create_and_add_child('e1')

    assert hasattr(a, 'b1')
    assert hasattr(a, 'c1')
    assert hasattr(a, 'd1')
    assert hasattr(a, 'e1')

    a.children.remove_parent()

    assert not hasattr(a, 'b2')
    assert not hasattr(a, 'b1')
    assert not hasattr(a, 'c1')
    assert not hasattr(a, 'd1')
    assert not hasattr(a, 'e1')


def test_set_raises_attr_error():

    a = ObjChain()
    a._create_and_add_child('b1')
    with pytest.raises(AttributeError):
        a.b1 = 4


def test_sanitize_attr():

    a = ObjChain()
    with pytest.raises(AttributeError):
        a._create_and_add_child('in')
    with pytest.raises(AttributeError):
        a._create_and_add_child('with')
    n = 'something'
    a._create_and_add_child(n)
    with pytest.raises(AttributeError):
        a._create_and_add_child(n)


def test_default_push_up_True():
    a = ObjChain(push_up=True)
    a._create_and_add_child('b')._create_and_add_child('c')
    assert hasattr(a, 'b')
    assert hasattr(a, 'c')
    assert a.has('b')
    assert a.has('c')
    assert a.get('b').has('c')


def test_default_push_up_False():
    a = ObjChain(push_up=False)
    a._create_and_add_child('b')._create_and_add_child('c')
    assert hasattr(a, 'b')
    assert not hasattr(a, 'c')
    assert a.has('b')
    assert not a.has('c')
    assert a.get('b').has('c')
