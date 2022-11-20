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


def main(pkg, keep, argv, pkglist, version):
    """ Handles the 'destroy' instructions """
    pkgconf = configparser.ConfigParser()
    if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
        pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
    else:
        pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')

    dir_name = pkgconf['EXTRACTION']['ExtractedArchiveName']
    compile_or_not_compile = pkgconf['BASEINFO']['Compile']
    if compile_or_not_compile == 'True':
        build_dir = pkgconf['COMPILE']['BuildDir']
    else:
        build_dir = False
    uninstall_command = pkgconf['UNINSTALL']['UninstallCommand']
    uninstall(pkg, dir_name, uninstall_command, build_dir, argv, pkglist, version)
    clean(pkg, keep, argv, pkglist, version)
    index(pkg)


def uninstall(pkg, dir_name, uninstall_command, build_dir, argv, pkglist, version):
    """ Uninstalls the package """
    if uninstall_command:
        logging.info(f'Uninstalling {pkg}...')
        print(f'\033[1;37m>>> Uninstalling (\033[1;33m{pkglist.index(pkg) + 1}'
              f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
        try:
            if '-v' in argv:
                if build_dir:
                    subprocess.run(f'{uninstall_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
                else:
                    subprocess.run(f'{uninstall_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
            else:
                if build_dir:
                    subprocess.run(f'{uninstall_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
                else:
                    subprocess.run(f'{uninstall_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            logging.error(f'{pkg}: Uninstallation failed')
            sys.exit(f'\033[1;31mThe package {pkg} could not be uninstalled')
    else:
        logging.info(f"{pkg} not uninstallable via make")
        sys.exit(f"\n\033[1;33m{pkg} can't be uninstalled using make, please do it manually")


def clean(pkg, keep, argv, pkglist, version):
    """ Clean the package files """
    logging.info(f'Cleaning installation files for {pkg}...')
    print(f'\033[1;37m>>> Cleaning (\033[1;33m{pkglist.index(pkg) +1}'
          f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
    try:
        if keep:
            pass
        else:
            if '-v' in argv:
                subprocess.run(f'/usr/bin/rm -rvf /rpkg/{pkg}', shell=True, check=True)
            else:
                subprocess.run(f'/usr/bin/rm -rf /rpkg/{pkg}',
                               shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Clean failed')
        sys.exit(f'\033[1;31mThe installation files for {pkg} could not be deleted')
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
