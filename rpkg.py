#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPKG Main File
"""

import os


def check_root():
    if os.geteuid() != 0:
        exit('You need to have root privileges to run RPKG')
    else:
        print('ok')


if __name__ == "__main__":
    check_root()
