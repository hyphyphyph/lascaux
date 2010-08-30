import weakref

from lascaux import SObject


class HTTPCookie(dict, SObject):

    request = None

    def __init__(self, Request):
        self.request = weakref.proxy(Request)

    def set(self, Key, Value):
        self[Key] = Value
