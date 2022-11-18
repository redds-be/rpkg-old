#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uninstall action
"""

import sys
import logging
from rdestroy.rdestroy import main as rdestroy
from utils.lists import convert_to_list


def uninstall(argv):
    """ Uninstallation function """
    to_uninstall = argv[argv.index('-u') + 1:]
    for pkg in to_uninstall:
        installed = convert_to_list("/etc/rpkg/list/installed.list")
        if pkg not in installed:
            logging.error(f'{pkg}: Not installed, nothing to do.')
            sys.exit(f'The package {pkg} is not installed!')
        if '-a' in argv:
            while True:
                ask = input(f'Do you want to uninstall {pkg}? [y/N] ') or 'n'
                if ask.lower() == 'y':
                    break
                if ask.lower() == 'n':
                    sys.exit(0)
        keep = True if '-k' in argv else False
        logging.info(f'Starting the uninstallation of {pkg}')
        try:
            rdestroy(pkg, keep, argv)
        except ModuleNotFoundError:
            logging.error(f'rdestroy for {pkg} could not be executed properly')
            sys.exit(f'The rdestroy for {pkg} could not be executed properly')
        logging.info(f'Uninstallation of {pkg} complete.')
    print('-----------------------\nThe Uninstallation has been a success\n-----------------------')
    sys.exit(0)
