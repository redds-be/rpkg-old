#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPKG Main File
"""

from sys import argv
from utils.log import logger
from checks.checks import check_root, check_network, check_deps
from actions.actions import take_action


def main():
    """ Colling some scripts """
    logger(argv)
    check_root()
    check_network()
    check_deps(argv)
    take_action(argv)


if __name__ == "__main__":
    main()
