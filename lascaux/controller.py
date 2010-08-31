import os.path

from lascaux import SObject
from lascaux.util import parse_route_to_regex


class Controller(SObject):

    name = None
    path = None
    config = {}
    routes = []

    def __init__(self):
        for route in self.config["routes"]:
            pass

    def __get_static_dirs__(self):
        dirs = []
        for dir in (["", "public"],
                    ["styles", "styles"],
                    ["scripts", "scripts"]):
            dirs.append([os.path.join("plugins", self.name, dir[0]),
                         os.path.join(self.path, dir[1])])
        return dirs
