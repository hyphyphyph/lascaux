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
        request.static_path = self._get_static_path(request.uri)
        if request.static_path:
            return self.handle_static_serve(request)
        elif self.find_route(request):
            if request.flag_redirect:
                return self.handle_redirect_serve(request)
            self.exec_route(request)
            if request.flag_redirect:
                return self.handle_redirect_serve(request)
            return request
        elif request.flag_redirect:
            return self.handle_redirect_serve(request)
        else:
            return self.handle_error_serve("404", request)

    def find_route(self, request):
        return self.app.manager.execute('find_route', dict(app=self.app,
                                                           request=request),
                                        subsystems=['router'])

    def exec_route(self, request):
        return self.app.manager.execute('exec_route', dict(app=self.app,
                                                           request=request),
                                        subsystems=['router'])
        
    def handle_static_serve(self, request):
        request.simple_content = True
        if not request.static_path:
            path = self._get_static_path(request.uri)
        else:
            path = request.static_path
        if not path:
            self.handle_serve_error("404", request)
        request.headers.set("Content-type", mimetypes.guess_type(path)[0])
        file_ = open(path, "r")
        content = file_.read()
        file_.close()
        request.save(content, plain=True)
        logger.info("serving static file %s -> %s" % (path, request.uri))
        return request

    def _get_static_path(self, uri):
        dirs = list()
        for dir_ in (["", "public"], 
                    ["styles", "styles"], 
                    ["scripts", "scripts"]):
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
                if os.path.isfile(path):
                    return path
        return False

    def handle_redirect_serve(self, request):
        return request

    def handle_error_serve(self, Code, request):
        if Code == "404":
            request.set_http_code("404 NOT FOUND")
            request.save("Error 404, not found.")
        return request
