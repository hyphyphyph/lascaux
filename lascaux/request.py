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
    flag_redirect = None
    http_status_code = "202 SUCCESS"
    exec_plugin = None
    exec_route = None
    exec_args = None
    POST = None

    def __init__(self, URI):
        self.URI = URI
        self.headers = HTTPHeader(self)
        self.cookies = HTTPCookie(self)
        self.session = Session(self)
        self.content = u""
        self.exec_args = {}
        self.POST = {}

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

    def get_http_headers(self):
        self.cookies.save()
        headers = []
        for header in self.headers:
            headers.append((header, self.headers[header]))
        return headers
