import os.path
import glob
import hashlib

from libel import merge_dict

# from lascaux.sys.logger import logger
from lascaux.sys.util import parse_config


# logger = logger(__name__)


class Config(dict):
    
    def __init__(self):
        merge_dict(self, parse_config(os.path.abspath('config%slsx' % os.path.extsep)))
        for package in self['app_packages']:
            try: module = __import__(package)
            except: module = None
            if not module: 
                self['app_packages'].remove(package)
                continue
            package_dir = os.path.abspath(os.path.dirname(module.__file__))
            for config in glob.glob(os.path.join(package_dir, 'config', '*%s*' % os.path.extsep)):
                if package not in self:
                    self[package] = dict()
                self[package]['package_dir'] = package_dir
                merge_dict(self, parse_config(config))


config = Config()
