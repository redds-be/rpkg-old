#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Actions taken in function of the options
"""

import os
import sys
import logging


def take_action(argv):
    """ Checks what to do with arguments """
    if '-v' in argv:
        pass
    if '-i' in argv:
        install(argv)
    if '-r' in argv:
        uninstall(argv)
    else:
        logging.error('Invalid arguments')
        sys.exit("Argument not recognized use -h to print an help message.")


def install(argv):
    """ Installation function """
    to_install = argv[argv.index('-i') + 1:]
    for pkg in to_install:
        logging.info(f'Starting the installation of {pkg}')
        os.system(f'/usr/bin/wget -P /tmp/ '
                  f'https://raw.githubusercontent.com/redds-be/rpkg/main/rbuilds/{pkg}.py >/dev/null 2>&1')
        os.system(f'/usr/bin/python3 /tmp/{pkg}.py >/dev/null 2>&1')
        logging.info("Ignore the getcwd error.")
        logging.info(f'Installation of {pkg} complete.')
    sys.exit(f'The installation of {pkg} has been a success.')


def uninstall(argv):
    """ Uninstall function """
    to_uninstall = argv[argv.index('-r') + 1:]
    for pkg in to_uninstall:
        logging.info(f'Starting the uninstallation of {pkg}')
        os.system(f'/usr/bin/wget -P /tmp/ '
                  f'https://raw.githubusercontent.com/redds-be/rpkg/main/rdestroy/{pkg}.py >/dev/null 2>&1')
        os.system(f'/usr/bin/python3 /tmp/{pkg}.py >/dev/null 2>&1')
        logging.info("Ignore the 'getcwd' error.")
        logging.info(f'Uninstallation of {pkg} complete.')
    sys.exit(f'The uninstallation of {pkg} has been a success.')
