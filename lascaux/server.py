import weakref
import mimetypes
import os.path

import lascaux
from lascaux import config
from lascaux.sys.logger import logger


logger = logger(__name__)


class Server(object):

    app = None
    config = dict()

    def __init__(self, app=None, config=dict()):
        self.app = app and weakref.proxy(app) or None
        self.config = config or dict()

    def start(self):
        logger.info("started %s server on %s:%s  servering forever..." %
                    (self.__class__, self.config["host"], self.config["port"]))

    def serve(self, reqres):
        reqres.static_path = self.get_static_path(reqres.uri)
        if reqres.static_path:
            self.serve_static(reqres)
            return reqres
        else:
            reqres.find_execpaths()
        if reqres.flag_redirect:
            self.serve_redirect(reqres)
        if reqres.execpaths:
            reqres.execute()
        else:
            reqres.error = '404'
        if reqres.flag_redirect:
           self.serve_redirect(reqres)
        if reqres.error:
            self.serve_error(reqres)
        return reqres

    def serve_static(self, reqres):
        reqres.force_plain_content = True
        reqres.erase_content()
        if not reqres.static_path:
            reqres.static_path = self.get_static_path(reqres.uri)
        if not reqres.static_path:
            reqres.error = '404'
            self.serve_error(reqres)
        reqres.headers['Content-type'] = mimetypes.guess_type(reqres.static_path)[0]
        file_ = open(reqres.static_path, 'r')
        content = file_.read()
        file_.close()
        reqres.save(content)
        logger.info('serving static file %s -> %s' % (reqres.uri, reqres.static_path))
        return reqres

    def serve_redirect(self, reqres):
        return reqres

    def serve_error(self, reqres):
        if reqres.error == "404":
            reqres.set_http_code("404 NOT FOUND")
            reqres.save('Error 404, not found.')
        return reqres

    def get_static_path(self, uri):
        mappings = list()
        static_dir_mappings = self.app.manager.get_subsystem('server').config['static_dir_mappings']
        for local in static_dir_mappings:
            for app_package in config['app_packages']:
                mappings.append([local, 
                                 os.path.join(config[app_package]['package_dir'], 
                                              static_dir_mappings[local])])
        self.app.manager.execute("get_static_dir_mappings", mappings=mappings)
        # Oh yeah.  That's right.  List comprehension, baby.
        mappings = [[m[0].startswith('/') and m[0] or os.path.join('/', m[0]), m[1]] for m in mappings]
        for mapping in mappings:
            if uri.startswith(mapping[0]):
                uri_ = uri[len(mapping[0]):]
                path = os.path.join(mapping[1], *filter(lambda s: s,
                                                        uri_.split("/")))
                if os.path.isfile(path):
                    return path
        return False
