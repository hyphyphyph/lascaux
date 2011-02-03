if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from lascaux.app import App
from lascaux.reqres import Reqres
from lascaux.routers.regex import RegexRouter


class TestRegexRouter(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def runTest(self):
        routers = self.app.manager.get_subsystem('router').get_routers()
        for router in routers:
            print router.find_controller(Reqres(uri='/hello/world'))
        # for plugin in plugins:
        #     for route in plugin.config['routes']:
        #         print plugin.controllers[plugin.config['routes'][route]['controller']]

if __name__ == "__main__":
    unittest.main()
