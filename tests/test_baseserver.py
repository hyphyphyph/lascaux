if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from lascaux.sys import App
from lascaux.request import Request
from lascaux.baseserver import BaseServer


class TestBaseServer(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_get_static_path(self):
        server = BaseServer(self.app)
        print server._get_static_path('/README')
        print server._get_static_path('/plugins/lascaux/README')


if __name__ == "__main__":
    unittest.main()
