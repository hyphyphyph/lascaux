# -*- coding: utf-8 -*-

from lascaux import Controller


class Index(Controller):
    
    def get(self, p, place=None):
        self.render('index', message=u"Hello World")
        self.final('index', app_package=True)
