if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
import os.path

from lascaux.subsystems.plugin.lib import *


class TestSubsystemPluginLib(unittest.TestCase):

    def test_get_plugin_dirs(self):
        print get_plugin_dirs()

    def test_is_plugin_enabled(self):
        print map(is_plugin_enabled, [os.path.basename(p)
                                      for p in get_plugin_dirs()])


if __name__ == "__main__":
    unittest.main()
