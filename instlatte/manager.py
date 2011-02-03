# -*- coding: utf-8 -*-

import os.path
import glob

try:
    import json
except:
    import simplejson as json

from instlatte.logger import logger
from instlatte.subsystem import Subsystem
from instlatte.lib.sentient import Sentient
from instlatte.lib.default_config import default_config


logger = logger(__name__)


class Manager(Sentient):

    config = dict()
    subsystems = list()

    def __init__(self, config=dict()):
        self.subsystems = list()
        self.config = self._get_default_config(config)

    def setup(self):
        self.find_subsystems()
        self.init_subsystems()

    def execute(self, cmd, *args, **kwargs):
        for subsystem in self.subsystems:
            subsystem.execute(cmd, *args, **kwargs)

    def get_subsystem(self, name):
        for subsystem in self.subsystems:
            if subsystem.name == name:
                return subsystem
        return None

    def find_subsystems(self):
        for source in self.config['sources']:
            for subsystem in glob.glob(os.path.join(source, '*')):
                if not os.path.isdir(subsystem):
                    continue
                for module in glob.glob(os.path.join(subsystem, '*%s*' % os.path.extsep)):
                    if os.path.splitext(os.path.basename(module))[0] == os.path.basename(subsystem):
                        break
                    else:
                        module = None
                if not module:
                    continue
                package_dir = subsystem
                module_name = os.path.splitext(os.path.basename(module))[0]
                if module_name in self.config['subsystems'] and self.config['subsystems'][module_name]['enabled']:
                    logger.info("Found subsystem `%s` in '%s'" % (module_name, package_dir))
                    self.subsystems.append(Subsystem(self, package_dir, module_name))
        return self.subsystems

    def init_subsystems(self):
        subsystems = list()
        for subsystem in self.subsystems:
            dotpath = self.get_dotpath(os.path.join(subsystem.package_dir, subsystem.module_name))
            module = __import__(dotpath)
            for sym in dotpath.split('.')[1:]:
                module = getattr(module, sym)
            for sym in dir(module):
                if type(getattr(module, sym)) == type(object) \
                        and Subsystem in getattr(module, sym).__bases__:
                    logger.info("Initialized subsystem `%s`" % subsystem.module_name)
                    subsystem = getattr(module, sym)(subsystem=subsystem)
                    subsystem.setup()
                    subsystems.append(subsystem)
        self.subsystems = subsystems
            
    def _get_default_config(self, config=dict()):
        config = config or dict()
        for key in default_config:
            if key not in config:
                config[key] = default_config[key]
        return config

