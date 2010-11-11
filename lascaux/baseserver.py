import weakref
import mimetypes
import os.path

from lascaux.sys import SObject, logger, config


logger = logger(__name__)


class BaseServer(SObject):

    app = None

    def start(self, app):
        self.app = weakref.proxy(app)
        logger.info("started %s server on %s:%s  servering forever..." %
                    (self.__class__,
                     config["server"]["host"], config["server"]["port"]))

    def handle_request(self, request):
        if self._get_static_path(request.uri):
            return self.handle_static_serve(request)
        elif self.app.find_route(request):
            if request.flag_redirect:
                return self.handle_redirect_serve(request)
            self.app.exec_route(request)
            if request.flag_redirect:
                return self.handle_redirect_serve(request)
            return request
        elif request.flag_redirect:
            return self.handle_redirect_serve(request)
        else:
            return self.handle_error_serve("404", request)

    def handle_static_serve(self, request):
        request.simple_content = True
        path = self._get_static_path(request.URI)
        if not path:
            self.handle_serve_error("404", request)
        request.headers.set("Content-type", mimetypes.guess_type(path)[0])
        file = open(path, "r")
        content = file.read()
        file.close()
        request.save(content, plain=True)
        logger.info("Serving static file %s via %s" % (path, request.URI))
        return request

    def _get_static_path(self, URI):
        plugins = self.app.manager.select("subsystem",
                                          sl.EQUALS("lascaux_plugin"))
        dirs = []
        for dir in (["", "public"], 
                    ["styles", "styles"], 
                    ["scripts", "scripts"]):
            dirs.append([dir[0], os.path.join(self.get_exec_path(), dir[1])])
        self.app.manager.execute(plugins, "get_static_dirs", dirs)
        for dir in dirs:
            if not dir[0].startswith("/"):
                dir[0] = os.path.join("/", dir[0])
        for dir in dirs:
            if URI.startswith(dir[0]):
                URI_ = URI[len(dir[0]):]
                path = os.path.join(dir[1], *filter(lambda s: s,
                                                    URI_.split("/")))
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
