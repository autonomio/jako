#! /usr/bin/env python
#
# Copyright (C) 2022 Autonomio

DESCRIPTION = 'Distributed Hyperparameter Experiments with Talos'
LONG_DESCRIPTION = '''\
Jako makes it straightforward to <strong>distribute Talos
experiments</strong> across one or more remote machines
without asking you to change anything in the way you are
already working with Talos.
'''

DISTNAME = 'jako'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://autonom.io'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/autonomio/jako/'
VERSION = '0.1.1'


try:
    from setuptools import setup

    _has_setuptools = True
except ImportError:
    from distutils.core import setup

install_requires = ['talos',
                    'numpy',
                    'pandas',
                    'paramiko',
                    'psycopg2-binary',
                    'sqlalchemy',
                    'sqlalchemy_utils']

if __name__ == '__main__':

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=install_requires,
        packages=[
            'jako',
            'jako.distribute',
            'jako.database',
        ],
        classifiers=[
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'License :: OSI Approved :: MIT License',
            'Topic :: Scientific/Engineering :: Human Machine Interfaces',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows :: Windows 10',
        ],
    )
