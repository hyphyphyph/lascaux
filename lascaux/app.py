import os.path

import instlatte
from libel import sl

from lascaux import SObject, config


class App(SObject):

    manager = None

    def __init__(self):
        self.manager = instlatte.Manager(self.get_exec_path(),
            config["subsystems"], False)
        self.manager.add_subsystem_source(os.path.join("lascaux",
                                                       "subsystems"))
        self.manager.init()

        print self.manager.select("subsystem", sl.EQUALS("server"))

    def __call__(self):
        self.dispatch()


app = App()
