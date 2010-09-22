import weakref

from lascaux import SObject


class HTTPHeader(dict, SObject):

    request = None

    def __init__(self, Request):
        self["Content-type"] = "text/html"
        self.request = weakref.proxy(Request)

    def set(self, Header, Value):
        self[Header] = Value
