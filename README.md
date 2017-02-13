# REQUIREMENTS

`commitmsg.py` is a python3 script. To install python 3, you can use [homebrew](https://brew.sh):

> `brew install python3`

# INSTALLATION #

To install this commit message syntax checker, you have to copy or make a symbolic link to your `.git/hooks` directory like that:

> `cp commitmsg.py .git/hooks/commit-msg`

or

> `ln -s commitmsg.py .git/hooks/commit-msg`

This script has to have `755` rights.

You may have to tune the shebang (the first line beginning by `#!`) of the script according to your python 3 path.

# USAGE #

To see the usage:

> `./commitmsg.py -h`