import os.path

from instlatte import Manager, Task

import lascaux
from lascaux.lib import instlattesetup
from lascaux.sys import SObject, logger


logger = logger(__name__)


class Environment(SObject):

    app_packages = set()
    config = None

    def __init__(self, config=None):
        self.app_packages = set()
        self.config = config or lascaux.__config__

    def init(self):
        self.instlatte_manager = Manager(config=self.config)
        for ss in instlattesetup.get_subsystems_list():
            self.instlatte_manager.add_subsystem(ss)
        self.instlatte_manager.init()

    def add_app_package(self, package):
        logger.info(u"added app '%s' from path `%s`" %
                    (package.__name__, os.path.dirname(package.__file__)))
        self.app_packages.add(package)

    def get_app_paths(self):
        return [os.path.dirname(app.__file__) for app in self.app_packages]
