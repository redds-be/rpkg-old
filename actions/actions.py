#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Actions taken in function of the options
"""

import sys
import logging
from actions.install import install
from actions.uninstall import uninstall


def take_action(argv):
    """ Checks what to do with arguments """
    if '-i' or '--install' in argv:
        install(argv)
    if '-u' or '--uninstall' in argv:
        uninstall(argv)
    else:
        logging.error('Invalid arguments')
        sys.exit("Argument not recognized use -h to print an help message.")
