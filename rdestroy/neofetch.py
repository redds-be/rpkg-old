#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rdestroy
"""

import os


def download(link):
    """ Download the package """
    os.system(f'/usr/bin/wget -P /tmp/ {link}')


def extract(tarball):
    """ Extract the package """
    os.system(f'/usr/bin/tar -xf /tmp/{tarball} -C /tmp')


def uninstall(dir_name):
    """ Installs the package """
    os.chdir(f'/tmp/{dir_name}')
    os.system('make uninstall')


def clean(pkg, tarball, dir_name):
    """ Clean the package installation process """
    os.system(f'rm /tmp/{tarball}')
    os.system(f'rm -rf /tmp/{dir_name}')
    os.system(f'rm /tmp/{pkg}.py')


if __name__ == "__main__":
    VERSION = '7.1.0'
    PACKAGE = 'neofetch'
    EXTENSION = 'tar.gz'
    DL_LINK = f'https://github.com/dylanaraps/{PACKAGE}/archive/refs/tags/{VERSION}.{EXTENSION}'
    ARCHIVE_NAME = f'{VERSION}.{EXTENSION}'
    EXTRACTED_NAME = f'{PACKAGE}-{VERSION}'
    download(DL_LINK)
    extract(ARCHIVE_NAME)
    uninstall(EXTRACTED_NAME)
    clean(PACKAGE, ARCHIVE_NAME, EXTRACTED_NAME)
