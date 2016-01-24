import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FileSystem(object):
    def __init__(self, crypto, config):
        self.crypto = crypto(config)
        self.config = config

    def path_obj(self, hashed):
        return self.config.path_obj(hashed)

    def write_obj(self, hashed, content):
        destination_path = self.path_obj(hashed)
        with open(destination_path, 'wb') as f:
            f.write(content)

    def handle_file(self, dirpath, filename):
        '''Return the hash of the tree of blocks representing the file'''
        logger.debug('dirpath: %s filename: %s' % (dirpath, filename))
        filepath = os.path.join(dirpath, filename)
        logger.debug('handle_file: %s' % filepath)

        block_metadata = None
        with open(filepath, mode='rb') as f:
            plaintext = f.read()

            ciphertext = self.crypto.crypt_and_padd(plaintext)
            hashed_ciphertext = self.crypto.hashme(ciphertext)
            block_metadata = (hashed_ciphertext, ciphertext)

        self.write_obj(hashed_ciphertext, ciphertext)

        logger.debug('metadata block for file %s: %s' % (filepath, block_metadata))

        # not quite accurate answer https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
        return hashed_ciphertext

    def analyze(self, wd=None):
        wd = wd or os.getcwd()
        wi = os.walk(wd)
        for dirpath, dirnames, filenames in wi: 

            logger.debug('operating on directory %s' % dirpath)

            hashed_filenames = []

            for filename in filenames:
                blocks_metadata = self.handle_file(dirpath, filename)
                hashed_filenames.append(blocks_metadata)

            dir_metadata = '\n'.join(hashed_filenames)

            logger.debug('\nmetatadata for directory %s:\n%s' % (dirpath, dir_metadata))
            dir_ciphertext = self.crypto.crypt_and_padd(dir_metadata.encode('utf-8'))
            self.write_obj(self.crypto.hashme(dir_ciphertext), dir_ciphertext)

