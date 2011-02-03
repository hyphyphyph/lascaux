if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
from pprint import pprint


class TestConfig(unittest.TestCase):

    def runTest(self):
        from lascaux.config import Config
        pprint(Config())
        from lascaux import config
        pprint(config)


if __name__ == "__main__":
    unittest.main()
