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
from storm.locals import create_database, Store


logger = logger(__name__)


class Request(SObject):

    _init_time = None
    _close_time = None

    app = None
    config = None
    final_template = 'index'
    
    # Request State
    headers = None
    http_status_code = "202 SUCCESS"
    http_extra = None
    cookies = None
    session = None
    content = None
    plain_content = None
    force_plain_content = False
    
    # Exec Information
    uri = None
    flag_redirect = None
    
    exec_plugin = None
    exec_route = None
    exec_args = None
    POST = False

    db = None # Maps to Storm store
    _db_store = None

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
        self.force_plain_content = None
        self.exec_args = dict()
        self.http_extra = dict()

    def save(self, content, name='content', plain=False, force_plain=True):
        if plain:
            if force_plain in (True, False) and \
               self.force_plain_content == None:
                self.force_plain_content = True
            self.force_plain_content = True
            if self.plain_content:
                self.plain_content += content
            else:
                self.plain_content = content
            return
        if name not in self.content:
            self.content[name] = []
        self.content[name].append(content)

    def route(self, controller, action, args=dict()):
        return self.get_route(controller, action, args)

    def debug(self, title, content):
        self.save(u'%s: %s' % (title, content), name='debug')

    def redirect(self, where, code="302"):
        pass

    def hook(self, hook, *argc, **argv):
        if 'request' not in argv:
            argv['request'] = self
        return self.app.hook(hook, *argc, **argv)


    def close(self):
        self._close_time = time.time()
        logger.info(u'%s milliseconds' % ((self._close_time -
                                           self._init_time) * 1000))
        self.session.save()
        self.cookies.save()
        self.hook('request_close')

    def set_content(self, content, plain=False):
        """
        pretty low-level...  Gotta say, dude.
        """
        if plain:
            self.plain_content = content
        else:
            self.content = content

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

    def _init_db_store(self):
        if not self._db_store:
            db = create_database("%s://%s:%s@%s%s/%s" %
                                 (config["database"]["interface"],
                                  config["database"]["username"],
                                  config["database"]["password"],
                                  config["database"]["host"],
                                  config["database"]["port"] and \
                                  ":%s" % c["database"]["port"] or "",
                                  config["database"]["database"]))
            self._db_store = Store(db)
        return self._db_store
    db = property(_init_db_store)
    
    
class MakoRenderer(object):

    request = None
    final_template = None

    def __init__(self, request):
        self.request = request
        self.final_template = config['system']['mako']['final_template']

    def get_content(self):
        content = dict()
        if config['debug'] and 'debug' not in self.request.content:
            self.request.content['debug'] = u''
        for key in self.request.content:
            if key == 'debug' and not config['debug']:
                pass
            content[key] = u'\n'.join(self.request.content[key])
        return content
    
    def render(self):
        r = self.request
        if r.force_plain_content or r.plain_content:
            return r.plain_content
        dirs = [os.path.abspath(
                    os.path.join(os.path.dirname(p.__file__), 
                                 config['system']['mako']['directory']))
                for p in lascaux.app_packages]
        k = Kitchen(dirs, config['system']['mako']['extensions'])
        file_ = k.get(self.final_template)
        t = Template(filename=file_, module_directory=os.path.join(
            config.get_tmp(), config['system']['mako']['cache_dir']))
        return t.render(**self.get_content()).encode('utf-8')
