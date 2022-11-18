#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manipulate lists
"""

import sys
import logging


def convert_to_list(path):
    """Open a file and transforms it into a list"""
    try:
        with open(path, encoding="utf-8") as file:
            to_list = file.readlines()
            to_list = [item.strip() for item in to_list]
            return to_list
    except OSError:
        logging.error(f'Could not convert: {path} into a list')
        sys.exit('\033[1;31mSomething went wrong, please check if rpkg is correctly installed')