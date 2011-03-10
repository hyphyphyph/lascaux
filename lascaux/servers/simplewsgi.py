import os.path
import cgi
import uuid

import wsgiref.simple_server
from wsgiref.simple_server import make_server

import libel

from lascaux import config
from lascaux.server import Server
from lascaux.sys.logger import logger
from lascaux.reqres import Reqres


logger = logger(__name__)


class SimpleWSGIServer(Server):

    def start(self):
        Server.start(self)

        # Silences standard output from simple_server
        class quiet_handler(wsgiref.simple_server.WSGIRequestHandler):
            def log_message(self, format, *args):
                pass

        server = make_server(self.config["host"],
                             int(self.config["port"]),
                             self, handler_class=quiet_handler)
        server.serve_forever()

    def __call__(self, environ, start_response):
        return self.serve(environ=environ,
                          start_response=start_response)

    def serve(self, environ, start_response):
        uri = environ.get("PATH_INFO")
        reqres = Reqres(self.app.get_root(), uri)
        reqres.cookies.eat(environ.get("HTTP_COOKIE"))
        reqres.session.load()
        reqres.set_domain(environ.get("HTTP_HOST"))
        reqres.request_method = environ['REQUEST_METHOD'].lower()
        if environ["REQUEST_METHOD"].upper() == "POST":
            reqres.post = self._extract_post(environ)
        reqres = Server.serve(self, reqres)
        reqres.close()
        start_response(reqres.get_http_code(), reqres.get_http_headers())
        if reqres.flag_redirect:
            return ['']
        return [reqres.render().encode('utf-8')]
        
    def _extract_post(self, environ):
        form_data = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        form_values = {}
        for name in form_data:
            # type==file
            if form_data[name].filename:
                dir_ = os.path.join(config["paths"]["tmp"],
                                    str(uuid.uuid1()))
                filename = form_data[name].filename
                libel.mkdir(dir_)
                file = open(os.path.join(dir_, filename), "wb")
                file.write(form_data[name].file.read())
                file.close()
                form_values[name] = os.path.join(dir_, filename)
            # anything "normal"
            else:
                # TODO: should the encoding be hard-coded ?
                form_values[name] = form_data[name].value.decode('utf-8')
        return form_values
