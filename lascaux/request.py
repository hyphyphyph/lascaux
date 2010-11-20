import os.path
import weakref
import time

from libel import sl

import lascaux
from lascaux.sys import SObject, logger, config
from lascaux.httpheader import HTTPHeader
from lascaux.httpcookie import HTTPCookie
from lascaux.session import Session

from crepehat import Kitchen
from mako.template import Template


logger = logger(__name__)


class Request(SObject):

    _init_time = None
    _close_time = None

    app = None
    uri = None
    headers = None
    cookies = None
    session = None
    content = None
    plain_content = None
    render_template = 'index'
    flag_redirect = None
    http_status_code = "202 SUCCESS"
    http_extra = None
    exec_plugin = None
    exec_route = None
    exec_args = None
    post = None
    config = None

    def __init__(self, app, uri):
        self._init_time = time.time()
        self.app = weakref.proxy(app)
        self.uri = uri.startswith('/') and uri or u'/%s' % uri
        self.headers = HTTPHeader(self)
        self.cookies = HTTPCookie(self)
        self.session = Session(self)
        self.content = dict(content=list(),
                            head_style=list(),
                            head_script=list())
        self.plain_content = ""
        self.exec_args = dict()
        self.http_extra = dict()
        self.post = dict()
        self.config = config

    def close(self):
        self._close_time = time.time()
        logger.info(u'%s milliseconds' % ((self._close_time -
                                           self._init_time) * 1000))
        self.session.save()
        self.cookies.save()
        self.hook('request_close')

    def dump_content(self):
        content = dict()
        # TODO: Where should this go ?
        if config['debug'] and 'debug' not in self.content:
            self.content['debug'] = u''
        for key in self.content:
            if key == 'debug' and not config['debug']:
                pass
            content[key] = u'\n'.join(self.content[key])
        return content

    def render(self):
        """
        returns a unicode of the request's content.  if not plain
        content, it renders through the active main template.
        """
        if self.plain_content:
            return self.plain_content
        dirs = [os.path.abspath(os.path.join(os.path.dirname(p.__file__),
                                'templates')) for p in lascaux.app_packages]
        k = Kitchen(dirs, ['.mako'])
        file_ = k.get(self.render_template)
        t = Template(filename=file_, module_directory=os.path.join(
            config.get_tmp(), 'tmpl_cache'))
        return t.render(**self.dump_content()).encode('utf-8')

    def save(self, content, name='content', plain=False):
        if plain:
            if self.plain_content:
                self.plain_content += content
            else:
                self.plain_content = content
            return
        if name not in self.content:
            self.content[name] = []
        self.content[name].append(content)

    def set_content(self, content, plain=False):
        """
        pretty low-level...  Gotta say, dude.
        """
        if plain:
            self.plain_content = content
        else:
            self.content = content

    def debug(self, title, content):
        self.save(u'%s: %s' % (title, content), name='debug')

    def redirect(self, where, code="302"):
        pass

    def set_http_code(self, code):
        self.http_status_code = code

    def get_http_code(self):
        return str(self.http_status_code)

    def get_http_headers(self):
        headers = []
        for header in self.headers:
            headers.append((header, str(self.headers[header])))
        return headers

    def set_domain(self, domain):
        self.http_extra["domain"] = domain

    def get_domain(self):
        return self.http_extra.get("domain")

    def get_route(self, controller, action, args=dict()):
        args = args or dict()
        m = self.app.manager
        routes = m.execute(m.select("subsystem", sl.EQUALS("lascaux_router")),
                           "get_route", {"request": self,
                                         "controller": Controller,
                                         "action": Action, "args": args})
        return routes.values()[0] or u"/"

    def route(self, controller, action, args={}):
        return self.get_route(controller, action, args)

    def hook(self, hook, *argc, **argv):
        if 'request' not in argv:
            argv['request'] = self
        return self.app.hook(hook, *argc, **argv)
