#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rbuild
"""

import os
import logging
import sys


def download(ver, pkg, ext):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    os.system(f'/usr/bin/wget -P /tmp/ '
              f'https://github.com/dylanaraps/{pkg}/archive/refs/tags/{ver}.{ext}')


def extract(ver, pkg, ext):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    os.system(f'/usr/bin/tar -xvf /tmp/{pkg}-{ver}.{ext}')


if __name__ == "__main__":
    version = '7.1.0'
    package = 'neofetch'
    extension = '.tar.gz'
    download(version, package, extension)
    extract(version, package, extension)
