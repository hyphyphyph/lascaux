# -*- coding: utf-8 -*-

import weakref
import os.path

from mako.template import Template
from crepehat import Kitchen

from lascaux import config


class Controller(object):

    plugin = None
    reqres = None
    execpath = None

    def __init__(self, reqres, execpath):
        self.reqres = weakref.proxy(reqres)
        self.execpath = execpath
        # reqres aliases
        self.save = reqres.save
        self.cookies = reqres.cookies
        self.session = reqres.session

    def get(self, *args, **kwargs): pass 
    def post(self, *args, **kwargs): pass

    def render(self, name, *args, **kwargs):
        self.save(self.template(name, *args, **kwargs))

    def template(self, name, *args, **kwargs):
        kitchen = Kitchen(os.path.join(self.plugin.config['package_dir'], 'templates'),
                          ['.mako'])
        template = kitchen.get(name)
        t = Template(filename=template)
        return t.render(**kwargs)

    def final(self, name, app_package=True):
        search_dir = app_package and os.path.join(config[self.plugin.app_package]['package_dir']) \
                     or os.path.join(self.plugin.config['package_dir'])
        kitchen = Kitchen(os.path.join(search_dir, 'templates'),
                          ['.mako'])
        template = kitchen.get(name)
        if not template:
            return False
        content = dict()
        for location in self.reqres.content:
            content.setdefault(location, list())
            content[location] = u'\n'.join(self.reqres.content[location])
        t = Template(filename=template)
        final = t.render(**content)
        saved = self.reqres.erase_content()
        self.save(final)
        return saved
