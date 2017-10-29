# Usage

This is a blank python project for Travis-CI and PyPI release.

1. Text search and replace `USER/REPO` with your username and repo
1. Replace `MODULE` in setup.py with your module name
1. replace `url='https://github.com/USER/REPO'` in setup.py
1. Add files to your `MANIFEST.in`
1. Add your license to `LICENSE.txt` and `setup.py`
1. setup the rest of setup.py with python version, description, keywords, author, email, etc.
1. setup .travis.yml
    1. pick your python versions
    1. setup the install comman
1. deploying using PyPI
    1. cd locally to your repo
    1. run `travis encrypt --add deploy.password`
    1. type in your github password. Enter. Ctrl+D
1. encrypting secret files (https://docs.travis-ci.com/user/encrypting-files/)
    1. `travis encrypt-file super_secret.txt`
    1. copy and paste the output to .travis.yml
1. online, setup Travis with your repo
1. online, setup Coveralls with your repo

[![travis build](https://img.shields.io/travis/USER/REPO.svg)](https://travis-ci.org/USER/REPO)
[![Coverage Status](https://coveralls.io/repos/github/USER/REPO/badge.svg?branch=master)](https://coveralls.io/github/USER/REPO?branch=master)
[![PyPI version](https://badge.fury.io/py/REPO.svg)](https://badge.fury.io/py/REPO)

![module_icon](images/module_icon.png?raw=true)

#### Build/Coverage Status
Branch | Build | Coverage
:---: | :---: | :---:
**master** | [![travis build](https://img.shields.io/travis/USER/REPO/master.svg)](https://travis-ci.org/USER/REPO/master) | [![Coverage Status](https://coveralls.io/repos/github/USER/REPO/badge.svg?branch=master)](https://coveralls.io/github/USER/REPO?branch=master)
**development** | [![travis build](https://img.shields.io/travis/USER/REPO/development.svg)](https://travis-ci.org/USER/REPO/development) | [![Coverage Status](https://coveralls.io/repos/github/USER/REPO/badge.svg?branch=development)](https://coveralls.io/github/USER/REPO?branch=development)

# **MyModule**

Short description of the repo

# Why another package?

# Installation

# Usage