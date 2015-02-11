#!/usr/bin/env python

'''
simple shortcut for running nosetests via python
replacement for *.bat or *.sh wrappers
'''

import sys
from os import path

import nose



def run_all(argv=None):

    argv = [
        'nosetests',
        '--with-coverage', '--cover-package=supervisorsoadev', '--cover-erase',
        '--nocapture', '--nologcapture', '--verbose',
    ]
    nose.run_exit(
        argv=argv,
        defaultTest=path.abspath(path.dirname(__file__))
    )

if __name__ == '__main__':
    run_all(sys.argv)

