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
        self[Key] = Value

    def save(self):
        cookie_ = http_cookies.SimpleCookie()
        for key in self:
            cookie_[key] = self[key]
        output = "%s; " % cookie_.output(header="")
        if self.request.config["cookie"].get("output_path"):
            output += "path=/; "
        if self.request.config["cookie"].get("output_domain"):
            output += "domain=%s; " % self.request.get_domain()
        if self.request.config["cookie"].get("http_only"):
            output += "HttpOnly"
        self.request.headers.set("Set-cookie", "%s" % output)
