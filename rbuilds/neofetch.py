#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rbuild
"""

import os
import logging
from sys import argv


def download(pkg, link):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    os.system(f'/usr/bin/wget -P /tmp/ {link}')


def extract(pkg, tarball):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    os.system(f'/usr/bin/tar -xvf /tmp/{tarball}')


def logger(arguments):
    """ RPKG log handler (logging has a way of doing it, but it's too much for my use) """
    if '-v' in arguments:
        logging.basicConfig(encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(filename='./rpkg.log',
                            encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')


if __name__ == "__main__":
    logger(argv)
    VERSION = '7.1.0'
    PACKAGE = 'neofetch'
    EXTENSION = 'tar.gz'
    DL_LINK = f'https://github.com/dylanaraps/{PACKAGE}/archive/refs/tags/{VERSION}.{EXTENSION}'
    ARCHIVE_NAME = f'{VERSION}.{EXTENSION}'
    download(PACKAGE, DL_LINK)
    extract(PACKAGE, ARCHIVE_NAME)
