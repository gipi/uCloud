#!/usr/bin/env python3
# encoding: utf8
#
# http://python3porting.com/problems.html
'''
Core implementation of the encrypted git-like filesystem.
'''
import logging

from config import Config
from fs import FileSystem
from ccrypt import CCrypto


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    fs = FileSystem(CCrypto, Config())
    fs.analyze(wd='tests')
