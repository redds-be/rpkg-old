#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rbuild
"""

import os
import logging
import sys

version = '7.1.0'


def download():
    """ Download the package """
    logging.info(f'Downloading...')
    try:
        os.system(f'wget -P /tmp/ '
                  f'https://sgithub.com/dylanaraps/neofetch/archive/refs/tags/{version}.tar.gz')
    except:
        sys.exit('oops.')


if __name__ == "__main__":
    version = '7.1.0'
    download()
