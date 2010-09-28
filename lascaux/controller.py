import os.path
import weakref

from lascaux import SObject
from lascaux.util import parse_route_to_regex


class Controller(SObject):

    request = None
    content = None
    name = None
    path = None
    config = {}
    routes = []
    POST = None
    cookies = None
    session = None

    def __init__(self, Request=None):
        self.content = ""
        self.POST = {}
        if not self.__class__.routes:
            self.__class__.routes = self.config["routes"]
        if Request:
            self.request = Request
            self.POST = self.request.POST
            self.cookies = self.request.cookies
            self.session = self.request.session

    def __get_static_dirs__(self):
        dirs = []
        for dir in (["", "public"],
                    ["styles", "styles"],
                    ["scripts", "scripts"]):
            dirs.append([os.path.join("plugins", self.name, dir[0]),
                         os.path.join(self.path, dir[1])])
        return dirs

    def save(self, Content):
        if self.request:
            if self.content:
                self.request.save(self.content)
                self.content = ""
            self.request.save(Content)
        else:
            self.content += Content
