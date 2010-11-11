import cgi
import binascii
import uuid
import os.path

import wsgiref.simple_server
from wsgiref.simple_server import make_server

import libel

from lascaux.baseserver import BaseServer
from lascaux.sys import logger

from lascaux.request import Request
from lascaux.sys import config


logger = logger(__name__)


class SimpleWSGIServer(BaseServer):
    def start(self, app):
        BaseServer.start(self, app)
        # Silences standard output from simple_server
        class quiet_handler(wsgiref.simple_server.WSGIRequestHandler):
            def log_message(self, format, *args):
                pass
        server = make_server(config["server"]["host"],
                             int(config["server"]["port"]),
                             self, handler_class=quiet_handler)
        server.serve_forever()

    def __call__(self, environ, start_response):
        return self.handle_request(environ=environ,
                                   start_response=start_response)

    def handle_request(self, environ, start_response):
        uri = environ.get("PATH_INFO")
        request = Request(self.app.get_root(), uri)
        request.cookies.load(environ.get("HTTP_COOKIE"))
        # request.session.load()
        # request.set_domain(environ.get("HTTP_HOST"))
        # if environ["REQUEST_METHOD"] == "POST":
        #     form_data = cgi.FieldStorage(fp=environ["wsgi.input"],
        #                                  environ=environ)
        #     form_values = {}
        #     for name in form_data:
        #         # type=file
        #         if form_data[name].filename:
        #             dir_ = os.path.join(config["paths"]["tmp"],
        #                                 str(uuid.uuid1()))
        #             filename = form_data[name].filename
        #             libel.mkdir(dir_)
        #             file = open(os.path.join(dir_, filename), "wb")
        #             file.write(form_data[name].file.read())
        #             file.close()
        #             form_values[name] = os.path.join(dir_, filename)
        #         # anything "normal"
        #         else:
        #             form_values[name] = form_data[name].value
        #     request.POST = form_values
        # else:
        #     request.POST = False
        # request = BaseServer.handle_request(self, request)
        request.close()
        start_response(request.get_http_code(), request.get_http_headers())
        # if request.flag_redirect:
        #     return [""]
        # content = request.render_final()
        content = u"!3"
        return [content.encode('utf-8')]
