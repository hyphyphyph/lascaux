import weakref
import mimetypes
import os.path

import lascaux
from lascaux.sys import SObject, logger, config


logger = logger(__name__)


class BaseServer(SObject):

    app = None

    def __init__(self, app=None):
        self.app = app and weakref.proxy(app) or None

    def start(self, app):
        self.app = weakref.proxy(app)
        logger.info("started %s server on %s:%s  servering forever..." %
                    (self.__class__,
                     config["server"]["host"], config["server"]["port"]))

    def handle_request(self, request):
        request.static_path = self.get_static_path(request.uri)
        if request.static_path:
            return self.serve_static(request)
        elif self.find_route(request):
            if request.flag_redirect:
                return self.serve_redirect(request)
            logger.info(u"serving executable request %s -> %s.%s()" %
                        (request.uri, request.exec_plugin.class_,
                         request.exec_route['action']))
            self.exec_route(request)
            if request.flag_redirect:
                return self.serve_redirect(request)
            return request
        elif request.flag_redirect:
            return self.serve_redirect(request)
        else:
            # TODO: why is request.uri for favicon
            #       /lascaux/favicon.ico instead of /favicon.ico ?
            logger.info(u'serving 404 -> %s' % request.uri)
            return self.serve_error("404", request)

    def find_route(self, request):
        return True in self.app.manager.execute('find_route', dict(
            app=self.app, request=request), subsystems=['router']) or False

    def exec_route(self, request):
        return self.app.manager.execute('exec_route', dict(app=self.app,
                                                           request=request),
                                        subsystems=['router'])

    def serve_static(self, request):
        request.simple_content = True
        if not request.static_path:
            path = self.get_static_path(request.uri)
        else:
            path = request.static_path
        if not path:
            self.serve_error("404", request)
        request.headers.set("Content-type", mimetypes.guess_type(path)[0])
        file_ = open(path, "r")
        content = file_.read()
        file_.close()
        request.save(content, plain=True)
        logger.info("serving static file %s -> %s" % (path, request.uri))
        return request

    def get_static_path(self, uri):
        dirs = list()
        for dir_ in config['system']['baseserver']['static_serve_directories']:
            for app in lascaux.app_packages:
                dirs.append([dir_[0], os.path.abspath(os.path.join(
                    os.path.dirname(app.__file__), dir_[1]))])
        self.app.manager.execute("get_static_dirs", dict(dirs=dirs),
                                 subsystems=['plugin'])
        for dir_ in dirs:
            if not dir_[0].startswith("/"):
                dir_[0] = os.path.join("/", dir_[0])
        for dir_ in dirs:
            if uri.startswith(dir_[0]):
                uri_ = uri[len(dir_[0]):]
                path = os.path.join(dir_[1], *filter(lambda s: s,
                                                     uri_.split("/")))
                print path
                if os.path.isfile(path):
                    return path
        return False

    def serve_redirect(self, request):
        return request

    def serve_error(self, code, request):
        if code == "404":
            request.set_http_code("404 NOT FOUND")
            request.save("Error 404, not found.")
        return request
