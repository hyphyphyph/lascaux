import os.path

from lascaux import SObject, logger


logger = logger(__name__)


class Environment(SObject):

    apps = set()


    def __init__(self):
        self.apps = set()

    def add_app_package(self, package):
        logger.info(u"added app '%s' from path `%s`" %
                    (package.__name__, os.path.dirname(package.__file__)))
        self.apps.add(package)

    def get_app_paths(self):
        return [os.path.dirname(app.__file__) for app in self.apps]
