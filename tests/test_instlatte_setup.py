if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from lascaux.lib.instlatte_setup import *


class TestInstlatteSetup(unittest.TestCase):

    def test_new_manager(self):
        print new_manager()


if __name__ == "__main__":
    unittest.main()
