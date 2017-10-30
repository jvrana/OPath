[![travis build](https://img.shields.io/travis/jvrana/magicdir.svg)](https://travis-ci.org/jvrana/magicdir)
[![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
[![PyPI version](https://badge.fury.io/py/REPO.svg)](https://badge.fury.io/py/REPO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![module_icon](images/module_icon.png?raw=true)

#### Build/Coverage Status
Branch | Build | Coverage
:---: | :---: | :---:
**master** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/master.svg)](https://travis-ci.org/jvrana/magicdir/master) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
**development** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/development.svg)](https://travis-ci.org/jvrana/magicdir/development) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=development)](https://coveralls.io/github/jvrana/magicdir?branch=development)

# magicdir

Dealing with paths and directories can be a pain. **Treehouse** allows you to build directory trees by treating
your directory tree as a first-class object.

So fancy. So perfect. So forever.

```python
from treehouse import magicdir

env = magicdir('bin')
env.add('level1')

# paths can be accessed as attributes
env.level1

# paths and attributes are heirarchical
env.level1.add('level2')
env.level1.level2

# by default, attributes get 'pushed' back to root for quick access to your paths
env.level2 == env.level1.level2

# attribute aliases can be defined
env.level2.add('level2', alias='level2a')
env.level2a

# print the expected tree
env.print_tree()

# alias of directory
env.alias
env.level1.alias

# name of directory
env.name
env.level1.name

# print root path
env.path # relative path
env.path.absolute()
env.abspath

# print paths in tree
env.paths # relative paths
env.paths.absolute() # absolute paths
env.abspaths

# all attributes return another magicdir object
l2 = env.level2
print("tree")
env.print_tree()

print("level2 tree")
l2.print_tree()

# set the parent directory this directory tree will exist in
env.set_dir('..')

# instantly make the directory tree
env.mkdirs()

# remove the directory tree (be careful!)
env.rmdirs()

# move the directory tree
env.mvdirs()

# copy the directory tree
env.cpdirs()

# get root
assert env is env.misc.root

#
env.misc.somethingelse = 5
assert not hasattr(env, 'somethingelse')
assert hasattr(env.misc, 'somethingelse')

# fancy things
env.misc.ancestors(include_self=True).name # name of all attributes for parents
env.descendents(include_self=True).name # name of all children
env.paths.absolute().resolve() # chain things together

env.paths # all paths of all children
env.paths.absolute() # apply absolute() to each path, return ChainList
env.paths.resolve() # apply absolute() and then resolve() to each path, return ChainList

# quickly writing files

```

The following are equivalent ways to produce the following directory
structure:

```python
env = magicdir('bin')
env.add('.secrets', alias='secrets')
env.secrets.add('misc')
env.add('public')
env.public.add('category1')
env.public.add('category2')

env.mkdirs()
```

```python
env = magicdir('bin')
env.add('.secrets', alias='secrets').add('misc')
env.add('public').add('category1')
env.public.add('category2')

env.mkdirs()
```

```python
env = magicdir('bin')
env.add('.secrets', alias='secrets').add('misc')
env.add('public/category1')
env.add('public/category2')
env.mkdirs()
```

Quickly access your paths:
```python
env.category1 # 'bin/public/category1'
env.category2 # 'bin/public/category2'
env.public  # 'bin/public'
env.secrets # 'bin/.secrets'
env.misc # 'bin/.secrets/misc'
```