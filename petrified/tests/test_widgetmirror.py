if __name__ == "__main__": import sys; sys.path.append("..")
import unittest


from petrified import 


class TestWidgetMirror(unittest.TestCase):

    def setUp(self):
        self.mirror = WidgetMirror()

    def test_get_static_path(self):
        server = BaseServer(self.app)
        print server._get_static_path('/README')
        print server._get_static_path('/plugins/lascaux/README')


if __name__ == "__main__":
    unittest.main()

