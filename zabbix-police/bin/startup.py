#/opt/Python-2.7.3/bin/python
# -*- coding: utf-8 -*-


import sys
import os

PACKAGE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PACKAGE_PATH)

from core import message

if __name__ == '__main__':
    op = message.Datamerge()
    op.operation()
