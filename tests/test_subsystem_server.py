# -*- coding: utf-8 -*-

if __name__ == "__main__": import sys; sys.path.append(".")
import unittest
import os.path
try:
    import json
except:
    import simplejson as json

import lascaux
from instlatte import Manager


class TestSubsystemServer(unittest.TestCase):

    def setUp(self):
        self.manager = Manager({
            'sources': [os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'subsystems'))],
            'subsystems': {
                'server': {
                    'enabled': True,
                    'sources': [],
                    'servers': {
                        'simplewsgi': {
                            'enabled': True
                        }
                    }
                }
            }
        })
        self.manager.setup()

    def runTest(self):
        self.manager.execute('load_servers')
        self.manager.execute('start_servers')


if __name__ == "__main__":
    unittest.main()
