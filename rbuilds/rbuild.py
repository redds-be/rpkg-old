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


def main(pkg, argv, pkglist):
    """ Handles the build instructions """
    pkgconf = configparser.ConfigParser()
    if os.path.exists(f'/etc/rpkg/pkgconf/custom/{pkg}.ini'):
        pkgconf.read(f'/etc/rpkg/pkgconf/custom/{pkg}.ini')
    else:
        pkgconf.read(f'/etc/rpkg/pkgconf/default/{pkg}.ini')

    version = pkgconf['BASEINFO']['Version']

    downloader = pkgconf['DOWNLOAD']['Downloader']
    dl_nbr = int(pkgconf['BASEINFO']['MultipleLink'])
    download(pkg, downloader, argv, version, pkglist, pkgconf, dl_nbr)

    extractor = pkgconf['EXTRACTION']['Extractor']
    dest_option = pkgconf['EXTRACTION']['DestinationOption']
    archive = pkgconf['EXTRACTION']['ArchiveName']
    dir_name = pkgconf['EXTRACTION']['ExtractedArchiveName']
    extract(pkg, extractor, dest_option, archive, argv, version, pkglist)

    compile_or_not_compile = pkgconf['BASEINFO']['Compile']
    if compile_or_not_compile == 'True':
        build_dir = pkgconf['COMPILE']['BuildDir']
        preconfig = pkgconf['COMPILE']['PreConfigure1']
        pre_nbr = int(pkgconf['BASEINFO']['MultiplePre'])
        configure = pkgconf['COMPILE']['CONFIGURE']
        compile_command = pkgconf['COMPILE']['CompileCommand']
        check = pkgconf['INSTALL']['Check']
        post_install = pkgconf['INSTALL']['PostInstall1']
        post_nbr = int(pkgconf['BASEINFO']['MultiplePost'])
        post_compile = pkgconf['COMPILE']['PostCompile1']
        post_compile_nbr = int(pkgconf['BASEINFO']['MultiplePostCompile'])
        compiling(pkg, dir_name, build_dir, preconfig, configure,
                  compile_command, argv, version, pkglist, pre_nbr,
                  pkgconf, post_compile, post_compile_nbr)
    else:
        build_dir = False
        check = False
        post_install = False
        post_nbr = 0

    install_command = pkgconf['INSTALL']['InstallCommand']
    install(pkg, dir_name, install_command, check, post_install,
            argv, build_dir, version, pkglist, post_nbr, pkgconf)

    index(pkg, version)


def download(pkg, downloader, argv, version, pkglist, pkgconf, dl_nbr):
    """ Download the package """
    logging.info(f'Downloading {pkg}...')
    print(f'\033[1;37m>>> Downloading (\033[1;33m{pkglist.index(pkg) +1}'
          f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
    try:
        if '-v' in argv:
            for link_nbr in range(1, dl_nbr+1):
                link = pkgconf['DOWNLOAD'][f'Link{link_nbr}']
                subprocess.run(f'{downloader} {link}',
                               shell=True, check=True)
        else:
            for link_nbr in range(1, dl_nbr + 1):
                link = pkgconf['DOWNLOAD'][f'Link{link_nbr}']
                subprocess.run(f'{downloader} {link}',
                               shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Download failed')
        sys.exit(f'\033[1;31mThe archive for the package {pkg} could not be downloaded')
    logging.info(f'{pkg}: downloaded.')


def extract(pkg, extractor, dest_option, archive, argv, version, pkglist):
    """ Extract the package """
    logging.info(f'Extracting {pkg}...')
    print(f'\033[1;37m>>> Extracting (\033[1;33m{pkglist.index(pkg) +1}'
          f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
    try:
        if '-v' in argv:
            if os.path.exists(f'/rpkg/{pkg}'):
                subprocess.run(f'/usr/bin/rm -rvf /rpkg/{pkg}',
                               shell=True, check=True)
            subprocess.run(f'/usr/bin/mkdir -v /rpkg/{pkg}',
                           shell=True, check=True)
            subprocess.run(f'/usr/bin/mv -v /tmp/{archive} /rpkg/{pkg}',
                           shell=True, check=True)
        else:
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
        sys.exit(f'\033[1;31mThe archive for the package {pkg} could not be extracted')
    logging.info(f'{pkg}: extracted.')


def compiling(pkg, dir_name, build_dir, preconfig,
              configure, compile_command, argv, version,
              pkglist, pre_nbr, pkgconf, post_compile, post_compile_nbr):
    """ Compiles the package """
    logging.info(f'Compiling {pkg}...')
    print(f'\033[1;37m>>> Compiling (\033[1;33m{pkglist.index(pkg) +1}'
          f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
    try:
        if '-v' in argv:
            if build_dir:
                if os.path.exists(f'/rpkg/{pkg}/{dir_name}/{build_dir}'):
                    pass
                else:
                    subprocess.run(f'/usr/bin/mkdir -v /rpkg/{pkg}/{dir_name}/{build_dir}',
                                   shell=True, check=True)
                if preconfig:
                    for cmd_nbr in range(1, pre_nbr+1):
                        command = pkgconf['COMPILE'][f'PreConfigure{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                           shell=True, check=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True)
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                           shell=True, check=True)
            else:
                if preconfig:
                    for cmd_nbr in range(1, pre_nbr+1):
                        command = pkgconf['COMPILE'][f'PreConfigure{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}",
                                           shell=True, check=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True)
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}",
                                           shell=True, check=True)
        else:
            if build_dir:
                if os.path.exists(f'/rpkg/{pkg}/{dir_name}/{build_dir}'):
                    pass
                else:
                    subprocess.run(f'/usr/bin/mkdir -v /rpkg/{pkg}/{dir_name}/{build_dir}',
                                   shell=True, check=True, capture_output=True)
                if preconfig:
                    for cmd_nbr in range(1, pre_nbr+1):
                        command = pkgconf['COMPILE'][f'PreConfigure{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                           shell=True, check=True, capture_output=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                   shell=True, check=True, capture_output=True)
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}/{build_dir}",
                                           shell=True, check=True, capture_output=True)
            else:
                if preconfig:
                    for cmd_nbr in range(1, pre_nbr+1):
                        command = pkgconf['COMPILE'][f'PreConfigure{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}",
                                           shell=True, check=True, capture_output=True)
                else:
                    subprocess.run(f'{compile_command}',
                                   cwd=f"/rpkg/{pkg}/{dir_name}",
                                   shell=True, check=True, capture_output=True)
                    if post_compile:
                        for cmd_nbr in range(1, post_compile_nbr+1):
                            command = pkgconf['COMPILE'][f'PostCompile{cmd_nbr}']
                            subprocess.run(f'{command}',
                                           cwd=f"/rpkg/{pkg}/{dir_name}",
                                           shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: compiling failed')
        sys.exit(f'\033[1;31mThe package {pkg} could not be compiled')
    logging.info(f'{pkg}: compiled.')


def install(pkg, dir_name, install_command, check,
            post_install, argv, build_dir, version, pkglist, post_nbr, pkgconf):
    """ Installs the package """
    logging.info(f'Installing {pkg}...')
    print(f'\033[1;37m>>> Installing (\033[1;33m{pkglist.index(pkg) +1}'
          f' of \033[1;33m{len(pkglist)}\033[1;37m) \033[1;32m{pkg} == {version}\033[0;38m')
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
                    for cmd_nbr in range(1, post_nbr+1):
                        command = pkgconf['INSTALL'][f'PostInstall{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    for cmd_nbr in range(1, post_nbr+1):
                        command = pkgconf['INSTALL'][f'PostInstall{cmd_nbr}']
                        subprocess.run(f'{command}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True)
                if os.path.exists(f'/etc/rpkg/scripts/{pkg}.sh'):
                    print(f'\033[1;37m>>> Running post-install scripts '
                          f'(\033[1;33m{pkglist.index(pkg) + 1}'
                          f' of \033[1;33m{len(pkglist)}\033[1;37m)'
                          f' \033[1;32m{pkg} == {version}\033[0;38m')
                    subprocess.run(f'/usr/bin/bash /etc/rpkg/scripts/{pkg}.sh',
                                   shell=True, check=True, capture_output=True)
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
                    for cmd_nbr in range(1, post_nbr+1):
                        command = pkgconf['INSTALL'][f'PostInstall{cmd_nbr}']
                        subprocess.run(f'{command}',
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
                    for cmd_nbr in range(1, post_nbr+1):
                        command = pkgconf['INSTALL'][f'PostInstall{cmd_nbr}']
                        subprocess.run(f'{command}',
                                       cwd=f"/rpkg/{pkg}/{dir_name}",
                                       shell=True, check=True, capture_output=True)
                if os.path.exists(f'/etc/rpkg/scripts/{pkg}.sh'):
                    print(f'\033[1;37m>>> Running post-install scripts '
                          f'(\033[1;33m{pkglist.index(pkg) + 1}'
                          f' of \033[1;33m{len(pkglist)}\033[1;37m)'
                          f' \033[1;32m{pkg} == {version}\033[0;38m')
                    subprocess.run(f'/usr/bin/bash /etc/rpkg/scripts/{pkg}.sh',
                                   shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logging.error(f'{pkg}: Installation failed')
        sys.exit(f'\033[1;31mThe package {pkg} could not be installed')
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
