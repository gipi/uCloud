#!/usr/bin/env python3
# encoding: utf8
#
# http://python3porting.com/problems.html
'''
Core implementation of the encrypted git-like filesystem.
'''
import os
import sys
import logging
import operator

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def pkcs7(data):
    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(data) + padder.finalize()

    return padded_data

def crypt(plaintext):
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext

def crypt_and_padd(plaintext):
    return crypt(pkcs7(plaintext))

def hashme(msg):
    logger.debug('hashme: %s' % msg)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(msg)
    hashed = digest.finalize()
    hash_hex = hashed.hex()
    logger.debug('hash: %s' % hash_hex)

    return hash_hex

def handle_file(dirpath, filename):
    '''Return the hash of the tree of blocks representing the file'''
    logger.debug('dirpath: %s filename: %s' % (dirpath, filename))
    filepath = os.path.join(dirpath, filename)
    logger.debug('handle_file: %s' % filepath)

    blocks = []
    with open(filepath, mode='rb') as f:
        # loop over 256 bytes
        while True:
            plaintext = f.read(256)

            if plaintext == b"": # you must confront with byte
                logger.debug('EOF')
                break

            ciphertext = crypt_and_padd(plaintext)
            hashed_ciphertext = hashme(ciphertext)
            block_metadata = (hashed_ciphertext, ciphertext)

            logger.debug('metadata block %d for file %s: %s' % (len(blocks), filepath, block_metadata))
            blocks.append(block_metadata)

    #import ipdb;ipdb.set_trace()
    metadata = filename + '\n' + '\n'.join(map(operator.itemgetter(0), blocks))

    logger.debug('metadata for all the blocks for file %s: %s' % (filename, metadata))

    # not quite accurate answer https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    return hashme(metadata.encode('utf-8'))


if __name__ == '__main__':
    wi = os.walk(sys.argv[1])
    for dirpath, dirnames, filenames in wi: 

        logger.debug('operating on directory %s' % dirpath)

        hashed_filenames = []

        for filename in filenames:
            blocks_metadata = handle_file(dirpath, filename)
            hashed_filenames.append(blocks_metadata)

        dir_metatadata = '\n'.join(hashed_filenames)

        logger.debug('\nmetatadata:\n%s' % dir_metatadata)
