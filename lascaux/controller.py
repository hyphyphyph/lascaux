import weakref

from lascaux import SObject
from lascaux.util import parse_route_to_regex


class Controller(SObject):

    app = None
    request = None
    name = None
    path = None
    meta = {}
    config = {}
    routes = []

    def __init__(self, App, Request):
        self.app = weakref.proxy(App)
        self.request = weakref.proxy(Request)
        for route in self.config["routes"]:
            pass
