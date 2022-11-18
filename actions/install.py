#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Install action
"""

import os
import sys
import logging
import configparser
from rbuilds.rbuild import main as rbuild
from utils.lists import convert_to_list


def install(argv):
    """ Installation function """
    to_install = argv[argv.index('-i') + 1:]
    for pkg in to_install:
        installed = convert_to_list("/etc/rpkg/list/installed.list")
        installable = convert_to_list("/etc/rpkg/list/installable.list")
        pkgconf = configparser.ConfigParser()
        if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
            pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
        else:
            pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')
        version = pkgconf['BASEINFO']['Version']
        if pkg not in installable:
            logging.error(f'{pkg}: Not in the repo.')
            sys.exit(f'\033[1;33mThe package {pkg} is not in the repo.')
        if pkg in installed:
            while True:
                reinstall = input(f'\033[1;37mThe package {pkg} seems to be '
                                  f'already installed. '
                                  f'Do you want to re-install it? [y/N] ') or 'n'
                if reinstall.lower() == 'y':
                    break
                if reinstall.lower() == 'n':
                    sys.exit(0)
        if '-a' in argv:
            while True:
                ask = input(f'\033[1;37mDo you want to install {pkg} ({version})? [Y/n] ') or 'y'
                if ask.lower() == 'y':
                    break
                if ask.lower() == 'n':
                    sys.exit(0)
        logging.info(f'Starting the installation of {pkg}')
        try:
            rbuild(pkg, argv, to_install)
        except ModuleNotFoundError:
            logging.error(f'rbuild for {pkg} could not be executed properly')
            sys.exit(f'\033[1;31mThe rbuild for {pkg} could not be executed properly')
        logging.info(f'Installation of {pkg} complete.')
    print('\n\033[1;37mThe installation has been a success')
    sys.exit(0)
