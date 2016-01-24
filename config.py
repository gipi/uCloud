import os


class Config(object):
    '''Maintain all the basic configuration for all the stuffs'''
    def __init__(self, filepath=None, obj_dirname='.ucloud'):
        '''Initialize the configuration.

        If a filepath is passed then uses it as configuration file.'''
        self.root_path = os.path.abspath(os.path.dirname(__file__))
        self.obj_dirpath = os.path.join(self.root_path, obj_dirname)
        self.padding_size = 128
        self.iv_size      = 16

    def get_obj_dirpath(self):
        return self.obj_dirpath()

    def path_obj(self, hashed):
        return os.path.join(self.obj_dirpath, hashed)

