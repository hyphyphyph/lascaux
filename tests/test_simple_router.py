if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from lascaux.sys import App
from lascaux.request import Request
from lascaux.routers.simple_router import SimpleRouter


class TestSimpleRouter(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_find_simple_route(self):
        request = Request(self.app, u'lascaux/index')
        router = SimpleRouter()
        self.assertTrue(router.find_route(self.app, request))
        print request.exec_plugin
        print request.exec_route
        print request.exec_args

    def test_find_arg_route(self):
        request = Request(self.app, u'lascaux/view/123')
        router = SimpleRouter()
        self.assertTrue(router.find_route(self.app, request))
        print request.exec_plugin
        print request.exec_route
        print request.exec_args


if __name__ == "__main__":
    unittest.main()
