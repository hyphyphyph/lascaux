# -*- coding: utf-8 -*-

import weakref


class Plugin(object):
    
    app = None
    name = None
    app_package = None
    config = dict()
    controllers = dict()

    def __init__(self, app=None, app_package=None, name=None, config=dict()):
        self.app = app and weakref.proxy(app) or None
        self.app_package = app_package
        self.name = name
        self.config = config or dict()
        self.controllers = dict()
