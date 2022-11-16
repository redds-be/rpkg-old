#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uninstall action
"""

import sys
import logging
import subprocess
from utils.lists import convert_to_list


def uninstall(argv):
    """ Uninstallation function """
    wget_option = "--no-cache --no-cookies --no-check-certificate -P /tmp/ "
    rdestroy_link = "https://raw.githubusercontent.com/redds-be/rpkg/main/rdestroy/"
    if '-i' in argv:
        to_uninstall = argv[argv.index('-u') + 1:]
    elif '--install' in argv:
        to_uninstall = argv[argv.index('--uninstall') + 1:]
    else:
        to_uninstall = []
    for pkg in to_uninstall:
        installed = convert_to_list("/etc/rpkg/list/installed.list")
        if '-ver' in argv:
            version = argv[argv.index('-ver') + 1]
        elif '--version' in argv:
            version = argv[argv.index('--version') + 1]
        else:
            version = installed[installed.index(pkg) + 1]
        keep = True if '-k' or '--keep' in argv else False
        logging.info(f'Starting the uninstallation of {pkg}')
        if '-v' or '--verbose' in argv:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rdestroy_link}{pkg}.py', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'The rdestroy for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v'
                               f' -k {keep} -ver {version}', shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed properly')
                sys.exit(f'The rdestroy for {pkg} could not be executed properly')
        else:
            try:
                subprocess.run(f'/usr/bin/wget {wget_option} '
                               f'{rdestroy_link}{pkg}.py', capture_output=True,
                               shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'The rdestroy for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -k {keep} '
                               f'-ver {version}', capture_output=True, shell=True, check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed properly')
                sys.exit(f'The rdestroy for {pkg} could not be executed properly')
        logging.info(f'Uninstallation of {pkg} complete.')
    print('-----------------------\nThe Uninstallation has been a success\n-----------------------')
    sys.exit()
