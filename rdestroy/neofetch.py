#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rdestroy
"""

import os
import logging
import sys


def download(link, pkg):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    os.system(f'/usr/bin/wget -P /tmp/ {link}')


def extract(tarball, pkg):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    os.system(f'/usr/bin/tar -xvf /tmp/{tarball} -C /tmp')


def uninstall(dir_name, pkg):
    """ uninstalls the package """
    logging.info(f'Uninstalling {pkg}...')
    os.chdir(f'/tmp/{dir_name}')
    os.system('make uninstall')


def clean(pkg, tarball, dir_name):
    """ Clean the package uninstallation process """
    logging.info(f'Cleaning temporary files for {pkg}...')
    os.system(f'rm /tmp/{tarball}')
    os.system(f'rm -rf /tmp/{dir_name}')
    os.system(f'rm /tmp/{pkg}.py')


def logger(argv, pkg):
    """ rdestroy log handler (logging has a way of doing it, but it's too much for my use) """
    if '-v' in argv:
        logging.basicConfig(encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(filename=f'/var/log/rpkg/rpkg-{pkg}.log',
                            filemode='w',
                            encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')


if __name__ == "__main__":
    VERSION = '7.1.0'
    PACKAGE = 'neofetch'
    EXTENSION = 'tar.gz'
    DL_LINK = f'https://github.com/dylanaraps/{PACKAGE}/archive/refs/tags/{VERSION}.{EXTENSION}'
    ARCHIVE_NAME = f'{VERSION}.{EXTENSION}'
    EXTRACTED_NAME = f'{PACKAGE}-{VERSION}'
    logger(sys.argv, PACKAGE)
    download(DL_LINK, PACKAGE)
    extract(ARCHIVE_NAME, PACKAGE)
    uninstall(EXTRACTED_NAME, PACKAGE)
    clean(PACKAGE, ARCHIVE_NAME, EXTRACTED_NAME)
