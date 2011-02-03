if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from instlatte.manager import Manager


class TestManager(unittest.TestCase):

    def test_manager_init(self):
        manager = Manager()
        manager.setup()
    

if __name__ == "__main__":
    unittest.main()
