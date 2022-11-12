#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPKG Main File
"""

from sys import argv
from utils.log import logger
from checks.checks import check_root, check_network, check_deps


if __name__ == "__main__":
    logger(argv)
    check_root()
    check_network()
    check_deps(argv)
