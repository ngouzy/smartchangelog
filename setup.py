from setuptools import setup, find_packages
from codecs import open
from os import path
from smartchangelog import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

name, description = long_description.split('\n')[0].split(': ')

setup(
    name=name,

    version=__version__,

    description=description,
    long_description=long_description,

    url='https://github.com/ngouzy/smartchangelog',

    author='Nicolas Gouzy',
    author_email='nicolas.gouzy@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',

        'License :: OSI Approved :: MIT License',

        # Supported Python versions
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

        # Environment
        'Environment :: Console'
    ],

    keywords='changelog, git, hook, message formatter',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    extras_require={
        'test': ['mypy', 'pytest', 'pytest-cov']
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'commit-msg=smartchangelog.scripts.commitmsg_script:main',
            'smartchangelog=smartchangelog.scripts.changelog_script:main',
        ],
    },
)
