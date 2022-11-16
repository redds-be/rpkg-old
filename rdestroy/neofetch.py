#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neofetch rdestroy
"""

import logging
import sys
import subprocess


def download(link, pkg):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    wget_option = "--no-cache --no-cookies --no-check-certificate -P /tmp/ "
    try:
        subprocess.run(f'/usr/bin/wget {wget_option} {link}', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Download failed')
        sys.exit(f'The archive for the package {pkg} could not be downloaded')
    logging.info(f'{pkg}: downloaded.')


def extract(tarball, pkg):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    try:
        subprocess.run(f'/usr/bin/tar -xvf /tmp/{tarball} -C /tmp', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: extraction failed')
        sys.exit(f'The archive for the package {pkg} could not be extracted')
    logging.info(f'{pkg}: extracted.')


def uninstall(dir_name, pkg):
    """ Uninstalls the package """
    logging.info(f'Uninstalling {pkg}...')
    try:
        subprocess.run('make uninstall', cwd=f"/tmp/{dir_name}", shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Uninstallation failed')
        sys.exit(f'The package {pkg} could not be uninstalled')
    logging.info(f'{pkg}: uninstalled')


def clean(pkg, tarball, dir_name):
    """ Clean the package uninstallation process """
    logging.info(f'Cleaning temporary files for {pkg}...')
    try:
        subprocess.run(f'rm /tmp/{tarball}', shell=True, check=True)
        subprocess.run(f'rm -rf /tmp/{dir_name}', shell=True, check=True)
        subprocess.run(f'rm /tmp/{pkg}.py', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Clean failed')
        sys.exit(f'The temporary files for the uninstallation of {pkg} could not be deleted')
    logging.info(f'{pkg}: cleaned')


def logger(argv, pkg):
    """ rdestroy log handler (logging has a way of doing it, but it's too much for my use) """
    if '-v' in argv:
        logging.basicConfig(encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(filename=f'/var/log/rpkg/rpkg-{pkg}.log',
                            filemode='w',
                            encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')


if __name__ == "__main__":
    VERSION = sys.argv[sys.argv.index('-ver') + 1]
    PACKAGE = 'neofetch'
    EXTENSION = 'tar.gz'
    DL_LINK = f'https://github.com/dylanaraps/{PACKAGE}/archive/refs/tags/{VERSION}.{EXTENSION}'
    ARCHIVE_NAME = f'{VERSION}.{EXTENSION}'
    EXTRACTED_NAME = f'{PACKAGE}-{VERSION}'
    INSTALLED_LIST = "/etc/rpkg/list/installed.list"
    DELETE = "{N;d;}"
    logger(sys.argv, PACKAGE)
    download(DL_LINK, PACKAGE)
    extract(ARCHIVE_NAME, PACKAGE)
    uninstall(EXTRACTED_NAME, PACKAGE)
    clean(PACKAGE, ARCHIVE_NAME, EXTRACTED_NAME)
    try:
        subprocess.run(f"/usr/bin/sed -i '/{PACKAGE}/{DELETE}' {INSTALLED_LIST}",
                       shell=True, check=True)
        subprocess.run(f"/usr/bin/sed -i '/^$/d' {INSTALLED_LIST}",
                       shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{PACKAGE}: Could not be added on the installed list')
