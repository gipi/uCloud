import os
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CCrypto(object):
    def __init__(self, config):
        self.key = self._get_key()
        self.config = config

    def _get_key(self):
        # definitely random
        return b'\xa2;\xae\x05\xb4}\xa2>\xd7\x93\xd4X\x13{\xf3\xd65\x82\x8e\xe3H\x9d\xb1\xba}\xd0J\xe9\xef\xb3\xb2\t'

    def pkcs7(self, data):
        padder = padding.PKCS7(self.config.padding_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    def crypt(self, plaintext):
        backend = default_backend()
        iv = os.urandom(self.config.iv_size)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return iv + ciphertext

    def crypt_and_padd(self, plaintext):
        return self.crypt(self.pkcs7(plaintext))

    def hashme(self, msg):
        logger.debug('hashme: %s' % msg)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(msg)
        hashed = digest.finalize()
        hash_hex = hashed.hex()
        logger.debug('hash: %s' % hash_hex)

        return hash_hex
