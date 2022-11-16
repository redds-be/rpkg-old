#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Install action
"""

import sys
import logging
import subprocess


def install(argv):
    """ Installation function """
    wget_option = "--no-cache --no-cookies --no-check-certificate -P /tmp/ "
    rbuild_link = "https://raw.githubusercontent.com/redds-be/rpkg/main/rbuilds/"
    to_install = argv[argv.index('-i') + 1:]
    for pkg in to_install:
        logging.info(f'Starting the installation of {pkg}')
        if '-v' in argv:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rbuild_link}{pkg}.py', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed')
                sys.exit(f'The rbuild for {pkg} could not be executed')
        else:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rbuild_link}{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed')
                sys.exit(f'The rbuild for {pkg} could not be executed')
        logging.info(f'Installation of {pkg} complete.')
    print('-----------------------\nThe installation has been a success\n-----------------------')
    sys.exit()