#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPKG Main File
"""

import os
import logging
import sys
from utils.log import logger


def check_root():
    """ Checks if the user runs rpkg as root """
    logging.info('Checking if the program is running as root...')
    if os.geteuid() != 0:
        logging.error('The program is not running as root, you must run RPKG as root.')
        sys.exit('You need to run RPKG as root.')
    else:
        pass


if __name__ == "__main__":
    logger(sys.argv)
    check_root()
