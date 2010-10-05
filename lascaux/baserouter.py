from lascaux.model import create_store
from lascaux import SObject, Redirect


class BaseRouter(SObject):
    def __init__(self):
        pass

    def find_route(self, App, Request):
        pass

    def exec_route(self, App, Request):
        instance = Request.exec_plugin["__class__"](Request)
        instance.db = create_store()
        method = getattr(instance, Request.exec_route["action"])
        App.hook("pre_exec", {"app": App,
                              "request": Request,
                              "controller": instance,
                              "method": Request.exec_route["action"],
                              "args": Request.exec_args})
        return_ = method(**Request.exec_args)
        App.hook("post_exec", {"app": App,
                              "request": Request,
                              "controller": instance,
                              "method": Request.exec_route["action"],
                              "args": Request.exec_args,
                              "return_": return_})
        if isinstance(return_, Redirect):
            Request.flag_redirect = True
            Request.URI = return_.where or "/"
            Request.set_http_code(return_.code)
            Request.headers["Location"] = Request.URI
        return return_

    def get_route(self, controller, action, args={}):
        pass
