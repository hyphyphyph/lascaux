# -*- coding: utf-8 -*-

from lascaux import Controller 


class Index(Controller):
    
    def get(self, p, place=None):
        # self.render('index', message=u"Hello World")
        # self.final('index', app_package=True)
        self.save("""
            <form method="post" enctype="multipart/form-data">
                <input type="text" />
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        """)
