# -*- coding: utf-8 -*-

from lascaux import Controller, model


class Index(Controller):
    
    def get(self, p, place=None):
        m = model.HelloWorldMessage()
        self.store.add(m)
        self.store.commit()
        self.render('index', message=u"Hello World")
        self.final('index', app_package=True)
