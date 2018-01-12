.. OPath documentation master file, created by
   sphinx-quickstart on Thu Jan 11 17:29:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OPath: Python directory and file tree object encapsulation
==========================================================

|travis build| |Coverage Status| |PyPI version| |License: MIT|

OPath is a library for encapsulating directory and file trees.
It makes creating, moving, and deleting directories and files
a breeze.

**GitHub**: https://github.com/jvrana/opath

.. toctree::
   :maxdepth: 3

   index

Build/Coverage Status
---------------------

OPath is currently in development (Version |Version|)

+-------------------+------------------+---------------------+
| Branch            | Build            | Coverage            |
+===================+==================+=====================+
| **master**        | |travis build|   | |Coverage Status|   |
+-------------------+------------------+---------------------+
| **development**   | |travis build|   | |Coverage Status|   |
+-------------------+------------------+---------------------+

Installation
------------

Its suggested you use `pipenv <https://pipenv.readthedocs.io/en/latest/>`__ to install OPath.

OPath can be downloaded from `PyPI here <https://pypi.python.org/pypi/opath/0.5.1>`__

**Option 1 (recommended): pipenv**

To install, just cd into your project and run. Make sure to review how to use
`pipenv <https://pipenv.readthedocs.io/en/latest/>`__.

To install your project to the virtual environment

.. code:: bash

   pipenv install opath


**Option 2: pip**

To install on your machine using pip/pip3

.. code:: bash

   pip install opath

Usage
-----

Use ``add`` to create folders.

.. code:: python

    from opath import *

    env = ODir('bin')
    env.add('subfolder1')
    env.add('subfolder2')
    env.print()

    >>>
    *bin
    |   *subfolder1
    |   *subfolder2

Functions return ODir objects and so can be chained together.

.. code:: python

    env = ODir('bin')
    env.add('subfolder1').add('subsubfolder')
    env.print()

    >>>
    *bin
    |   *subfolder1
    |   |   *subsubfolder

Files can be written quickly

.. code:: python

    env = ODir('bin')
    env.add('subfolder1').add('subsubfolder')
    env.subsubfolder.write('My Data', 'w')

Or a OFile can be added:

.. code:: python

    env = ODir('bin')
    env.add_file('myfile.txt', attr='myfile')
    env.myfile.write('this is my data', 'w')

Folders create accesible ODir attributes automatically. Alternative
attribute names can be set using 'alias='

.. code:: python

    env = ODir('bin')
    env.add('subfolder1')
    env.subfolder1.add('misc')
    env.subfolder1.misc.add('.hidden', alias='hidden')
    env.subfolder1.misc.hidden.add('hiddenbin')
    env.print()

    *bin
    |   *subfolder1
    |   |   *misc
    |   |   |   *.hidden ("hidden")
    |   |   |   |   *hiddenbin

By default, attributes are *pushed* back the the root directory. The
following is equivalent to above.

.. code:: python

    env = ODir('bin')
    env.add('subfolder1')
    env.subfolder1.add('misc')
    env.misc.add('.hidden', alias='hidden')
    env.hidden.add('hiddenbin')
    env.print()

    *bin
    |   *subfolder1
    |   |   *misc
    |   |   |   *.hidden ("hidden")
    |   |   |   |   *hiddenbin


Making, moving, copying, and deleting directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The location of the root folder can be set by ``set_bin``

.. code:: python

    env.set_bin('../bin')

Directories can be created, deleted, copied or moved using ``mkdirs``,
``cpdirs``, ``mvdirs``, ``rmdirs``

.. code:: python

    env.mkdirs()
    env_copy = env.cpdirs()
    # you can do stuff with env_copy independently
    env.mvdirs('~/Document')
    env_copy.rmdirs()

Advanced usage
^^^^^^^^^^^^^^

All iterables return special list-like objects that can be chained in
one-liners.

.. code:: python

    env.descendents() # returns a ChainList object

    # find all txt files
    env.descendents(include_self=True).glob("*.txt")

    # recursively change permissions for directories
    env.abspaths.chmod(0o444)


Running Tests
-------------

To run tests, cd into the OPath directory and run

.. code:: bash

   pipenv run pytest


API Reference
-------------

.. toctree::
   :maxdepth: 3
.. automodule:: opath
      :members:
      :noindex:


.. |travis build| image:: https://img.shields.io/travis/jvrana/magicdir.svg
   :target: https://travis-ci.org/jvrana/magicdir
.. |Coverage Status| image:: https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master
   :target: https://coveralls.io/github/jvrana/magicdir?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/REPO.svg
   :target: https://badge.fury.io/py/REPO
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |travis build| image:: https://img.shields.io/travis/jvrana/magicdir/master.svg
   :target: https://travis-ci.org/jvrana/magicdir/master
.. |travis build| image:: https://img.shields.io/travis/jvrana/magicdir/development.svg
   :target: https://travis-ci.org/jvrana/magicdir/development
.. |Coverage Status| image:: https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=development
   :target: https://coveralls.io/github/jvrana/magicdir?branch=development