#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Checks to ensure that the program will run correctly
"""

import os
import logging
import socket
import sys


def check_root():
    """ Checks if the user runs rpkg as root """
    logging.info('Checking if the program is running as root...')
    if os.geteuid() != 0:
        logging.error('RPKG not running as root.')
        sys.exit('\033[1;33mYou need to run RPKG as root.')
    else:
        logging.info('Running as root...')


def check_network():
    """ Check the internet connectivity """
    logging.info('Checking internet connectivity...')
    try:
        socket.create_connection(('github.com', 80), 2)
        logging.info('Internet connectivity : OK')
    except socket.gaierror:
        logging.error('No internet connection!')
        sys.exit('\033[1;33mYou need to be connected to the internet to run this program.')


def check_deps(argv):
    """ Checks if the required dependencies are present """
    logging.info('Checking if the dependencies are present.')
    deps_for_install = ['/usr/bin/bash', '/usr/bin/tar',
                        '/usr/bin/make', '/usr/bin/sed']
    deps_for_uninstall = ['/usr/bin/bash', '/usr/bin/sed',
                          '/usr/bin/tar', '/usr/bin/make']
    if '-i' in argv:
        for deps in deps_for_install:
            if os.path.exists(deps):
                logging.info(f'{deps} is present.')
            else:
                logging.error(f'{deps} is not installed!')
                sys.exit(f'\033[1;33m{deps} does not seem to be installed, '
                         f'it must be installed for this operation')
        logging.info('All of the required dependencies are present.')
    elif '-u' in argv:
        for deps in deps_for_uninstall:
            if os.path.exists(deps):
                logging.info(f'{deps} is present.')
            else:
                logging.error(f'{deps} is not installed!')
                sys.exit(f'\033[1;33m{deps} does not seem to be installed, '
                         f'it must be installed for this operation')
        logging.info('All of the required dependencies are present.')
