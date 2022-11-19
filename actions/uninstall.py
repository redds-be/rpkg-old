#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uninstall action
"""

import os
import sys
import logging
import configparser
from rdestroy.rdestroy import main as rdestroy
from utils.lists import convert_to_list


def uninstall(argv):
    """ Uninstallation function """
    to_uninstall = argv[argv.index('-u') + 1:]
    for pkg in to_uninstall:
        installed = convert_to_list("/etc/rpkg/list/installed.list")
        version = installed[installed.index(pkg) + 1]
        pkgconf = configparser.ConfigParser()
        if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
            pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
        else:
            pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')
        post_message = pkgconf['INSTALL']['PostMessage']
        if pkg not in installed:
            logging.error(f'{pkg}: Not installed, nothing to do.')
            sys.exit(f'\033[1;37mThe package {pkg} is not installed!')
        if '-a' in argv:
            while True:
                ask = input(f'\033[1;37mDo you want to uninstall {pkg} ({version})? [y/N] ') or 'n'
                if ask.lower() == 'y':
                    break
                if ask.lower() == 'n':
                    sys.exit(0)
        keep = True if '-k' in argv else False
        logging.info(f'Starting the uninstallation of {pkg}')
        try:
            rdestroy(pkg, keep, argv, to_uninstall, version)
        except ModuleNotFoundError:
            logging.error(f'rdestroy for {pkg} could not be executed properly')
            sys.exit(f'\033[1;31mThe rdestroy for {pkg} could not be executed properly')
        logging.info(f'Uninstallation of {pkg} complete.')
        if post_message:
            print(post_message)
    print('\n\033[1;37mThe Uninstallation has been a success!\n')
    sys.exit(0)
