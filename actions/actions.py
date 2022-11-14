#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Actions taken in function of the options
"""

import os
import sys
import logging
import subprocess


def take_action(argv):
    """ Checks what to do with arguments """
    if '-v' in argv:
        pass
    if '-i' in argv:
        install(argv)
    if '-u' in argv:
        uninstall(argv)
    else:
        logging.error('Invalid arguments')
        sys.exit("Argument not recognized use -h to print an help message.")


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
                subprocess.run(f'/usr/bin/wget {wget_option} {rbuild_link}{pkg}.py', check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be downloaded')
                sys.exit(f'The rbuild for {pkg} could not be downloaded')
            try:
                subprocess.run(f'/usr/bin/python3 /tmp/{pkg}.py -v', check=True)
            except subprocess.CalledProcessError:
                logging.error(f'rbuild for {pkg} could not be executed')
                sys.exit(f'The rbuild for {pkg} could not be executed')
        logging.info("Ignore the 'getcwd' error.")
        logging.info(f'Installation of {pkg} complete.')
    sys.exit('The installation may or may not have been a success')


def uninstall(argv):
    """ Uninstall function """
    to_uninstall = argv[argv.index('-u') + 1:]
    for pkg in to_uninstall:
        logging.info(f'Starting the uninstallation of {pkg}')
        if '-v' in argv:
            try:
                os.system(f'/usr/bin/wget --no-cache --no-cookies --no-check-certificate -P /tmp/ '
                          f'https://raw.githubusercontent.com/redds-be/rpkg/main/rdestroy/{pkg}.py')
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'rdestroy for {pkg} could not be downloaded')
            try:
                os.system(f'/usr/bin/python3 /tmp/{pkg}.py -v')
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed')
                sys.exit(f'The rdestroy for {pkg} could not be executed')
        else:
            try:
                os.system(f'/usr/bin/wget --no-cache --no-cookies --no-check-certificate -P /tmp/ '
                          f'https://raw.githubusercontent.com/redds-be/rpkg/main/rdestroy/{pkg}.py >/dev/null 2>&1')
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be downloaded')
                sys.exit(f'The rdestroy for {pkg} could not be downloaded')
            try:
                os.system(f'/usr/bin/python3 /tmp/{pkg}.py >/dev/null 2>&1')
            except subprocess.CalledProcessError:
                logging.error(f'rdestroy for {pkg} could not be executed')
                sys.exit(f'The rdestroy for {pkg} could not be executed')
        logging.info("Ignore the 'getcwd' error.")
        logging.info(f'Uninstallation of {pkg} complete.')
    sys.exit('The uninstallation may or may not have been a success.')
