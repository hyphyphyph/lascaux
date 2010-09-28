import os.path

import instlatte
from libel import sl

from lascaux.sobject import SObject
from lascaux.config import config


class App(SObject):

    manager = None
    _app = None

    def __init__(self):
        self.app = self
        self.manager = instlatte.Manager(self.get_exec_path(),
            config["subsystems"], False)
        self.manager.add_subsystem_source(os.path.join("lascaux",
                                                       "subsystems"))
        self.manager.init()

    def init_server(self):
        self.manager.execute(self.manager.select("subsystem",
                                                 sl.EQUALS("lascaux_server")),
                             "init_server", {"app": self})

    def __call__(self):
        self.dispatch()

    def find_exec(self, Request):
        self.manager.execute(self.manager.select("subsystem",
                                                 sl.EQUALS("lascaux_router")),
                             "find_exec", {"app": "self", "request": Request})

    def find_route(self, Request):
        results = self.manager.execute(self.manager.select(
            "subsystem", sl.EQUALS("lascaux_router")), "find_route",
            {"App": self, "Request": Request})
        return True in results.values()

    def exec_route(self, Request):
        results = self.manager.execute(self.manager.select(
            "subsystem", sl.EQUALS("lascaux_router")), "exec_route",
            {"App": self, "Request": Request})

    def get_root(self):
        app = self
        while app.app != app:
            app = app.app
        return app
