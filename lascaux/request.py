import os.path
import weakref

from libel import sl

from lascaux import SObject, config
from lascaux.httpheader import HTTPHeader
from lascaux.httpcookie import HTTPCookie
from lascaux.session import Session

from crepehat import Kitchen
from mako.template import Template


class Request(SObject):

    app = None
    URI = None
    headers = None
    cookies = None
    session = None
    content = None
    plain_content = None
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
        self.content = {"content": []}
        self.plain_content = ""
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
        if self.plain_content:
            return self.plain_content
        content = {}
        for key in self.content:
            content[key] = u"\n".join(self.content[key])
        return content

    def render_final(self):
        if self.plain_content:
            return self.plain_content
        dirs = [os.path.join(self.get_exec_path(), "templates")]
        k = Kitchen(dirs, [".mako"])
        file = k.get("index")

        t = Template(filename=file, module_directory=os.path.join(
            config.get_tmp(), "tmpl_cache"))
        return t.render(**self.get_content())

    def save(self, Content, Name="content", plain=False):
        if plain:
            if self.plain_content:
                self.plain_content += Content
            else:
                self.plain_content = Content
            return
        if Name not in self.content:
            self.content[Name] = []
        self.content[Name].append(Content)

    def set_content(self, content, plain=False):
        """
        Pretty low-level...  Gotta say, dude.
        """
        if plain:
            self.plain_content = content
        else:
            self.content = content

    def redirect(self, Where, Code="302"):
        pass

    def set_http_code(self, Code):
        self.http_status_code = Code

    def get_http_code(self):
        return str(self.http_status_code)

    def get_http_headers(self):
        headers = []
        for header in self.headers:
            headers.append((header, str(self.headers[header])))
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
        return routes.values()[0] or u"/"

    def route(self, controller, action, args={}):
        return self.get_route(controller, action, args)

    def hook(self, hook, data={}, controller=None):
        return self.app.hook(hook, data, controller=controller, request=self)
