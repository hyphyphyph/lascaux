# -*- coding: utf-8 -*-

if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
import os.path
try:
    import json
except:
    import simplejson as json

from instlatte import Manager

import lascaux


class TestSubsystemPlugin(unittest.TestCase):

    def setUp(self):
        self.manager = Manager({
            'sources': [os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'subsystems'))],
            'subsystems': {
                'plugin': {
                    'enabled': True
                }
            }
        })
        self.manager.setup()

    def test_find_plugins(self):
        self.manager.execute('load_plugins')


if __name__ == "__main__":
    unittest.main()
