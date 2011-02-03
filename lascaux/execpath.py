# -*- coding: utf-8 -*-

import weakref


class Execpath(object):

    def __init__(self, reqres, plugin, alias, controller, args):
        self.reqres = weakref.proxy(reqres)
        self.plugin = weakref.proxy(plugin)
        self.alias = alias
        self.controller = controller
        self.args = args

