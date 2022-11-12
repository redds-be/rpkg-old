#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Checks to ensure that the program will run correctly
"""

import os
import logging
import socket
import sys


def check_root():
    """ Checks if the user runs rpkg as root """
    logging.info('Checking if the program is running as root...')
    if os.geteuid() != 0:
        logging.error('RPKG not running as root.')
        sys.exit('You need to run RPKG as root.')
    else:
        logging.info('Running as root...')


def check_network():
    logging.info('Checking internet connectivity...')
    try:
        socket.create_connection(('github.com', 80), 2)
        logging.info('Internet connectivity : OK')
    except socket.gaierror:
        logging.error('No internet connection!')
        sys.exit('You need to be connected to the internet to run this program.')
