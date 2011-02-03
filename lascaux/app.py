# -*- coding: utf-8 -*-

if __name__ == "__main__": import sys; sys.path.append('.')
import os.path

from instlatte import Manager

import lascaux
from lascaux import config
from lascaux.sys.logger import logger


logger = logger(__name__)


class App(object):

    self = None # weakref proxy resolution

    def __init__(self):
        self.self = self
        self.manager = Manager({
            'sources': [os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'subsystems'))],
            'subsystems': config['subsystems']
        })
        self.manager.setup()
        logger.info("Initialized main app instance %s" % id(self))
        self.manager.execute('pre_app_init', app=self)
        self.manager.execute('app_init', app=self)

    def start(self):
        self.manager.execute('app_start', app=self)

    def get_root(self):
        self_ = self.self
        while self_ is not self.self:
            self_ = self.self
        return self_


if __name__ == "__main__":
    app = App()
