# -*- coding: utf-8 -*-

from lascaux import Controller
from lascaux import config


class Index(Controller):
    
    def get(self, p, place=None):
        print config
        self.render('index', message=u"Hello World")
        self.final('index', app_package=True)
