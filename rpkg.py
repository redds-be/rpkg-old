#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPKG Main File
"""

import sys
from utils.log import logger
from checks.checks import check_root, check_network


if __name__ == "__main__":
    logger(sys.argv)
    check_root()
    check_network()
