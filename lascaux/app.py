import os.path

import instlatte

from lascaux.sobject import SObject


class App(SObject):

    env = None
    self = None # weakref proxy resolution

    def __init__(self, env):
        self.env = env
        self.self = self
