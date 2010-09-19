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
    http_status_code = "202 SUCCESS"

    def __init__(self, URI):
        self.URI = URI
        self.headers = HTTPHeader(self)
        self.cookies = HTTPCookie(self)
        self.session = Session(self)
        self.content = u""

    def get_content(self):
        return self.content

    def save(self, Content):
        self.content += Content

    def redirect(self, Where, Code="302"):
        pass

    def set_http_code(self, Code):
        self.http_status_code = Code

    def get_http_code(self):
        return self.http_status_code
