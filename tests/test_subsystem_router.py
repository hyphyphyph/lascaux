if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
import os.path
try:
    import json
except:
    import simplejson as json

import lascaux
from instlatte import Manager


class TestSubsystemRouter(unittest.TestCase):

    def setUp(self):
        self.m = Manager()
        self.m.add_subsystem(os.path.join(lascaux.__lib_path__,
                                          'subsystems', 'router'))
        self.m.init()

    def runTest(self):
        self.m.execute("__load_enabled_plugins__")


if __name__ == "__main__":
    unittest.main()
