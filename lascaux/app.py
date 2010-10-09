import os.path

import instlatte
from libel import sl

from lascaux.sobject import SObject
from lascaux.config import config


def get_manager(config_=None, init=False):
    config_ = config_ or config["subsystems"]
    manager = instlatte.Manager(SObject().get_exec_path(), config_, False)
    manager.add_subsystem_source(os.path.join("lascaux", "subsystems"))
    if init:
        manager.init()
    return manager


class App(SObject):

    manager = None
    _app = None

    def __init__(self):
        self.app = self
        self.manager = get_manager(init=True)
        self.manager.execute(self.manager.select("subsystem",
                                                 sl.EQUALS("lascaux_hook")),
                             "_discover_plugins", {"app": self})
        self.hook("app_init", {"app": self})

    def hook(self, hook, data={}, controller=None, request=None):
        data = data or {}
        data["controller_"] = controller
        data["request_"] = request
        self.manager.execute(self.manager.select("subsystem",
                                                 sl.EQUALS("lascaux_hook")),
                             "exec_hook", {"hook": hook, "data": data})

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
