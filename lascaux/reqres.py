# -*- coding: utf-8 -*-

import weakref
import time

from lascaux import config
from lascaux.httpcookie import HttpCookie
from lascaux.session import Session
from lascaux.sys.logger import logger


logger = logger(__name__)


class Reqres(object):

    _init_time = None
    _close_time = None

    app = None
    uri = u''
    static_path = u''
    flag_redirect = u''
    error = False

    headers = dict()
    http_status_code = "202 SUCCESS"
    http_extra = dict()
    request_method = 'get'

    cookies = None
    session = None

    content = dict()
    force_plain_content = False

    exec_paths = list()

    def __init__(self, app=None, uri=u'', redirect=False, headers=dict()):
        self._init_time = time.time()
        self.app = app and weakref.proxy(app) or None
        self.uri = uri
        self.flag_redirect = redirect
        self.headers = headers or {'Content-type': 'text/html'}
        self.http_extra = dict()
        self.cookies = HttpCookie(self)
        self.session = Session(self)
        self.content = dict()
        self.execpaths = list()

    def close(self):
        self._close_time = time.time()
        logger.info(u'%s milliseconds' % ((self._close_time -
                                           self._init_time) * 1000))
        self.session.save()
        # self.cookies.bake()
        if config['debug']:
            for header in self.headers:
                self.save(u'%s %s' % (header, self.headers[header]), 'debug')
            self.save(u'Request time: %s milliseconds' % ((self._close_time - self._init_time) * 1000),
                      'debug')

    def find_execpaths(self):
        for router in self.app.manager.get_subsystem('router').get_routers():
            execpath = router.find_execpath(self)
            if execpath:
                self.execpaths.append(execpath)

    def execute(self):
        instance = self.execpaths[0].controller(self, self.execpaths[0])
        getattr(instance, self.request_method)(*self.execpaths[0].args.values(), **self.execpaths[0].args)

    def save(self, content, location='main'):
        self.content.setdefault(location, list())
        self.content[location].append(content)

    def erase_content(self):
        self.content = dict()

    def render(self):
        if self.force_plain_content:
            # Yes, this should be a string, not a unicode.
            return '\n'.join(self.content['main'])
        final = u''
        for location in self.content:
            if location == 'debug':
                continue 
            for content in self.content[location]:
                final += u'\n%s' % content
        if 'debug' in self.content:
            final += u'<hr /><pre>\n%s</pre>' % u'\n'.join(self.content['debug'])
        return final

    def redirect(self, uri, code=None):
        code = code or config['defaults']['redirect_code']
        self.flag_redirect = True
        self.set_http_code(code)
        self.headers['Location'] = uri

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
