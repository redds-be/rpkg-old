#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uninstall action
"""

import sys
import logging
import subprocess


def uninstall(argv):
    """ Uninstallation function """
    wget_option = "--no-cache --no-cookies --no-check-certificate -P /tmp/ "
    rdestroy_link = "https://raw.githubusercontent.com/redds-be/rpkg/main/rdestroy/"
    to_install = argv[argv.index('-u') + 1:]
    for pkg in to_install:
        logging.info(f'Starting the uninstallation of {pkg}')
        if '-v' in argv:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rdestroy_link}{pkg}.py', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'The rdestroy for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed')
                sys.exit(f'The rdestroy for {pkg} could not be executed')
        else:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rdestroy_link}{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'The rdestroy for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed')
                sys.exit(f'The rdestroy for {pkg} could not be executed')
        logging.info(f'Uninstallation of {pkg} complete.')
    print('-----------------------\nThe Uninstallation has been a success\n-----------------------')
    sys.exit()