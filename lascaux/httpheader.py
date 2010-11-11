import weakref

from lascaux.sys import SObject


class HTTPHeader(dict, SObject):

    request = None

    def __init__(self, request):
        self["Content-type"] = "text/html; charset=utf-8"
        self.request = weakref.proxy(request)

    def set(self, header, value):
        self[header] = value
