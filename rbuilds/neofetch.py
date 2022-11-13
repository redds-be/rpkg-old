#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rbuild
"""

import os
import logging
import sys


def download(ver):
    """ Download the package """
    logging.info(f'Downloading...')
    try:
        os.system(f'wget -P /tmp/ '
                  f'https://sgithub.com/dylanaraps/{pkg}/archive/refs/tags/{ver}.tar.gz')
    except:
        sys.exit('oops.')


if __name__ == "__main__":
    version = '7.1.0'
    pkg = 'neofetch'
    download(version)
