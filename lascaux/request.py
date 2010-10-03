import weakref

from libel import sl

from lascaux import SObject
from lascaux.httpheader import HTTPHeader
from lascaux.httpcookie import HTTPCookie
from lascaux.session import Session


class Request(SObject):

    app = None
    URI = None
    headers = None
    cookies = None
    session = None
    content = None
    flag_redirect = None
    http_status_code = "202 SUCCESS"
    http_extra = None
    exec_plugin = None
    exec_route = None
    exec_args = None
    POST = None
    config = None

    def __init__(self, App, URI):
        self.app = weakref.proxy(App)
        self.URI = URI
        self.headers = HTTPHeader(self)
        self.cookies = HTTPCookie(self)
        self.session = Session(self)
        self.content = u""
        self.exec_args = {}
        self.http_extra = {}
        self.POST = {}
        self.config = {
            "cookie": {
                "output_domain": True,
                "output_path": True,
                "http_only": True
            }
        }

    def close(self):
        self.session.save()
        self.cookies.save()

    def get_content(self):
        return self.content

    def save(self, Content):
        self.content += Content

    def redirect(self, Where, Code="302"):
        pass

    def set_http_code(self, Code):
        self.http_status_code = Code

    def get_http_code(self):
        return self.http_status_code

    def get_http_headers(self):
        headers = []
        for header in self.headers:
            headers.append((header, self.headers[header]))
        return headers

    def set_domain(self, Domain):
        self.http_extra["domain"] = Domain

    def get_domain(self):
        return self.http_extra.get("domain")

    def get_route(self, Controller, Action, Args={}):
        args = Args or {}
        m = self.app.manager
        routes = m.execute(m.select("subsystem", sl.EQUALS("lascaux_router")), 
                           "get_route", {"request": self, 
                                         "controller": Controller, 
                                         "action": Action, "args": args})
        return routes.values()[0]
