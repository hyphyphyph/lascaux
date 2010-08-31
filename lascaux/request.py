from lascaux import SObject
from lascaux.httpheader import HTTPHeader
from lascaux.httpcookie import HTTPCookie
from lascaux.session import Session


class Request(SObject):

    URI = None
    headers = None
    cookies = None
    session = None
    content = None

    def __init__(self, URI):
        self.URI = URI
        self.headers = HTTPHeader(self)
        self.cookies = HTTPCookie(self)
        self.session = Session(self)
        self.content = ""

    def redirect(self, Where, Code="302"):
        pass

    def get_http_code(self):
        return "202 SUCCESS"
