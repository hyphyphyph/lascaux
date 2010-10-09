import os.path
import weakref

from crepehat import Kitchen
from mako.template import Template

import libel

from lascaux import SObject, Redirect
from lascaux.config import config
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


    def save(self, Content, Name="content"):
        if self.request:
            if self.content:
                for key in self.content:
                    self.request.save(self.content[key], key)
                self.content = {}
            self.request.save(Content, Name)
        else:
            if Name not in self.content:
                self.content[Name] = []
            self.content[Name].append(Content)

    def get_template(self, Name, Dirs=None, Extensions=None):
        Dirs = Dirs or [os.path.join(self.get_exec_path(), "templates"),
                        os.path.join(self.path, "templates")]
        Extensions = Extensions or [".mako"]
        k = Kitchen(Dirs, Extensions)
        return k.get(Name)

    def get_js(self, Name):
        return self.get_template(Name, [self.get_exec_path(), "scripts",
                                        self.path, "script"], [".js"])

    def get_css(self, Name):
        return self.get_template(Name, [self.get_exec_path(), "styles",
                                        self.path, "styles"], [".css"])

    def render(self, File, Data=None):
        Data = Data or {}
        Data["controller"] = self
        libel.merge_dict(Data, self.request.get_content())
        if not os.path.isfile(File):
            File = self.get_template(File)
        t = Template(filename=File, module_directory=os.path.join(
            config.get_tmp(), "tmpl_cache"))
        return t.render(**Data)

    def route(self, Controller, Action=None, Args={}):
        if type(Action) is dict or Action is None:
            Args = Action
            Action = Controller
            Controller = self
        if Controller is self:
            Controller = self.name
        return self.request.get_route(Controller, Action, Args)

    def redirect(self, Controller, Action=None, Args={}):
        return Redirect(self.route(Controller, Action, Args))

    def hook(self, hook, data={}):
        return self.request.hook(hook, data, self)
