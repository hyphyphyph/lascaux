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
