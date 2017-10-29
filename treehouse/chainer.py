import keyword
from copy import copy


class ChainList(list):
    """ List-like class that collects attributes """

    def __getattr__(self, item):
        return ChainList([getattr(x, item) for x in self])

    def __call__(self, *args, **kwargs):
        return ChainList([x(*args, **kwargs) for x in self])


class Chainer(object):
    """ A tree-like class for chaining commands and attributes together """

    def __init__(self, parent=None, push_up=None):
        """
        Chainer constructor

        :param parent: parent node that called this object
        :type parent: Chainer
        :param push_up: whether to push up attributes to the root node
        :type push_up: boolean
        """
        self._parent = parent
        self._children = {}
        self._grandchildren = {}
        self._push_up = False
        if push_up is not None:
            self._push_up = push_up
        self._alias = None

    @property
    def alias(self):
        return self._alias

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return ChainList(self._children.values())

    @property
    def root(self):
        if self.parent is None:
            return self
        return self.parent.root

    def descendents(self, include_self=False):
        c = []
        if include_self:
            c = [self]
        if not self._children == {}:
            children = list(self._children.values())
            c += children
            for child in children:
                c += child.descendents()
        return ChainList(c)

    def ancestors(self, include_self=False):
        p = []
        if include_self:
            p = [self]
        if self.parent is not None:
            p += self.parent.ancestors()+[self.parent]
        return ChainList(p)

    def ancestor_attrs(self, attr, include_self=False):
        nodes = self.ancestors(include_self=include_self)+[self]
        return [getattr(n, attr) for n in nodes]

    def descendent_attrs(self, attr, include_self=False):
        nodes = self.descendents(include_self=include_self)+[self]
        return [getattr(n, attr) for n in nodes]

    def remove(self):
        if self.parent is not None:
            self.parent._remove_grandchild(self.alias)
            for c in self.descendents():
                self.parent._remove_grandchild(c.alias)
            rm = self.parent._remove_child(self.alias)
            rm._parent = None
            return rm

    def _sanitize_identifier(self, iden):
        if keyword.iskeyword(iden):
            raise AttributeError("\"{}\" is reserved and is not a valid identified.".format(iden))
        if not iden.isidentifier():
            raise AttributeError("\"{}\" is not a valid identifier.".format(iden))
        if hasattr(self, iden):
            raise AttributeError("identifier \"{}\" already exists".format(iden))

    def _add_child(self, alias, child=None, with_attributes=None, push_up=None):
        if push_up is None:
            push_up = self._push_up
        self._sanitize_identifier(alias)
        if child is None:
            child = self._create_child(alias, with_attributes)
        self._children[alias] = child
        if push_up:
            root = self.root
            if not self is root:
                if hasattr(root, alias):
                    raise AttributeError("Cannot push alias {} to root. Try using a unique alias.".format(alias))
                root._grandchildren[alias] = child
        return child

    def _update_grandchildren(self):
        for n, c in self._children:
            self._add_child()

    # def _connect(self, other):
    #     self._add_child(other)
    #     self.children()._connect()
    #     return other

    def _remove_grandchild(self, alias):
        gc = self.root._grandchildren
        if alias in gc:
            return gc.pop(alias)

    def _remove_child(self, alias):
        if alias in self._children:
            return self._children.pop(alias)

    def _create_child(self, alias, with_attributes=None):
        c = copy(self)
        c._parent = self
        c._children = {}
        c._grandchildren = {}
        if with_attributes is None:
            with_attributes = {}
        for k, v in with_attributes.items():
            setattr(c, k, v)
        c._alias = alias
        return c

    def __getattr__(self, name):
        c = {}
        c.update(object.__getattribute__(self, "_children"))
        c.update(object.__getattribute__(self, "_grandchildren"))
        if name in c:
            return c[name]
        else:
            return object.__getattribute__(self, name)

    # def __setattr__(self, name, value):
    #     if name in self._children:
    #         child = getattr(self, name)
    #
    #         child.remove()
    #     return object.__setattr__(self, name, value)