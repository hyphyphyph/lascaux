import weakref
try: # Python 3
    import http.cookies as http_cookies
except: # Python 2
    import Cookie as http_cookies

from lascaux import SObject


class HTTPCookie(dict, SObject):

    request = None

    def __init__(self, Request):
        self.request = weakref.proxy(Request)

    def set(self, Key, Value):
        self[str(Key)] = Value

    def load(self, RAW):
        if RAW:
            cookie = http_cookies.SimpleCookie()
            cookie.load(RAW)
            for key in cookie:
                self[key] = cookie[key].value

    def save(self):
        if self:
            cookie = http_cookies.SimpleCookie()
            for key in self:
                cookie[key] = self[key]
            self.request.headers.set("Set-cookie", cookie.output(header=""))
