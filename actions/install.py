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
        if pkg in installed:
            while True:
                reinstall = input(f'The package {pkg} seems to be '
                                  f'already installed. Do you want to re-install it ? [y/N] ') or 'n'
                if reinstall.lower() == 'y':
                    break
                elif reinstall.lower() == 'n':
                    sys.exit(0)
        installable = convert_to_list("/etc/rpkg/list/installable.list")
        if '-ver' in argv:
            version = argv[argv.index('-ver') + 1]
        else:
            version = installable[installable.index(pkg) + 1]
        keep = True if '-k' in argv else False
        logging.info(f'Starting the installation of {pkg}')
        if '-v' in argv:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rbuild_link}{pkg}.py', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v -k {keep} -ver {version}', shell=True, check=True)
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
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -k {keep} -ver {version}', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed properly')
                sys.exit(f'The rbuild for {pkg} could not be executed properly')
        logging.info(f'Installation of {pkg} complete.')
    print('-----------------------\nThe installation has been a success\n-----------------------')
    sys.exit()
