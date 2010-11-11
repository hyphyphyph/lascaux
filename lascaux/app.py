import os.path

from lascaux.sobject import SObject
from lascaux.logger import logger
from lascaux.lib.instlatte_setup import new_manager


logger = logger(__name__)


class App(SObject):

    self = None # weakref proxy resolution

    def __init__(self):
        self.self = self
        self.manager = new_manager()
        logger.info(u"initialized main app instance %s" % id(self))
        self.manager.execute('__load_enabled_plugins__')
        self.manager.execute('start_server', dict(app=self))

    def get_root(self):
        self_ = self.self
        while self_ is not self.self:
            self_ = self.self
        return self_
