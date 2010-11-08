import os.path

import libel
from crepehat import Kitchen
from mako.template import Template

# from lascaux.sys import SObject


class Hook(object):

    path = None
    controller = None
    db = None
    request = None

    def __init__(self, request=None, controller=None):
        self.request = request or None
        self.controller = controller or None
        if self.controller:
            self.db = controller.db

    def get_template(self, name, dirs=None, extensions=None):
        dirs = dirs or [os.path.join(self.get_exec_path(), "templates"),
                        os.path.join(self.path, "templates")]
        extensions = extensions or [".mako"]
        k = Kitchen(dirs, extensions)
        return k.get(name)

    def render(self, file, data=None):
        if self.request:
            data = data or {}
            data["request"] = self.request
            if self.controller:
                data["controller"] = self.controller
            libel.merge_dict(data, self.request.get_content())
            if not os.path.isfile(file):
                file = self.get_template(file)
            t = Template(filename=file, module_directory=os.path.join(
                config.get_tmp(), "tmpl_cache"))
            return t.render(**data)
