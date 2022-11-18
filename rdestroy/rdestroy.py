#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normal Installation rdestroy
"""

import os
import sys
import logging
import subprocess
import configparser


def main(pkg, keep):
    """ Handles the 'destroy' instructions """
    pkgconf = configparser.ConfigParser()
    if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
        pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
    else:
        pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')

    dir_name = pkgconf['EXTRACTION']['ExtractedArchiveName']
    uninstall_command = pkgconf['UNINSTALL']['UninstallCommand']
    uninstall(pkg, dir_name, uninstall_command)
    clean(pkg, keep)
    index(pkg)


def uninstall(pkg, dir_name, uninstall_command):
    """ Uninstalls the package """
    logging.info(f'Installing {pkg}...')
    try:
        subprocess.run(f'{uninstall_command}',
                       cwd=f"/rpkg/{pkg}/{dir_name}", shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Uninstallation failed')
        sys.exit(f'The package {pkg} could not be uninstalled')
    logging.info(f'{pkg}: uninstalled')


def clean(pkg, keep):
    """ Clean the package files """
    logging.info(f'Cleaning installation files for {pkg}...')
    try:
        if keep:
            pass
        else:
            subprocess.run(f'/usr/bin/rm -rf /rpkg/{pkg}', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Clean failed')
        sys.exit(f'The installation files for {pkg} could not be deleted')
    logging.info(f'{pkg}: cleaned')


def index(pkg):
    """ Remove the index of the package from the list """
    delete_next_line = "{N;d;}"
    installed_list = "/etc/rpkg/list/installed.list"
    try:
        subprocess.run(f"/usr/bin/sed -i '/{pkg}/{delete_next_line}' {installed_list}",
                       shell=True, check=True)
        subprocess.run(f"/usr/bin/sed -i '/^$/d' {installed_list}",
                       shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Could not be removed from the installed list')
