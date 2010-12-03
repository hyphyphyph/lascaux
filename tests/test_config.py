if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
from pprint import pprint

from lascaux.config import Config


class TestManagerInit(unittest.TestCase):

    def runTest(self):
        pprint(Config())


if __name__ == "__main__":
    unittest.main()
