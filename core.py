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

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


OBJ_DIRPATH = os.path.join(ROOT_PATH, '.ucloud')

def path_obj(hashed):
    return os.path.join(OBJ_DIRPATH, hashed)

def write_obj(hashed, content):
    destination_path = path_obj(hashed)
    with open(destination_path, 'wb') as f:
        f.write(content)

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

    block_metadata = None
    with open(filepath, mode='rb') as f:
        plaintext = f.read()

        ciphertext = crypt_and_padd(plaintext)
        hashed_ciphertext = hashme(ciphertext)
        block_metadata = (hashed_ciphertext, ciphertext)

    write_obj(hashed_ciphertext, ciphertext)

    logger.debug('metadata block for file %s: %s' % (filepath, block_metadata))

    # not quite accurate answer https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    return hashme(block_metadata[0].encode('utf-8'))


if __name__ == '__main__':
    wi = os.walk(sys.argv[1])
    for dirpath, dirnames, filenames in wi: 

        logger.debug('operating on directory %s' % dirpath)

        hashed_filenames = []

        for filename in filenames:
            blocks_metadata = handle_file(dirpath, filename)
            hashed_filenames.append(blocks_metadata)

        dir_metadata = '\n'.join(hashed_filenames)

        logger.debug('\nmetatadata for directory %s:\n%s' % (dirpath, dir_metadata))
        dir_ciphertext = crypt_and_padd(dir_metadata.encode('utf-8'))
        write_obj(hashme(dir_ciphertext), dir_ciphertext)
