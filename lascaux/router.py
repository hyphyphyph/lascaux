# -*- coding: utf-8 -*-

import weakref


class Router(object):

    app = None

    def __init__(self, app=None):
        self.app = app and weakref.proxy(app) or None

    def find_execpath(self, uri):
        pass

    def find_route(self, alias=None, plugin=None, controller=None):
        pass
