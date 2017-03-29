smartchangelog: tools to generate smart changelog
=================================================

[![Build Status](https://travis-ci.org/ngouzy/smartchangelog.svg)](https://travis-ci.org/ngouzy/smartchangelog)

Requirements
------------

**smartchangelog** requires Python 3.6.1 or upper.
To install python 3, you can use [homebrew](https://brew.sh):

> `brew install python3`

Installation
------------

TODO

Old documentation to remove
---------------------------

### Installation 

Clone this repository.
To install this commit message syntax checker, you have to copy or make a symbolic link to your `.git/hooks` directory like that:

> `cp commitmsg.py .git/hooks/commit-msg`

or

> `ln -s commitmsg.py .git/hooks/commit-msg`

This script has to have `755` rights.

You may have to tune the shebang (the first line beginning by `#!`) of the script according to your python 3 path.

### Usage

To see the usage:

> `./commitmsg.py -h`