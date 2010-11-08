if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from lascaux.config import Config


class TestManagerInit(unittest.TestCase):

    def runTest(self):
        Config()


if __name__ == "__main__":
    unittest.main()
