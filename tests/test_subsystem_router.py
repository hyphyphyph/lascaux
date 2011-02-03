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


class TestSubsystemRouter(unittest.TestCase):

    def setUp(self):
        self.manager = Manager({
            'sources': [os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'subsystems'))],
            'subsystems': {
                'router': { 
                    'enabled': True,
                    'routers': {
                        'regex': {
                            'enabled': True
                        }
                    }
                }
            }
        })
        self.manager.setup()

    def runTest(self):
        self.manager.execute('load_routers')


if __name__ == "__main__":
    unittest.main()
