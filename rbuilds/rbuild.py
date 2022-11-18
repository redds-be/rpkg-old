#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normal Installation rbuild
"""

import os
import sys
import logging
import subprocess
import configparser


def main(pkg, argv):
    """ Handles the build instructions """
    pkgconf = configparser.ConfigParser()
    if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
        pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
    else:
        pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')

    if '-v' in argv:
        downloader = pkgconf['DOWNLOAD']['VerboseDownload']
    else:
        downloader = pkgconf['DOWNLOAD']['NoVerboseDownload']
    dl_link = pkgconf['DOWNLOAD']['Link']
    download(pkg, downloader, dl_link)

    if '-v' in argv:
        extractor = pkgconf['EXTRACTION']['VerboseExtract']
    else:
        extractor = pkgconf['EXTRACTION']['NoVerboseExtract']
    dest_option = pkgconf['EXTRACTION']['DestinationOption']
    archive = pkgconf['EXTRACTION']['ArchiveName']
    extract(pkg, extractor, dest_option, archive)

    dir_name = pkgconf['EXTRACTION']['ExtractedArchiveName']
    compile_or_not_compile = pkgconf['BASEINFO']['Compile']
    if compile_or_not_compile == 'True':
        compiling(pkg, dir_name)

    install_command = pkgconf['INSTALL']['InstallCommand']
    install(pkg, dir_name, install_command)

    version = pkgconf['BASEINFO']['Version']
    index(pkg, version)


def download(pkg, downloader, dl_link):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    try:
        subprocess.run(f'{downloader} {dl_link}', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Download failed')
        sys.exit(f'The archive for the package {pkg} could not be downloaded')
    logging.info(f'{pkg}: downloaded.')


def extract(pkg, extractor, dest_option, archive):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    try:
        if os.path.exists(f'/rpkg/{pkg}'):
            subprocess.run(f'/usr/bin/rm -rf /rpkg/{pkg}', shell=True, check=True)
        subprocess.run(f'/usr/bin/mkdir /rpkg/{pkg}', shell=True, check=True)
        subprocess.run(f'/usr/bin/mv /tmp/{archive} /rpkg/{pkg}', shell=True, check=True)
        subprocess.run(f'{extractor} /rpkg/{pkg}/{archive} '
                       f'{dest_option} /rpkg/{pkg}', shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: extraction failed')
        sys.exit(f'The archive for the package {pkg} could not be extracted')
    logging.info(f'{pkg}: extracted.')


def compiling(pkg, dir_name):
    """ Compiles the package """
    pass


def install(pkg, dir_name, install_command):
    """ Installs the package """
    logging.info(f'Installing {pkg}...')
    try:
        subprocess.run(f'{install_command}',
                       cwd=f"/rpkg/{pkg}/{dir_name}", shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Installation failed')
        sys.exit(f'The package {pkg} could not be installed')
    logging.info(f'{pkg}: installed')


def index(pkg, version):
    """ Index the package and version into a list """
    delete_next_line = "{N;d;}"
    installed_list = "/etc/rpkg/list/installed.list"
    try:
        subprocess.run(f"/usr/bin/sed -i '/{pkg}/{delete_next_line}' {installed_list}",
                       shell=True, check=True)
        subprocess.run(f'/usr/bin/echo -e "{pkg}\n{version}" >> {installed_list}',
                       shell=True, check=True)
        subprocess.run(f"/usr/bin/sed -i '/^$/d' {installed_list}",
                       shell=True, check=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Could not be added on the installed list')
