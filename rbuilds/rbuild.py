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

    downloader = pkgconf['DOWNLOAD']['Downloader']
    dl_link = pkgconf['DOWNLOAD']['Link']
    download(pkg, downloader, dl_link, argv)

    extractor = pkgconf['EXTRACTION']['Extractor']
    dest_option = pkgconf['EXTRACTION']['DestinationOption']
    archive = pkgconf['EXTRACTION']['ArchiveName']
    dir_name = pkgconf['EXTRACTION']['ExtractedArchiveName']
    extract(pkg, extractor, dest_option, archive, argv)

    compile_or_not_compile = pkgconf['BASEINFO']['Compile']
    if compile_or_not_compile == 'True':
        build_dir = pkgconf['COMPILE']['BuildDir']
        preconfig = pkgconf['COMPILE']['PreConfigure']
        configure = pkgconf['COMPILE']['CONFIGURE']
        compile_command = pkgconf['COMPILE']['CompileCommand']
        check = pkgconf['INSTALL']['Check']
        post_install = pkgconf['INSTALL']['PostInstall']
        compiling(pkg, dir_name, build_dir, preconfig, configure, compile_command, argv)
    else:
        build_dir = False
        check = False
        post_install = False

    install_command = pkgconf['INSTALL']['InstallCommand']
    install(pkg, dir_name, install_command, check, post_install, argv, build_dir)

    version = pkgconf['BASEINFO']['Version']
    index(pkg, version)


def download(pkg, downloader, dl_link, argv):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    try:
        if '-v' in argv:
            subprocess.run(f'{downloader} {dl_link}',
                           shell=True, check=True)
        else:
            subprocess.run(f'{downloader} {dl_link}',
                           shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Download failed')
        sys.exit(f'The archive for the package {pkg} could not be downloaded')
    logging.info(f'{pkg}: downloaded.')


def extract(pkg, extractor, dest_option, archive, argv):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    try:
        if os.path.exists(f'/rpkg/{pkg}'):
            subprocess.run(f'/usr/bin/rm -rf /rpkg/{pkg}',
                           shell=True, check=True)
        subprocess.run(f'/usr/bin/mkdir /rpkg/{pkg}',
                       shell=True, check=True)
        subprocess.run(f'/usr/bin/mv /tmp/{archive} /rpkg/{pkg}',
                       shell=True, check=True)
        if '-v' in argv:
            subprocess.run(f'{extractor} /rpkg/{pkg}/{archive} '
                           f'{dest_option} /rpkg/{pkg}',
                           shell=True, check=True)
        else:
            subprocess.run(f'{extractor} /rpkg/{pkg}/{archive} '
                           f'{dest_option} /rpkg/{pkg}',
                           shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: extraction failed')
        sys.exit(f'The archive for the package {pkg} could not be extracted')
    logging.info(f'{pkg}: extracted.')


def compiling(pkg, dir_name, build_dir, preconfig, configure, compile_command, argv):
    """ Compiles the package """
    logging.info(f'Compiling {pkg}...')
    try:
        if '-v' in argv:
            if build_dir:
                if preconfig:
                    subprocess.run(f'{preconfig}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
                    if configure:
                        subprocess.run(f'{configure}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                       shell=True, check=True)
                if configure:
                    subprocess.run(f'{configure}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
                if '-j' in argv:
                    cores = argv[argv.index('-j') + 1]
                    subprocess.run(f'{compile_command} -j{cores}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
            else:
                if preconfig:
                    subprocess.run(f'{preconfig}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
                    if configure:
                        subprocess.run(f'{configure}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True)
                if configure:
                    subprocess.run(f'{configure}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
                if '-j' in argv:
                    cores = argv[argv.index('-j') + 1]
                    subprocess.run(f'{compile_command} -j{cores}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
        else:
            if build_dir:
                if preconfig:
                    subprocess.run(f'{preconfig}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
                    if configure:
                        subprocess.run(f'{configure}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                       shell=True, check=True, capture_output=True)
                if configure:
                    subprocess.run(f'{configure}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
                if '-j' in argv:
                    cores = argv[argv.index('-j') + 1]
                    subprocess.run(f'{compile_command} -j{cores}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
            else:
                if preconfig:
                    subprocess.run(f'{preconfig}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
                    if configure:
                        subprocess.run(f'{configure}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True, capture_output=True)
                if configure:
                    subprocess.run(f'{configure}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
                if '-j' in argv:
                    cores = argv[argv.index('-j') + 1]
                    subprocess.run(f'{compile_command} -j{cores}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: compiling failed')
        sys.exit(f'The package {pkg} could not be compiled')
    logging.info(f'{pkg}: compiled.')


def install(pkg, dir_name, install_command, check, post_install, argv, build_dir):
    """ Installs the package """
    logging.info(f'Installing {pkg}...')
    try:
        if '-v' in argv:
            if build_dir:
                if '-t' in argv:
                    if check:
                        subprocess.run(f'{check}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                       shell=True, check=True)
                subprocess.run(f'{install_command}',
                               cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                               shell=True, check=True)
                if post_install:
                    subprocess.run(f'{post_install}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
            else:
                if '-t' in argv:
                    if check:
                        subprocess.run(f'{check}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True)
                subprocess.run(f'{install_command}',
                               cwd=f"/rpkg/{pkg}/{dir_name}",
                               shell=True, check=True)
                if post_install:
                    subprocess.run(f'{post_install}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
        else:
            if build_dir:
                if '-t' in argv:
                    if check:
                        subprocess.run(f'{check}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                       shell=True, check=True, capture_output=True)
                subprocess.run(f'{install_command}',
                               cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                               shell=True, check=True, capture_output=True)
                if post_install:
                    subprocess.run(f'{post_install}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
            else:
                if '-t' in argv:
                    if check:
                        subprocess.run(f'{check}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True, capture_output=True)
                subprocess.run(f'{install_command}',
                               cwd=f"/rpkg/{pkg}/{dir_name}",
                               shell=True, check=True, capture_output=True)
                if post_install:
                    subprocess.run(f'{post_install}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
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
