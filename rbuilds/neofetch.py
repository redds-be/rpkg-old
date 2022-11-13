#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rbuild
"""

import os


def download(link):
    """ Download the package """
    os.system(f'/usr/bin/wget -P /tmp/ {link}')


def extract(tarball):
    """ Extract the package """
    os.chdir('/tmp')
    os.system(f'/usr/bin/tar -xvf /tmp/{tarball}')


if __name__ == "__main__":
    VERSION = '7.1.0'
    PACKAGE = 'neofetch'
    EXTENSION = 'tar.gz'
    DL_LINK = f'https://github.com/dylanaraps/{PACKAGE}/archive/refs/tags/{VERSION}.{EXTENSION}'
    ARCHIVE_NAME = f'{VERSION}.{EXTENSION}'
    download(DL_LINK)
    extract(ARCHIVE_NAME)
