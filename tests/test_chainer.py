from treehouse import *
import pytest

def test_chain_list():

    x = ["the", "cow", "jumped"]
    x = ChainList(x)

    x.strip()
    print(x.replace("e", "a"))


def test_chain_equivalence():
    parent = Chainer()
    assert parent.root == parent

    child = Chainer(parent=parent)
    assert child.root == parent

    grandchild = Chainer(parent=child)
    assert grandchild.root == parent

@pytest.fixture(params=[True, False])
def b(request):
    pushup = request.param
    a = Chainer(push_up=pushup)
    a._add_child('b1', )
    a._add_child('c1', )
    a.b1._add_child('b2', )
    a.b1.b2._add_child('b3', )
    a.c1._add_child('c2', )

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

def test_chainer_add_child(b):
    pass


def test_chaining():
    a = Chainer(push_up=True)
    a._add_child('b1', )
    a._add_child('c1', )
    a.b1._add_child('b2', )
    b3 = a.b1.b2._add_child('b3', )
    a.c1._add_child('c2', )

    assert set(a.descendents().alias) == set(['b1', 'c1', 'b2', 'b3', 'c2'])
    a.descendents()[1]
    set(a.descendents())
    assert set(b3.ancestors().alias) == set(['b2', 'b1', None])

    children = a.descendents()

    children += [1]
    assert type(children) is ChainList

def test_ancestors():
    a = Chainer(push_up=True)
    a._add_child('b1', )
    a.b1._add_child('c1', )
    d1 = a.c1._add_child('d1', )

    assert len(a.descendents(include_self=False)) == 3
    assert len(a.descendents(include_self=True)) == 4

    assert len(d1.ancestors(include_self=False)) == 3
    assert len(d1.ancestors(include_self=True)) == 4

def test_remove():
    a = Chainer(push_up=True)
    a._add_child('b1', )
    a.b1._add_child('c1', )
    a.c1._add_child('d1', )
    a.d1._add_child('e1')

    assert hasattr(a, 'b1')
    assert hasattr(a, 'c1')
    assert hasattr(a, 'd1')
    assert hasattr(a, 'e1')

    c1 = a.c1.remove()
    assert hasattr(a, 'b1')
    assert not hasattr(a, 'c1')
    assert not hasattr(a, 'd1')
    assert not hasattr(a, 'e1')

    assert hasattr(c1, 'd1')
    assert hasattr(c1, 'e1')


def test_attributes():
    a = Chainer(push_up=True)
    a._add_child('b1', )
    a.b1._add_child('c1', )
    d1 = a.c1._add_child('d1', )

    d1.ancestor_attrs('alias')

    # a.c1 = 4

