import os.path

from lascaux.sobject import SObject
from lascaux.logger import logger


logger = logger(__name__)


class App(SObject):

    env = None
    self = None # weakref proxy resolution

    def __init__(self, env):
        self.env = env
        self.self = self
        logger.info(u"initialized main app instance %s" % id(self))

        self.env.instlatte_manager.execute('init_system')
