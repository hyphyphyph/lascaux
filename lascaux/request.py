from lascaux import SObject
from lascaux import HTTPHeader, HTTPCookie, Session


class Request(SObject):

    headers = {}
    header = None
    cookie = None
    session = None

    def __init__(self):
        headers = {}
        self.header = HTTPHeader(self)
        self.cookie = HTTPCookie(self)
        self.session = Session(self)

    def redirect(self, Where, Code="302"):
        pass
