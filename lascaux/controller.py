import os.path
import weakref

from crepehat import Kitchen
import libel
from mako.template import Template

import lascaux
from lascaux.sys import SObject, config
from lascaux.locals import Redirect
# from lascaux.util import parse_route_to_regex
# from lascaux.helpers import get_resource


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

    def __init__(self, request=None):
        self.content = ""
        self.POST = {}
        if not self.__class__.routes:
            self.__class__.routes = self.config["routes"]
        if request:
            self.request = request
            self.POST = self.request.POST
            self.cookies = self.request.cookies
            self.session = self.request.session
            self.path = self.request.exec_plugin.package_dir
            self.save = self.request.save

    @classmethod
    def get_static_dirs(cls, meta):
        dirs = []
        for dir_ in (["", "public"],
                    ["styles", "styles"],
                    ["scripts", "scripts"]):
            dirs.append([os.path.join("plugins", meta.name, dir_[0]),
                         os.path.join(meta.package_dir, dir_[1])])
        return dirs


    def get_template(self, name, dirs=None, extensions=None):
        dirs = dirs or [os.path.join(os.path.dirname(a.__file__), 'templates')
                        for a in lascaux.app_packages]
        dirs.append(os.path.join(self.path, 'templates'))
        extensions = extensions or ['.mako']
        k = Kitchen(dirs, extensions)
        return k.get(name)

    def get_js(self, Name):
        return self.get_template(Name, [os.path.join(self.get_exec_path(),
                                                     "scripts"),
                                        os.path.join(self.path, "scripts")],
                                 [".js"])

    def get_css(self, name):
        return self.get_template(name, [os.path.join(self.get_exec_path(),
                                                     "styles"),
                                        os.path.join(self.path, "styles")],
                                 [".css"])

    def render(self, file, data=None):
        data = data or {}
        data["controller"] = self
        if not os.path.isfile(file):
            file = self.get_template(file)
        if file:
            t = Template(filename=file, module_directory=os.path.join(
                config.get_tmp(), "tmpl_cache"))
            return t.render(**data).decode("utf-8")
        return u""

    def route(self, controller, action=None, args={}):
        if type(action) is dict or action is None:
            args = action
            action = controller
            controller = self
        if controller is self:
            controller = self.name
        return self.request.get_route(controller, action, args)

    def redirect(self, controller, action=None, args={}):
        return Redirect(self.route(controller, action, args))

    def hook(self, hook, data={}):
        return self.request.hook(hook, data, self)

    def add_css(self, name):
        resource = get_resource("%s.css" % name, self.name)
        self.save(resource, "head_style")

    def add_js(self, name):
        resource = get_resource("%s.js" % name, self.name)
        self.save(resource, "head_script")
