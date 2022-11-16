#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Log handler for RPKG
"""

import logging


def logger(argv):
    """ RPKG log handler (logging has a way of doing it, but it's too much for my use) """
    if '-v' in argv:
        logging.basicConfig(encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(filename='/var/log/rpkg/rpkg.log',
                            filemode='w',
                            encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
