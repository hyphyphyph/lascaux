import wsgiref.simple_server
from wsgiref.simple_server import make_server

from lascaux.baseserver import BaseServer
from lascaux import config, logger
logger = logger(__name__)
from lascaux.request import Request


class SimpleWSGIServer(BaseServer):
    def init_server(self, App):
        BaseServer.init_server(self, App)
        # Silences standard output from simple_server
        class quiet_handler(wsgiref.simple_server.WSGIRequestHandler):
            def log_message(self, format, *args):
                pass
        server = make_server(config["server"]["host"],
                             int(config["server"]["port"]),
                             self,
                             handler_class = quiet_handler)
        logger.info("Started SimpleWSGI server on %s:%s. \
                     Servering forever... (and ever and ever and ever)" % (
            config["server"]["host"], config["server"]["port"]))
        server.serve_forever()

    def __call__(self, environ, start_response):
        return self.handle_request(environ=environ,
                            start_response=start_response)

    def handle_request(self, environ, start_response):
        uri = environ.get("PATH_INFO")
        request = Request(uri)
        request = self.handle_static_serve(request)
        headers = []
        for header in request.headers:
            headers.append((header, request.headers[header]))
        start_response(request.get_http_code(), headers)
        return [str(request.content)]
