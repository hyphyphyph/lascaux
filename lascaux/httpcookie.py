import weakref
try: 
    # Python 3
    import http.cookies as http_cookies
except: 
    # Python 2
    import Cookie as http_cookies

from lascaux import config


class HttpCookie(dict):

    reqres = None

    def __init__(self, reqres):
        self.reqres = weakref.proxy(reqres)

    def eat(self, dough):
        """ Dough is so much better than the baked version anyway... """
        if dough:
            cookie = http_cookies.SimpleCookie()
            cookie.load(dough)
            for key in cookie:
                self[key] = self._clean(cookie[key].value)

    def bake(self):
        if self:
            cookie = http_cookies.SimpleCookie()
            for key in self:
                cookie[str(key)] = self[key]
            self.reqres.headers['Set-cookie'] = cookie.output(header='')

    def _clean(self, value):
        """ Normalizes some values to be more pythonic... """
        if value in ('None'):
            return None
        return value
