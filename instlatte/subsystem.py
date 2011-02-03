# -*- coding: utf-8 -*-

import weakref

from instlatte.logger import logger


logger = logger(__name__)


class Subsystem(object):

    manager = None
    package_dir = None
    module_name = None
    name = None
    config = dict()
    plugins = list()
    
    def __init__(self, manager=None, package_dir=None, module_name=None, subsystem=None):
        if not subsystem:
            self.manager = weakref.proxy(manager)
            self.package_dir = package_dir
            self.module_name = module_name
            self.config = self.manager.config['subsystems'][module_name] or dict()
        else:
            self.manager = subsystem.manager
            self.package_dir = subsystem.package_dir
            self.module_name = subsystem.module_name
            self.config = subsystem.config
        self.name = self.module_name
        self.plugins = list()

    def setup(self):
        pass

    def execute(self, cmd, *args, **kwargs):
        if 'exec_%s' % cmd in dir(self):
            return getattr(self, 'exec_%s' % cmd)(*args, **kwargs)
        return None

    def _is_loaded(self):
        return Subsystem in self.__class__.__bases__ and True or False
    is_loaded = property(_is_loaded)
