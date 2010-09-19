import weakref
import mimetypes
import os.path

from libel import sl

from lascaux import SObject
from lascaux import logger
logger = logger(__name__)


class BaseServer(SObject):

    app = None

    def init_server(self, App):
        self.app = weakref.proxy(App)

    def handle_request(self, Request):
        if self._get_static_path(Request.URI):
            return self.handle_static_serve(Request)
        # elif self.app.router.find_route(Request):
        #     return self.handle_request(Request)
        # elif Request.redirect:
        #     return self.handle_redirect_serve(Request)
        else:
            return self.handle_error_serve("404", Request)

    def handle_static_serve(self, Request):
        path = self._get_static_path(Request.URI)
        if not path:
            self.handle_serve_error("404", Request)
        Request.headers.set("Content-type", mimetypes.guess_type(path)[0])
        file = open(path, "r")
        content = file.read()
        file.close()
        Request.content = content
        logger.info("Serving static file %s via %s" % (path, Request.URI))
        return Request

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
                path = os.path.join(dir[1], *filter(lambda s: s,
                                                    URI.split("/")))
                if os.path.isfile(path):
                    return path
        return False

    def handle_redirect_serve(self, Request):
        pass

    def handle_error_serve(self, Code, Request):
        if Code == "404":
            Request.set_http_code("404 NOT FOUND")
            Request.save("Error 404, not found.")
        return Request
