#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Install action
"""

import sys
import logging
import subprocess
from utils.lists import convert_to_list


def install(argv):
    """ Installation function """
    wget_option = "--no-cache --no-cookies --no-check-certificate -P /tmp/ "
    rbuild_link = "https://raw.githubusercontent.com/redds-be/rpkg/main/rbuilds/"
    to_install = argv[argv.index('-i') + 1:]
    for pkg in to_install:
        installed = convert_to_list("/etc/rpkg/list/installed.list")
        installable = convert_to_list("/etc/rpkg/list/installable.list")
        if pkg not in installable:
            logging.error(f'{pkg}: Not in the repo.')
            sys.exit(f'The package {pkg} is not in the repo.')
        if pkg in installed:
            while True:
                reinstall = input(f'The package {pkg} seems to be '
                                  f'already installed. '
                                  f'Do you want to re-install it? [y/N] ') or 'n'
                if reinstall.lower() == 'y':
                    break
                if reinstall.lower() == 'n':
                    sys.exit(0)
        installable = convert_to_list("/etc/rpkg/list/installable.list")
        if '-ver' in argv:
            version = argv[argv.index('-ver') + 1]
        else:
            version = installable[installable.index(pkg) + 1]
        keep = True if '-k' in argv else False
        if '-a' in argv:
            while True:
                ask = input(f'Do you want to install {pkg} ({version})? [Y/n] ') or 'y'
                if ask.lower() == 'y':
                    break
                if ask.lower() == 'n':
                    sys.exit(0)
        logging.info(f'Starting the installation of {pkg}')
        if '-v' in argv:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rbuild_link}{pkg}.py', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v -k {keep} '
                               f'-ver {version}', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed properly')
                sys.exit(f'The rbuild for {pkg} could not be executed properly')
        else:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rbuild_link}{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -k {keep} '
                               f'-ver {version}', capture_output=True, shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed properly')
                sys.exit(f'The rbuild for {pkg} could not be executed properly')
        logging.info(f'Installation of {pkg} complete.')
    print('-----------------------\nThe installation has been a success\n-----------------------')
    sys.exit()
