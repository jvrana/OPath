from .magicchain import MagicChain, MagicList
from pathlib import *
from copy import deepcopy
from .magicchain import MagicChain
from .utils import *
import glob


class MagicPath(MagicChain):

    def __init__(self, name, push_up=True):
        super().__init__(parent=None, push_up=push_up)
        self.name = name
        self._parent_dir = ''

    @property
    def dir(self):
        return self.root._parent_dir

    @property
    def relpath(self):
        return Path(*self.ancestors(include_self=True).name)

    @property
    def path(self):
        return Path(self.dir, *self.ancestors(include_self=True).name)

    @property
    def abspath(self):
        return self.path.absolute()

    def set_dir(self, path):
        self.root._parent_dir = path
        return path

    def remove_parent(self):
        new_parent = self.abspath.parent
        self._parent_dir = new_parent
        return super().remove_parent()

    def exists(self):
        return self.abspath.is_dir()

    def write(self, filename, mode, data, *args, **kwargs):
        with self.open(filename, mode, *args, **kwargs) as f:
            f.write(data)

    def read(self, filename, mode, *args, **kwargs):
        with self.open(filename, mode, *args, **kwargs) as f:
            return f.read()

    def open(self, filename, mode, *args, **kwargs):
        return fopen(str(Path(self.abspath, filename)), mode, *args, **kwargs)

    def __repr__(self):
        return "<{}(\"{}\")>".format(self.__class__.__name__, self.name, self.relpath)


class MagicFile(MagicPath):

    def write(self, mode, data, *args, **kwargs):
        return self.parent.write(self.name, mode, data, *args, **kwargs)

    def read(self, mode, *args, **kwargs):
        return self.parent.read(self.name, mode, *args, **kwargs)

    def open(self, mode, *args, **kwargs):
        return self.parent.open(self.name, mode, *args, **kwargs)

    def rm(self):
        os.remove(str(self.abspath))


class MagicDir(MagicPath):

    @property
    def files(self):
        desc = self.descendents(include_self=True)
        return MagicList([d for d in desc if d.__class__ is MagicFile])

    @property
    def dirs(self):
        desc = self.descendents(include_self=True)
        return MagicList([d for d in desc if d.__class__ is self.__class__])

    @property
    def paths(self):
        return self.dirs.path

    @property
    def abspaths(self):
        return self.paths.absolute()

    def all_exists(self):
        return all(self.abspaths.is_dir())

    def mkdirs(self):
        for p in self.abspaths:
            makedirs(p, exist_ok=True)
        return self

    def rmdirs(self):
        if self.abspath.is_dir():
            rmtree(self.abspath)
        return self

    def cpdirs(self, new_parent):
        copytree(self.abspath, Path(new_parent, self.name))
        copied_dirs = deepcopy(self)
        copied_dirs.remove_parent()
        copied_dirs.set_dir(new_parent)
        return copied_dirs

    def mvdirs(self, new_parent):
        oldpath = self.abspath
        self.remove_parent()
        copytree(oldpath, Path(new_parent, self.name))
        self.set_dir(new_parent)
        rmtree(oldpath)

    def ls(self):
        return listdir(self.abspath)

    def glob(self, pattern):
        return glob.glob(str(Path(self.abspath, pattern)))

    def collect(self):
        """ collects new directories that exist on the local machine and add to tree """

    def add(self, name, attr=None):
        if attr is None:
            attr = name
        if name in self.children.name:
            raise AttributeError("Folder name \"{}\" already exists. Existing folders: {}".format(name,
                  ', '.join(self.childen.name)))
        return self._create_and_add_child(attr, with_attributes={"name": name})

    def add_file(self, name, attr=None):
        if attr is None:
            attr = name
        if name in self.files.name:
            raise AttributeError("File name \"{}\" already exists. Existing files: {}".format(name,
                  ', '.join(self.files.name)))
        file = MagicFile(name)
        file._parent = self
        file.attr = attr
        self._add_child(file)
        return file

    def print(self, print_files=False, indent=4, max_level=None, level=0, list_missing=True):
        padding = '|   ' * level
        name = self.name
        if self.attr and name != self.attr:
            name += " (\"{}\")".format(self.attr)
        missing_tag = ''
        if list_missing and not self.exists():
            missing_tag = "*"
        print("{padding}{missing}{name}".format(missing=missing_tag, padding=padding, name=name))

        level += 1
        for name, child in self._children.items():
            child.print(print_files, indent, max_level, level, list_missing)