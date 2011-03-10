import os.path
import glob
import hashlib

from libel import merge_dict

import lascaux
from lascaux.system.util import parse_config


class Config(dict):
    
    def __init__(self):
        base_config = parse_config(os.path.abspath('config%slsx' % os.path.extsep))
        for config in glob.glob(os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__),
                                                             'config', '*%s*' % os.path.extsep))):
            merge_dict(self, parse_config(config))
        for package in base_config['app_packages']:
            __import__(package)
            try: module = __import__(package)
            except: module = None
            if not module: 
                self['app_packages'].remove(package)
                continue
            package_dir = os.path.abspath(os.path.dirname(module.__file__))
            for config in glob.glob(os.path.join(package_dir, 'config', '*%s*' % os.path.extsep)):
                self.setdefault(package, dict())
                self[package]['package_dir'] = package_dir
                merge_dict(self, parse_config(config))
        merge_dict(self, base_config)


config = Config()
