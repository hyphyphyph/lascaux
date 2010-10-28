import os.path

from petrified import SObject


class Environment(SObject):

    sources = None
    extensions = None
    tmpl_tmp = None

    def __init__(self, sources=None, extensions=None, tmpl_tmp=None):
        if sources:
            self.sources = sources
        else:
            self.sources = [os.path.join(self.get_lib_path(), "templates"),
                            os.path.join(self.get_lib_path(),
                                         "widgets", "templates")]
        if extensions:
            self.extensions = extensions
        else:
            self.extensions = [".mako"]
        self.tmpl_tmp = tmpl_tmp and os.path.abspath(tmpl_tmp) or \
                        os.path.join(self.get_exec_path(), "tmp")

    def get_sources(self):
        return self.sources

    def get_extensions(self):
        return self.extensions

    def get_tmpl_tmp(self):
        return self.tmpl_tmp
